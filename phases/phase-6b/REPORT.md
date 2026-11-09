# Phase 6b — Skip the search decision when the reranker score is high

Date: 5 November 2026. Report: `reports/20261105-1252-answers*`. Built on 6a (896 px).

## Change

- `rag.ENOUGH_SCORE = 0.5`: if the best chunk of the first search has a reranker score ≥ 0.5, the model is not asked
  the "is this enough?" decision (SEARCH_DECISION).
- Rationale (full-index retrieval data):
  - All 69 answerable questions already finished in one round, i.e. the model said "ENOUGH" every time.
  - 62 of these questions score above 0.5.
  - The highest score of an unanswerable question is 0.34. These questions are still sent to the model and searched
    again if needed.
- Unit test: `test_high_rerank_score_skips_the_decision`.

## Result

| Metric | 6a | 6b |
|---|---|---|
| Answers | — | **82/82 identical** |
| Quality metrics | correct 0.99, faith 0.91, prec 0.84, cites 0.90 | same |
| p50 | 22.5 s | **21.6 s** |
| mean | 30.7 s | **29.1 s** |
| p95 | 55.7 s | 56.8 s (noise; the slowest are the q36/q37 loop and unanswerable questions) |

- The memory guard restarted the run once (66 GB); the interrupted question was measured again.
- The gain is small (the decision call is 1–3 s on a short prompt), but it comes without changing the output.

## Phase 6c

Skipped, by the user's decision: after 6a + 6b, p50 21.6 ≤ 30 and p95 56.8 ≤ 60. The risky sdpa experiment was no
longer needed. Next step: streaming/TTFT.
