# Success criteria

Agreed: 4 November 2026 (discussed and agreed with the user). Phases continue until these criteria are met.

Update 5 November 2026 (user approval, Phase 5c): `unanswerable_with_citation` is now measured on the answer the system
returns; the rate in the model's raw text is reported for information as `raw_unanswerable_with_citation`.

Update 5 November 2026 (user approval, Phase 8): the TTFT p50 target was relaxed from ≤ 10 s to ≤ 15 s. On this
hardware, the search (4–5 s) and the local model's reading of the prompt (prefill) do not bring the first text below
10 s; the value reached while keeping quality is 12.9 s (Phase 8b, 2 page images).

**Success statement:** the system meets criteria defined in advance **on an unseen final test set**.
(Indefensible claims such as "very successful by 2026 standards" are not used.)

## 0. General rules

1. **Two sets.**
   - Development set: `eval/golden_doc1.jsonl` (45 questions; doc2/doc3 questions may be added later). Prompt, chunking
     and search settings are tuned by looking at this set only. Phases are compared on this set.
   - Final (holdout) test set: run **once** after all development is finished; success is declared only on it. It is
     not opened during development and nothing is tuned on its result. It is not written by the same person/model
     that writes questions by looking at the pages (Claude); the user writes it (to avoid easy questions / a ceiling effect).
2. **Scope:** doc1, doc2 and doc3 are indexed (multi-document distractor effect). doc3 is a scanned document and tests
   the Chandra OCR + VLM visual reading layer.
3. **Sample:** at least 8–10 questions of each type in the final set (factual, paraphrase, table, figure/OCR,
   multi_page, turkish), 15–20 unanswerable questions (~70–80 in total). If a subgroup has n < 8, it is reported for
   information only and no pass/fail threshold applies.
4. **No regression:** each phase must not significantly lower the previous phase's primary metrics. Significant drop =
   more than one question on the development set (> 0.03 on 37 answerable questions), or any automated test breaking.
   If there is a drop, its reason is written in the phase report and it is accepted deliberately, or the change is
   rolled back.
5. All "Pass" thresholds below must be met on the final set. The "Target" column is an ambitious goal, not mandatory.

## 1. Retrieval (`python3 evaluate.py retrieval`)

Basic rule: the correct page must be in the top TOP_K = 6, and each added step (RRF, reranker) must not be
significantly worse than pure vector search in Recall@6 and MRR.

| Metric (live system: hybrid + reranker) | Pass | Target | Phase 1 (development set) |
|---|---|---|---|
| Recall@6 | ≥ 0.90 | ≥ 0.95 | 0.97 (vector 1.00) |
| Recall@1 | ≥ 0.80 | ≥ 0.90 | 0.89 (vector 0.97) |
| MRR | ≥ 0.85 | ≥ 0.92 | 0.932 (vector 0.986) |
| All pages@6 (multi-page, n ≥ 8) | ≥ 0.70 | ≥ 0.85 | 0.33 (n = 3, informational) |
| Recall@6 for each question type (n ≥ 8) | ≥ 0.85 | ≥ 0.95 | paraphrase 0.88, the others 1.00 (most n < 8) |
| Reranker score separation (answerable − unanswerable mean) | ≥ 0.50 | answerable > 0.75, unanswerable < 0.15 | 0.823 − 0.052 |

## 2. Answers (`python3 evaluate.py answers`)

| Metric | Meaning | Pass | Phase 1 |
|---|---|---|---|
| faithfulness | share of the answer's claims supported by the retrieved excerpts | ≥ 0.92 | 0.96 |
| answer_correctness | factual agreement with the golden answer (judge) | ≥ 0.85 | 0.92 |
| cites_expected_page | the citations include the gold page | ≥ 0.85 | 0.73 |
| citation_precision | share of the given citations that point to a correct page | ≥ 0.80 | 0.91 |
| answers_without_citation | uncited answer to an answerable question | ≤ 0.05 | **0.24** |
| unanswerable_refused | refusing an unanswerable question | ≥ 0.90 | 1.00 (n = 8) |
| unanswerable_with_citation | citing while refusing: the answer the system returns (`result["answer"]`) | 0.00 | 0.00 |
| raw_unanswerable_with_citation | the same, in the model's raw text (before the refusal sentence is replaced); informational | — | 0.00 |
| false_refusals | refusing a question that has an answer | ≤ 0.05 | 0.00 |
| latency p50 | per question | ≤ 30 s | (mean 45 s; p50 not measured yet) |
| latency p95 | including multi-round and unanswerable questions | ≤ 60 s | (unanswerable mean 72 s) |
| TTFT p50 | time until the first text appears (streaming) | ≤ 15 s (previously: ≤ 10 s) | no streaming |

## 3. Judge reliability (`python3 evaluate.py calibrate`)

- The **user** gives the labels (so that an AI judge is not validated by AI).
- Stratified sampling: **all** rows where the judge said "wrong / unsupported / refused" + random "correct" rows.
- Separately for each kind (`correct`, `claim_supported`, `refusal`), at least 25–30 labelled rows per kind.

| Metric (for each kind) | Pass |
|---|---|
| Agreement | ≥ 0.85 |
| Cohen's kappa | ≥ 0.70 |

If kappa < 0.60, the answer metrics based on that kind (correctness, faithfulness) are considered unreliable and
success cannot be declared.

## 4. Engineering and security tests

| Test | Pass |
|---|---|
| `pytest` (unit + integration) | 0 failed; `test_long_bullet_list_respects_max_chars` must leave xfail and pass normally |
| `pytest tests/e2e/test_prompt_injection.py` | 0 leaks: neither the canary nor the fake URL enters `rag_chunks.context` or the answer; the real facts (90 days, 15 min) are answered correctly with a source |
| `pytest tests/e2e/test_ui.py` | answers are produced for Turkish and English questions, source images load (`img.complete && naturalWidth > 0`), "Search details" shows the queries and rerank scores |
| CI | actually runs green on GitHub Actions |

## 5. Infrastructure work needed to reach the criteria

So that the criteria can be measured (to be added to the phase plan):

- [ ] `evaluate.py answers`: latency p50 and p95; n per question type and an "informational" mark for n < 8
- [ ] `evaluate.py calibrate`: a helper command that produces a stratified labelling list
- [ ] An English question in the UI test (currently Turkish only)
- [ ] Streaming + TTFT measurement
- [ ] Indexing doc2 (~30–40 min) and doc3 (200 scanned pages, ~4–11 hours); for doc3, page-level resume first
- [ ] The final test set (user, ~70–80 questions, three documents) and doc2/doc3 questions in the development set
- [ ] Git repository + push to GitHub (with the user's approval), CI green

(All of these were done by 6 November 2026; see [README.md](README.md) and [final/REPORT.md](final/REPORT.md).)
