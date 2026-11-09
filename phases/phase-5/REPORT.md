# Phase 5 — Chunking: splitting long lists/tables/lines + rechunking

Date: 5 November 2026. Reports: `reports/20261105-0019-retrieval.md`, `reports/20261105-0116-answers.md`.

## Change

- `chunk_markdown` splits long lists, tables and lines at a 1,500-character limit; the table header is repeated in
  every chunk. `test_long_bullet_list_respects_max_chars`, formerly xfail, now passes.
- `indexer.rechunk_document`: rechunks from the stored page text without OCR (one transaction per page, can be rerun).
- Only the pages whose split changed were rewritten: doc1 24 pages (6 min), doc2 28 pages (32 min), doc3_sample
  5 pages (2.5 min).
  - The number of chunks went from 657 to 713: doc1 298, doc2 304, doc3_sample 111.
  - The longest chunk went from 6,104 characters to 1,500.
- Backup: `backups/pre-faz5-20261104-2306.dump` (outside git).

Two more changes are in the same measurement:

- **Golden:** the user added a second valid page to 7 doc2 questions (Phase J report).
- **Memory fix Z13:** embedder and reranker inputs are padded to multiples of 128. The score difference is at most 0.00017.

The effect of the golden change is computed separately below. The judge is the same as in Phase J
(`judge_sha256` c2301e4f60d7).

## Retrieval (live system: hybrid + reranker)

| Metric | Phase 4 | Phase 5 | Pass threshold |
|---|---|---|---|
| Recall@1 | 0.81 | **0.88** | ≥ 0.80 |
| Recall@6 | 0.96 | 0.94 | ≥ 0.90 |
| MRR | 0.879 | **0.918** | ≥ 0.85 |
| doc2 R@1 / R@6 | 0.33 / 0.83 | 0.67 / 0.75 | — |
| Turkish R@1 | 0.75 | 0.92 | — |

- The R@6 drop comes from a single question: d2q03 went from rank 6 to rank 8.
- Part of the doc2 R@1 gain comes from the pages added to the golden set.
- Vector search alone also improved (R@6 0.94 → 0.97). The embedding of a short chunk carries its topic more clearly.

## Answers

| Metric | Phase J | Phase 5 | Pass threshold |
|---|---|---|---|
| answer_correctness | 0.94 | **0.97** | ≥ 0.85 |
| faithfulness | 0.93 | **0.94** | ≥ 0.92 |
| cites_expected_page | 0.83 (0.93 with the new golden) | 0.90 | ≥ 0.85 |
| citation_precision | 0.77 (0.87 with the new golden) | 0.84 | ≥ 0.80 |
| answers_without_citation | 0.00 | 0.00 | ≤ 0.05 |
| unanswerable_refused | 1.00 | 1.00 | ≥ 0.90 |
| unanswerable_with_citation | 0.00 | **0.15** ❌ | 0.00 |
| false_refusals | 0.00 | 0.00 | ≤ 0.05 |
| p50 / p95 latency | 39.6 / 103.9 s | 35.4 / 67.0 s | ≤ 30 / ≤ 60 s |

**Improvements:**

- **The repetition loops disappeared.** In Phase J, q33, q36, q37 and d2q10 repeated the same sentence 6–40 times
  (175–208 s). In Phase 5 the longest answer is under 2,500 characters and the slowest question takes 81 s.
  - p95 went from 104 s to 67 s.
  - q33 and q36 are now correct; Turkish correctness went from 0.75 to 0.92.
  - The loops appear to have been triggered by the long chunks (LaTeX-heavy, 3.5–6 thousand characters).
- The measurement finished in one go without hitting the memory guard (Z13 fix).

**Regressions:**

- **Citations:** with the golden effect removed, i.e. Phase J rescored with the new golden, cites_expected_page went
  from 0.928 to 0.899 and citation_precision from 0.872 to 0.843. That is about two questions (q26 and q33 no longer
  show the correct page).
  - It stays under the "> 0.03" limit of rule 0.4, so it does not count as a significant regression, but it is borderline.
  - Accepted deliberately: the gains in correctness, faithfulness and latency are larger.
- **Refusal sentence with citations (0.15):** q42 and q45 write "The documents do not contain information about this
  [1][2][3][4][5][6]." The prompt is the same; only the retrieved chunks changed. So Phase 3c's sep_rule is fragile.
  - In the answer the user gets, these citations do not show as sources because the refusal regex catches them. But
    the raw-text metric misses the target.
  - Added to the Phase 5b sweep: the `[1][2]…[6]` sequence is also a form of repetition; an n-gram block or a
    repetition penalty might fix it.

## Decision

Phase 5 was kept. Retrieval, correctness, faithfulness and latency improved. The two-question drop in citations is
under the limit. unanswerable_with_citation is handled in Phase 5b.
