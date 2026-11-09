# Phase 1b — New baseline on a three-document index

Date: 4 November 2026. Phase 1 was measured on doc1 only; since the success criteria cover doc2 and doc3
(SUCCESS_CRITERIA §0.2), a new baseline was taken with the same code on a three-document index.

## What changed (data, not code)

| | Phase 1 | Phase 1b |
|---|---|---|
| Index | doc1 (99 pages, 276 chunks) | + doc2 (CODATA 2022, 62 pages text layer, 269 chunks) + doc3 sample (1966 scanned report, 40 pages Chandra OCR, 112 chunks) |
| Development set | `golden_doc1.jsonl` 45 questions | `golden_dev.jsonl` 82 questions (doc2 14, doc3 23; doc3 has 5 table, 4 figure, 2 multi-page) |
| Report | breakdown by type | + breakdown by document |

The doc3 questions were written from the indexed Chandra text and their key phrases were verified in the text; the
`orig_pages` field holds the original doc3 page (the page number in the index is the page of the sample PDF,
`eval/doc3_sample_pages.json`).

## Retrieval (`reports/20261104-1019-retrieval.md`, 69 answerable questions)

| Method | R@1 | R@6 | MRR | All pages@6 (n=5) |
|---|---|---|---|---|
| vector | 0.81 | 0.94 | 0.867 | 0.40 |
| keyword | 0.07 | 0.29 | 0.169 | 0.00 |
| hybrid (RRF) | 0.41 | 0.83 | 0.548 | 0.00 |
| vector + reranker | 0.81 | 0.96 | 0.879 | 0.60 |
| **hybrid + reranker (live)** | **0.81** | **0.96** | **0.880** | 0.60 |

| Document (n) | live R@6 / MRR |
|---|---|
| doc1 (37) | 1.00 / 0.94 |
| doc2 (12) | **0.75 / 0.55** |
| doc3 sample (20) | 1.00 / 0.97 |

Findings:

- **doc3 (scanned, OCR) is better than expected:** the correct page is at rank 1 in 18 of 20 questions, including
  table and figure questions. Chandra's figure descriptions (`![Figure 1: …]`) make figure questions searchable.
- **doc2 is the weak link:** d2q03 (G constant, table) at rank 29, d2q10 (paraphrase) at 14, d2q12 at 7. doc2 chunks are
  up to 6,104 characters long (tables and LaTeX); the reranker can only judge the start of a long chunk → candidate
  for Phase 5 (chunking).
- **Keyword search is almost useless (R@6 0.29)** and RRF disturbs the vector ranking in the live system (hybrid R@1
  0.41 < vector 0.81). Cause (isolated with a GPU-free experiment): the query ORs every word including fillers such as
  "what/the/does…", and `ts_rank_cd` favours long chunks in multi-term OR queries. With a filler-word list +
  `ts_rank(tsv, q, 1)` keyword R@6 goes 0.29 → **0.86** → Phase 4.
- Pass thresholds (on the development set, live system): R@6 0.96 ≥ 0.90 ✅, R@1 0.81 ≥ 0.80 ✅ (borderline), MRR
  0.88 ≥ 0.85 ✅, R@6 per type (n ≥ 8): factual 1.00, paraphrase 0.91, table 0.91, turkish 0.92 ✅.

## Answers — partial (q01–q42, all doc1) and the crash

The evaluation stopped twice at question 43 (q43, the unanswerable "What is the capital of Australia?") with a process
crash: `Segmentation fault` in `eager_attention_forward`. The prompt was 13,298 tokens (doc2's huge chunks + 3 images).
Details and hypothesis tests: [CHALLENGES.md Z9, Z10](../CHALLENGES.md). **The baseline system crashed on every question
that needed a long context (the user interface included)** — so Phase 2 was taken before the citation rate.

Results of the first 42 questions (`reports/20261104-answers-partial-42.jsonl`; the same questions as Phase 1, now on
the multi-document index):

| Metric | Phase 1 (45 questions) | Phase 1b (first 42) |
|---|---|---|
| answer_correctness | 0.92 | 0.92 |
| faithfulness | 0.96 | 0.95 |
| cites_expected_page | 0.73 | 0.70 |
| answers_without_citation | 0.24 | **0.30** (11 questions) |
| false_refusals | 0.00 | 0.00 |
| unanswerable_refused | 1.00 | 1.00 (n=5) |
| latency p50 / p95 | — / — | 41.7 / 76.4 s |

The multi-document index did not noticeably hurt the doc1 answers (small distractor effect); the problem of short
uncited answers continues.

## Next phases

1. **Phase 2 — stability:** a prompt token budget (to prevent the crash).
2. **Phase 3 — citation rate** (the top improvement since Phase 1).
3. **Phase 4 — keyword search** (filler words + `ts_rank`).
4. **Phase 5 — chunking** (splitting long lists/tables, `rechunk_document`).
5. **Phase 6 — latency** (p50 41.7 s > the 30 s target).
