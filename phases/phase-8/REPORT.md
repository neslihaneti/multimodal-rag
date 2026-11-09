# Phase 8: TTFT (Path 3 + Path 1)

User decision (5 November 2026): a refusal buffer of ~60 characters (Path 3) + fewer page images in the prompt
(Path 1); no sdpa. If TTFT p50 drops into the 11–14 s band, the target becomes ≤ 15 s (Path 4).

## Path 3: `rag.FIRST_SENTENCE_MAX` 300 → 60

On the 82 raw answers of Phase 7, buffers of 40/50/60/80 characters give exactly the same refusal decisions as the
whole first sentence. Unit test added (`test_stream_starts_before_a_long_first_sentence_ends`); unit + integration 80 passed.

## Path 1: sweep of the number of images (`sweep8.json`, 22 figure/table/selected questions, buffer 60)

| Images | Correctness | Gold page cited | TTFT p50 / p95 | Total p50 |
|---|---|---|---|---|
| 3 | 22/22 | 20 | 13.5 / 25.7 | 16.6 |
| 2 | 22/22 | 20 | 11.5 / 23.1 | 14.6 |
| 1 | 22/22 | 20 | 10.6 / 22.0 | 12.4 |

## Full measurement (82 questions)

| | Phase 7 (3 images, buffer 300) | Phase 8 (1 image) | **Phase 8b (2 images)** |
|---|---|---|---|
| answer_correctness | 0.99 | 0.96 | **0.97** |
| faithfulness (judge) | 0.91 | 0.93 | 0.90 |
| citation_precision | 0.84 | 0.86 | 0.84 |
| cites_expected_page | 0.90 | 0.90 | 0.90 |
| answers_without_citation / false_refusals | 0.00 / 0.00 | 0.00 / 0.00 | 0.00 / 0.00 |
| unanswerable_refused / with_citation | 1.00 / 0.00 | 1.00 / 0.00 | 1.00 / 0.00 |
| latency p50 / p95 | 19.9 / 56.1 | 14.6 / 37.7 | 17.8 / 52.4 |
| TTFT p50 / p95 | 17.7 / 37.5 | 10.8 / 31.1 | **12.9 / 36.4** |

- 1 image: q24 and q29 are newly wrong (q24 invents "test cases or inputs"; q29 loops over the table of contents and
  cites non-existent excerpts [7]–[11]). Two questions > the regression limit. A separate run is deterministic:
  1 image both ❌, 2 images only q24 ❌, 3 images both ✅. → **`MAX_PAGE_IMAGES = 2`** (the approved Path 1 "1–2 images").
- 8b: the wrong answers are q24 (new, 1 question = within the limit) and d2q12 (wrong since earlier). TTFT p50 12.9 →
  the SUCCESS_CRITERIA TTFT p50 target was set to ≤ 15 s (Path 4, approved by the user).
- Faithfulness: judge 0.90 (< 0.92). Applying the human labels of 6a to the identical claims gives 0.914. 11 unlabelled
  "unsupported" claims: `reports/20261105-1812-answers-judgments-unsupported-to-label.jsonl` → **awaiting the user's
  labels**; the final holdout comes after this decision (the final set is run once; no setting may change afterwards).
