# Phase J — Judge fix (A–D) + the full measurement of Phase 3c

Date: 4 November 2026. Report: `reports/20261104-2303-answers.md` (82 questions, `prompt_sha256` 4af2b18c854a,
`judge_sha256` c2301e4f60d7).

## Changes

A–D, approved from the user's critique of the judge (5 points); no E:

- **A.** `CLAIMS_PROMPT` removed. Instead of the model inventing claims, the answer is split into sentences
  (`answer_sentences`, at most 8).
- **B.** Each sentence is checked only against the excerpts **it cites** (against all excerpts if it cites none). This
  reduces the "lost in the middle" problem of giving all six excerpts at once.
- **C.** `SUPPORT_PROMPT`: "the sentence and the context may be in different languages, compare the meaning".
- **D.** `CORRECTNESS_PROMPT`: golden details the question did not ask for may be missing; an extra correct detail is fine.

Other changes measured in the same run:

- The Phase 3c prompt (sep_rule).
- Blocked eager attention for memory (`attention.py`, CHALLENGES Z12): the mask registration was missing before this
  run and was fixed.

## Results

| Metric | Phase 3 | Phase J | Pass threshold |
|---|---|---|---|
| answer_correctness | 0.91 | **0.94** | ≥ 0.85 |
| faithfulness | 0.94 | 0.93 | ≥ 0.92 |
| cites_expected_page | 0.87 | 0.83 | ≥ 0.85 |
| citation_precision | 0.84 | 0.77 | ≥ 0.80 |
| answers_without_citation | 0.00 | 0.00 | ≤ 0.05 |
| unanswerable_refused | 1.00 | 1.00 | ≥ 0.90 |
| unanswerable_with_citation | 0.38 | **0.00** | 0.00 |
| false_refusals | 0.00 | 0.00 | ≤ 0.05 |
| p50 / p95 latency | 43.7 / 84.2 s | 39.6 / 103.9 s | ≤ 30 / ≤ 60 s |

- **unanswerable_with_citation 0.38 → 0.00:** Phase 3c's target also held in the full measurement. This metric does
  not depend on the judge.
- **Correctness:** the new judge now counts two unchanged answers (d2q08, d3q12) as correct. The user had given d3q12
  in point 1 of the critique as an example of "a golden detail the question did not ask for".
  - Turkish correctness dropped from 0.83 to 0.75; a single question (q33) was affected. q33's answer changed with the
    new prompt and gives a general definition instead of listing the test levels.
- **Latency:** the p95 increase comes from a **repetition loop** (the user's observation, confirmed). In the four
  slowest questions (q33, q36, q37, d2q10; 175–208 s, 41–67 s in Phase 3) the model writes the same sentence over and
  over: answers of 3–4.7 thousand characters, 21 of 25 sentences repeated in q37. My first draft attributed this to
  memory pressure; that was wrong.
  - On the judge side, `answer_sentences` does not deduplicate repeated sentences; q37's claim was counted 6 times.
  - A fix was proposed to the user: a repetition penalty or an n-gram block in generation, deduplication in the judge.
  - Latency is the subject of Phase 6.

## Regression: citation_precision 0.84 → 0.77, cites_expected_page 0.87 → 0.83

Most of the drop comes from doc2: precision 0.31 → 0.14, the expected page in 2 of 12 questions. But a review showed
that **the error is in the golden set**. Much of the information asked about in doc2 appears on two pages, and the
golden set lists only one. The model shows the other page (verified in the PDF text):

| Question | Golden page | Page shown by the model | Evidence (on that page) |
|---|---|---|---|
| d2q01 | 1 | 2 | "closing date of midnight, December 31, 2022" |
| d2q02 | 1 | 2 | "Committee on Data of the International Science Council … responsibility" |
| d2q04 | 45 | 44 | Table: "Vacuum magnetic permeability … 1.6 × 10−10" |
| d2q05 | 45 | 44 | Table: "elementary charge e 1.602 176 634 × 10−19 C Exact" |
| d2q06 | 52 | 5 | "133 input data and 79 adjusted constants … ν = 54" |
| d2q09 | 54 | 44 | Table: "Inverse fine-structure constant 137.035 999 177(21)" |
| d2q11 | 45 | 44 | Table: "Speed of light in vacuum c 299 792 458 m s−1 Exact" |

If these pages are added to the golden set, cites_expected_page becomes 0.93 (doc2 9/12) and citation_precision 0.87.
**Not applied:** changing the golden set after seeing the result is a decision, so it was put to the user for approval.

In doc1 precision dropped from 0.96 to 0.89. In four questions (q23, q24, q26, q31) the model cites a second page next
to the correct one; in q24 it cites only the wrong page. This may be a side effect of the new prompt.

## Judge reliability

The old labels (Phase 2 answers) could not be used in this run: almost all answers changed and only one row per kind
stayed identical. New stratified list:
`reports/20261104-2303-answers-judgments-to-label.jsonl` (90 rows: claim 17+13, correct 4+26, refusal 13+17).
The user labelled it on 5 November. Result of `python3 evaluate.py calibrate` (target: agreement ≥ 0.85, kappa ≥ 0.70):

| Kind | n | Agreement | Kappa | Phase 2 judge (kappa) |
|---|---|---|---|---|
| claim_supported | 30 | 0.93 | **0.86** | 0.61 |
| correct | 30 | 0.93 | 0.76 | 0.76 |
| refusal | 30 | 1.00 | 1.00 | 1.00 |

All three kinds pass the threshold. `claim_supported` went from 0.61 to 0.86: this was the problem A–D targeted.

**Golden correction:** the user approved and added the second pages of the 7 questions to `eval/golden_dev.jsonl` and
`eval/golden_dev_doc2.jsonl` themselves (valid from Phase 5 on).

## Memory (CHALLENGES Z11, Z12)

- After the mask fix, blocked attention uses ~9 GB for one question. The old eager attention took 50 GB on d2q12.
- Memory still accumulates by ~3 GB per question between generate calls. The run was completed with `mem_guard.sh`
  (70 GB) + `run_resume.sh` (restart with `--resume`); the process restarted twice. Generation is deterministic, so
  the results are not affected.
- The root cause of the accumulation is open work: since the UI server runs for a long time, it will be looked at in Phase 6.
