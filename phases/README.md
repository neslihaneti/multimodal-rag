# Phases: measure → fix → measure again

Goal: [`SUCCESS_CRITERIA.md`](SUCCESS_CRITERIA.md). Phases continue until these criteria are met on the final test set.

Each improvement is a separate phase. A phase has these steps:

1. **Goal:** which problem we are solving and which measurement we expect to change (from the previous phase's report).
2. **Change:** a single improvement in the code (more than one change mixes up the effects).
3. **Measure again:** `pytest`, `pytest tests/e2e`, `python3 evaluate.py retrieval`, and if needed `python3 evaluate.py answers`.
4. **Compare:** side by side with the previous phase's tables; did it improve, did something else break (regression)?
5. **Record:** `phase-N/REPORT.md` + a copy of the measurement reports in `phase-N/reports/`; difficulties go into
   [`CHALLENGES.md`](CHALLENGES.md).

| Phase | Topic | Status | Report |
|---|---|---|---|
| 1 | Test infrastructure built, baseline measurement | ✅ 4 November 2026 | [phase-1/REPORT.md](phase-1/REPORT.md) |
| 1b | Three-document index (doc1 + doc2 + doc3 sample), 82-question development set, new baseline; crash found at q43 | ✅ 4 November 2026 | [phase-1b/REPORT.md](phase-1b/REPORT.md) |
| 2 | Stability: segfault on long prompts → token budget + clearing the MPS cache; 82/82 completed | ✅ 4 November 2026 | [phase-2/REPORT.md](phase-2/REPORT.md) |
| 3 | Citation rate: uncited 0.30→0.00, correct page 0.62→0.87 (side effect: citations while refusing 0.38) | ✅ 4 November 2026 | [phase-3/REPORT.md](phase-3/REPORT.md) |
| 3b | Refusal sentence without citations (exception in the prompt): no effect (0.38 → 0.38), rolled back | ❌ 4 November 2026 | [phase-3b/REPORT.md](phase-3b/REPORT.md) |
| 3c | Refusal: 5 prompt variants in a quick sweep; a fixed refusal sentence chosen (5 → 0 citations in the sweep) | ✅ 4 November 2026 (full measurement in Phase J) | [phase-3c/REPORT.md](phase-3c/REPORT.md) |
| J | Judge: sentence = claim, checked against the cited excerpt, correctness and cross-language prompts (from the user's calibration) | ✅ 4 November 2026 (correctness 0.94, refusal citations 0.38→0.00; calibration: claim κ 0.61→0.86, all three kinds pass; doc2 golden corrected) | [phase-j/REPORT.md](phase-j/REPORT.md) |
| 4 | Keyword search: keyword R@6 0.29→0.86, hybrid R@1 0.41→0.71; live system neutral | ✅ 4 November 2026 | [phase-4/REPORT.md](phase-4/REPORT.md) |
| 5 | Chunking (splitting long lists/tables, rechunking): R@1 0.81→0.88, correct 0.97, p95 104→67 s, loops gone; refusal citations 0.15 | ✅ 5 November 2026 | [phase-5/REPORT.md](phase-5/REPORT.md) |
| 5b | Repetition-block sweep: HF n-gram block corrupts numbers (2017→2020), loops already gone in Phase 5 → no generation setting; sentence deduplication in the judge | ✅ 5 November 2026 | [phase-5b/REPORT.md](phase-5b/REPORT.md) |
| 5c | Fixed refusal sentence, in the question's language and without citations (in simulation refusal citations 0.15→0.00, Turkish refusal to Turkish questions); success criteria updated | ✅ 5 November 2026 (full measurement in the new baseline) | [phase-5c/REPORT.md](phase-5c/REPORT.md) |
| B | Full-index baseline (doc3 200 pages): R@6 0.94, correct 0.97, refusal citations 0.00; all quality thresholds pass, latency p50/p95 31.4/63.5 s ❌; e2e 25/25 | ✅ 5 November 2026 | [baseline-full/REPORT.md](baseline-full/REPORT.md) |
| 6a | Page images 1280→896 px: p50/p95 31.4/63.5 → 22.5/55.7 s, correct 0.99; faithfulness 0.91 (judge labels pending), q36/q37 loop came back | ✅ 5 November 2026 (labels pending for faithfulness) | [phase-6a/REPORT.md](phase-6a/REPORT.md) |
| 6b | Skip the search decision if the reranker score is ≥ 0.5: answers 82/82 identical, p50 21.6 s | ✅ 5 November 2026 | [phase-6b/REPORT.md](phase-6b/REPORT.md) |
| 6c | sdpa | ⏭ skipped (target met with 6a+6b) | — |
| 7 | Streaming: answers 82/82 identical, total p50 19.9 s; TTFT p50/p95 17.7/37.5 s ❌ (prefill 7–10 s + first-sentence buffer) | ✅ 5 November 2026 (TTFT proposal with the user) | [phase-7/REPORT.md](phase-7/REPORT.md) |
| 8 | Refusal buffer 60 chars + 2 page images: correct 0.97, faithfulness 0.957 (human-labelled), TTFT p50 12.9 s; TTFT target ≤ 15 s | ✅ 5 November 2026 | [phase-8/REPORT.md](phase-8/REPORT.md) |
| Final | Holdout of 72 questions: 17 quality/retrieval criteria ✅, judge calibration 3/3 ✅ (kappa 0.79/1.00/1.00); TTFT p50 15.2 s (accepted by the user) | ✅ 5 November 2026 | [final/REPORT.md](final/REPORT.md) |
| 9 | (after the final) Answer language set in code: the question's language / an explicit request; language mismatch 1 → 0, correctness 0.97 unchanged | ✅ 6 November 2026 | [phase-9/REPORT.md](phase-9/REPORT.md) |
| 10 | (after the final) Turkish query + search with an English translation: correct 0.99, Turkish 12/12; Turkish TTFT +9 s (p95 75 ❌, TTFT p50 17.1 ❌). Rolled back by the user's decision, code at Phase 9 | ↩ 6 November 2026 | [phase-10/REPORT.md](phase-10/REPORT.md) |

The original phase plan is at the end of [phase-1/REPORT.md](phase-1/REPORT.md#5-phase-plan). Details of the steps:
[`../IMPROVEMENTS.md`](../IMPROVEMENTS.md).
