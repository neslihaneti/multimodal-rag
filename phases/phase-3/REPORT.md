# Phase 3 — Citation rate: "end every sentence with a citation"

Date: 4 November 2026. Since Phase 1 the biggest gap was answers without citations (Phase 2: 0.30, target ≤ 0.05). The
model skipped the citation in short, one-sentence answers (e.g. d2q06 "…133 input data and 79 adjusted constants.").

## Change (one)

In `rag.ANSWER_PROMPT`, the sentence "Cite the excerpts you used with their numbers in square brackets, like [1] or
[2][3]." was replaced with:

> End every sentence of your answer with the numbers of the excerpts it is based on, in square brackets. This applies to
> short answers too: even a one-sentence answer must end with its citation, for example: "The device weighs 4 kg [2]."
> or "Both colours are allowed [1][3]."

The example sentences are deliberately neutral and do not appear in the documents. The first draft's example ("…set up
in 2017") leaked the answer to q01 and was dropped.

## Result (`reports/20261104-1503-answers.md`, 82 questions)

| Metric | Target | Phase 2 | **Phase 3** |
|---|---|---|---|
| answer_correctness | ≥ 0.85 | 0.91 | **0.91** ✅ |
| faithfulness | ≥ 0.92 | 0.93 | **0.94** ✅ |
| citation_precision | ≥ 0.80 | 0.83 | **0.84** ✅ |
| cites_expected_page | ≥ 0.85 | 0.62 | **0.87** ✅ |
| answers_without_citation | ≤ 0.05 | 0.30 | **0.00** ✅ |
| false_refusals | ≤ 0.05 | 0.00 | **0.00** ✅ |
| unanswerable_refused | ≥ 0.90 | 0.92 | **1.00** ✅ |
| unanswerable_with_citation | 0.00 | 0.08 | **0.38** ❌ (regression) |
| latency p50 / p95 | ≤ 30 / ≤ 60 s | 49.9 / 97.8 | **43.7 / 84.2** ❌ |

| Document (n) | correct | faithfulness | cites expected page | without citation | unanswerable refused |
|---|---|---|---|---|---|
| doc1 (45) | 0.95 | 0.95 | **1.00** | 0.00 | 1.00 |
| doc2 (14) | 0.75 | 0.86 | **0.33** | 0.00 | 1.00 |
| doc3 sample (23) | 0.95 | 0.98 | 0.95 | 0.00 | 1.00 |

Findings:

- **Target exceeded:** answers without citation 0.30 → 0.00, expected page cited 0.62 → 0.87. Correctness and
  faithfulness did not drop.
- **q44 fixed** (in Phase 2 it partly invented an answer instead of refusing); every unanswerable question was refused.
- **Side effect (regression):** on 5 of the 13 unanswerable questions the model also writes citations while refusing:
  "The provided documents do not contain information about the half-life of carbon-14 [1][2][3]." The "end every
  sentence with a citation" instruction overrode "do not use square brackets when refusing". The UI shows no sources
  (the `NOT_FOUND` regex drops the citations), but the raw-text metric measures it and the user sees `[1][2][3]` in the
  text → **Phase 3b**.
- **doc2 is still weak:** expected page cited 0.33, correctness 0.75. There were citations, but to the wrong page; the
  root cause is retrieval/chunking (Phase 4/5).
- **Judge strictness:** d2q08 "chi-squared 44.2" is correct but was counted wrong because the p-value of the expected
  answer was missing. True correctness is probably one question higher; to be measured with the calibration labels (user).
- Counted wrong: q24, q36, d2q08 (judge), d2q10, d2q12, d3q12.
- Latency dropped a little (no direct speed change; probably shorter answers and a single search round on q44).

## Next

- **Phase 3b:** keep the refusal sentence without citations by writing the refusal explicitly as an exception to the
  citation rule in the prompt.
- **Phase 4:** keyword search (code ready, retrieval being measured).
