# Final holdout measurement (5 November 2026)

`eval/golden_final.jsonl`: 72 questions (57 answerable, 15 unanswerable), written by the user, not opened during
development. Run once; no setting was tuned on its result. Settings: Phase 8b (896 px, 2 page images, refusal buffer
60 chars, ENOUGH_SCORE 0.5). Reports: `reports/20261105-1921-retrieval.*`, `reports/20261105-1952-answers.*`.
The memory guard never stepped in; the run was uninterrupted.

## Retrieval (hybrid + reranker)

| Metric | Pass | Final | |
|---|---|---|---|
| Recall@6 | ≥ 0.90 | 0.98 | ✅ (also the target ≥ 0.95) |
| Recall@1 | ≥ 0.80 | 0.89 | ✅ |
| MRR | ≥ 0.85 | 0.934 | ✅ (also the target ≥ 0.92) |
| All pages@6 (multi_page n=8) | ≥ 0.70 | 1.00 | ✅ |
| Recall@6 per type (lowest) | ≥ 0.85 | turkish 0.90 | ✅ |
| Reranker score separation | ≥ 0.50 | 0.949 − 0.366 = 0.58 | ✅ |

## Answers

| Metric | Pass | Final | |
|---|---|---|---|
| faithfulness (judge) | ≥ 0.92 | 0.94 | ✅ |
| answer_correctness | ≥ 0.85 | 0.91 | ✅ |
| cites_expected_page | ≥ 0.85 | 0.95 | ✅ |
| citation_precision | ≥ 0.80 | 0.87 | ✅ |
| answers_without_citation | ≤ 0.05 | 0.00 | ✅ |
| unanswerable_refused (n=15) | ≥ 0.90 | 1.00 | ✅ |
| unanswerable_with_citation | 0.00 | 0.00 | ✅ (raw: 0.07, informational) |
| false_refusals | ≤ 0.05 | 0.02 (f51) | ✅ |
| latency p50 / p95 | ≤ 30 / ≤ 60 s | 22.2 / 40.4 | ✅ |
| TTFT p50 | ≤ 15 s | **15.2** (p95 30.5) | ❌ by 0.2 s |

Wrong answers (5/57): f39 (figure), f44 (multi_page), f49, f51 (false refusal), f54 (turkish). On Turkish questions
correctness is 0.70 and gold page cited 0.70: the weakest subgroup (no per-type correctness threshold, informational).

## Outcome

- All 17 quality/retrieval criteria passed on the final set.
- TTFT p50 15.2 s missed the ≤ 15 target by 0.2 s (dev 12.9). The final result was recorded without changing any
  setting; this criterion is reported as **not passed**.
- Not yet done (SUCCESS_CRITERIA §3–4): judge calibration on the final set (user labels, kappa) and GitHub CI (needs the
  user's approval). Success cannot be fully declared without these two.

## Decisions (user, 5 November 2026)

- TTFT p50 15.2 s: the 0.2 s gap was accepted as hardware/OS variance; no setting was changed.
- Judge calibration: `reports/20261105-1952-answers-judgments-to-label.jsonl` (90 rows: per kind all of the judge's
  rare decisions + random ones, seed 0) given to the user for labelling.

## Judge calibration (SUCCESS_CRITERIA §3; labels from the user, 90 rows)

| Kind | n | Agreement (≥ 0.85) | Kappa (≥ 0.70) | |
|---|---|---|---|---|
| claim_supported | 30 | 0.93 | 0.79 | ✅ |
| correct | 30 | 1.00 | 1.00 | ✅ |
| refusal | 30 | 1.00 | 1.00 | ✅ |

With the labels, final faithfulness is 0.94 → 0.958. There is no disagreement with the judge's correctness decisions,
so the 0.91 correctness also holds with human labels.

## Final result

On the final holdout set the retrieval (6/6), answer quality (11/11) and judge reliability (3/3) criteria passed; TTFT
p50 15.2 s was accepted by the user's decision. Unit + integration 80/80, e2e 25/25 (Phase 7). **The success criteria
are met**; one open item: pushing to GitHub and CI (§4), awaiting the user's approval.

## CI (6 November 2026)

The repository was pushed to GitHub (https://github.com/neslihaneti/multimodal-rag). The GitHub Actions `tests`
workflow is green: 83 tests passed, 2 modules skipped (those needing the real models/Docling). The last item of
SUCCESS_CRITERIA §4 is also met.
