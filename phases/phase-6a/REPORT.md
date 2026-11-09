# Phase 6a — Page images 1280 → 896 pixels

Date: 5 November 2026. User approval: Phase 6 order 6a → 6b → (if needed) 6c.

- Sweep: `sweep6a.json` (23 questions × 1280/1024/896).
- Full measurement: `reports/20261105-1206-answers*`.
- Golden: with the extra doc3 pages (sha 6cab820cb2f0). The baseline was rescored with this golden: cites 0.913,
  precision 0.848.

## Sweep (all figure and table questions + number, Turkish, refusal and two-page questions)

| size | correct | gold page cited | p50 | mean | prompt tokens (median) |
|---|---|---|---|---|---|
| 1280 | 22/22 | 19 | 32.3 s | 37.1 s | 5,294 |
| 1024 | 22/22 | 19 | 23.6 s | 28.4 s | 4,142 |
| 896 | 22/22 | 20 | 20.9 s | 26.0 s | 3,614 |

The numbers in the figure and table answers were compared one by one; all are the same.

## Full measurement

| Metric | Baseline (new golden) | 6a | Pass |
|---|---|---|---|
| answer_correctness | 0.97 | **0.99** | ≥ 0.85 ✅ |
| faithfulness | 0.96 | **0.91** | ≥ 0.92 ❌ |
| citation_precision | 0.85 | 0.84 | ≥ 0.80 ✅ |
| cites_expected_page | 0.91 | 0.90 | ≥ 0.85 ✅ |
| unanswerable_refused / with_citation | 1.00 / 0.00 | 1.00 / 0.00 | ✅ |
| raw_unanswerable_with_citation | 0.15 | 0.00 | informational |
| p50 / p95 | 31.4 / 63.5 s | **22.5 / 55.7 s** | ≤ 30 / ≤ 60 ✅ |

**The latency target is met.** But faithfulness fell below the threshold. Breakdown of the drop:

- **The repetition loop came back: q36 and q37 (Turkish), ~3,100 characters, 140–190 s.**
  - Small effect on faithfulness: counting the loops at their baseline value gives 0.907 → 0.912.
  - They also make up the tail of p95.
- **The rest of the drop: the judge's claim decisions changed on reworded answers.**
  - The judge counted 16 claims as "unsupported".
  - By hand, many of them are clearly in the cited excerpt. Examples:
    - q07: the F1 formula described in words.
    - d3q08: "inverse-square law".
    - d3q14: "irregularities in the interplanetary medium".
    - d3q18: "prototype 1976".
  - The judge's calibrated agreement is 0.93; a swing of a few claims over 69 questions is within this range.
  - The decision is made with the user's labels:
    `reports/20261105-1206-answers-judgments-unsupported-to-label.jsonl` (16 rows).
- In d3q14 the answer said "about 43 km" (golden: 20 km). Not invented: p.108 says "At 1 MHz … not be more than 43 km
  in aperture". The document has two different figures.

Memory: during the full measurement the MPS leak in the generator (Z13) led to 64 GB and 10 GB of swap.

- Meanwhile the times of d2q02–d2q07 were inflated (d2q06 568 s). These rows were deleted and measured again in a clean process.
- With the guard lowered to 48 GB the run could not progress, because d2q11 alone reaches 50–58 GB. The limit was set to 66 GB.
- Lesson: the guard's limit must be above the peak of a single question.

## Decision (provisional)

896 was kept: the latency target is met and correctness went up. Faithfulness awaits the user's labels.

- If the labels confirm judge errors, 6a is final.
- If not, the options are 1024 pixels or a separate fix for the q36/q37 loop.

## Human labels (5 November 2026)

The user labelled the 16 claims the judge called "unsupported": 7 are supported (judge false negatives: q07, q20, q29
×2, d3q07, d3q08, d3q14), 9 are not (mostly cited to a neighbouring page; d2q09, d2q12). With the labels, per-question
faithfulness is **0.907 → 0.95** (≥ 0.92). **896 px is final.**
