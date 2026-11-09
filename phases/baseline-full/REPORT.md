# Baseline: full index (doc1 + doc2 + all 200 pages of doc3), with Phase 5c

Date: 5 November 2026.

- Index: 3 documents, 1,164 chunks. The whole doc3.pdf instead of doc3_sample.
- Golden: `golden_dev.jsonl` (sha 236b0d3efd8e). doc3 questions use the original page numbers.
  - The extra-page proposal is not applied yet: `../doc3-full-golden-check.md`.
- Reports: `reports/20261105-0756-retrieval.*`, `reports/20261105-0849-answers*`.
- The measurement finished in one go: the memory guard did not step in and no resume was needed. 82 questions took ~50 min.

## Retrieval (hybrid + reranker)

| Metric | Phase 5 (doc3 sample) | Full index | Pass |
|---|---|---|---|
| Recall@1 | 0.88 | 0.86 | ≥ 0.80 |
| Recall@6 | 0.94 | 0.94 | ≥ 0.90 |
| MRR | 0.918 | 0.903 | ≥ 0.85 |
| doc3 R@6 / MRR | — | 1.00 / 0.93 | — |

- doc3 grew by 160 pages but R@6 stayed at 1.00.
- The R@1 drop comes from three doc3 questions (d3q02, d3q03, d3q19 at rank 2).
  - For d3q02 and d3q19 the chunk at rank 1 is on the repeated pages of the extra-page proposal. If the golden change
    is approved, these two will most likely move to rank 1.
- Still outside the top 6: q24 (7), d2q03 (8), d2q10 (15), d2q12 (7).

## Answers

| Metric | Phase 5 | Full index + 5c | Pass |
|---|---|---|---|
| answer_correctness | 0.97 | 0.97 | ≥ 0.85 ✅ |
| faithfulness | 0.94 | 0.96 | ≥ 0.92 ✅ |
| citation_precision | 0.84 | 0.82 | ≥ 0.80 ✅ |
| cites_expected_page | 0.90 | 0.90 | ≥ 0.85 ✅ |
| answers_without_citation | 0.00 | 0.00 | ≤ 0.05 ✅ |
| false_refusals | 0.00 | 0.00 | ≤ 0.05 ✅ |
| unanswerable_refused | 1.00 | 1.00 | ≥ 0.90 ✅ |
| unanswerable_with_citation | 0.15 | **0.00** | 0.00 ✅ |
| raw_unanswerable_with_citation (informational) | — | 0.15 | — |
| p50 / p95 latency | 35.4 / 67.0 s | 31.4 / 63.5 s | ≤ 30 / ≤ 60 ❌ |

- **Phase 5c confirmed in a real measurement.**
  - Refusal citations 0.00; 0.15 in the raw text (the q42/q45 type of cited refusal continues but does not reach the user).
  - q44, q45 and d3u03 got a Turkish refusal.
- Wrong answers:
  - q24: the independent-version question. The correct page is at rank 7.
  - d2q12: Turkish, doc2. The correct page is at rank 7.
  - Both are retrieval problems.
- d3q19 showed only p.111, and the whole answer is there. It will count as correct if the golden proposal is approved.

## E2E tests

`pytest tests/e2e`: 25/25 passed (3 min). Coverage:

- UI tests:
  - Turkish question, source images.
  - Search details.
  - English follow-up question (worked for the first time).
  - Turkish refusal (new).
- Prompt injection test.
- Refusal judge test (15/15).

## Status

All answer and retrieval thresholds of the success criteria pass. Remaining:

- Latency: p50 31.4 s (target ≤ 30), p95 63.5 s (target ≤ 60).
- TTFT: no streaming yet.
- The final holdout test.
