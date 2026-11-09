# Phase 5b — Repetition blocking in answers (sweep) + sentence deduplication in the judge

Date: 5 November 2026. User approval and conditions:

- The sweep must include number, citation and refusal questions besides the loop questions.
- `no_repeat_ngram_size` 8–12 must also be tried.
- The judge change must be reflected in `judge_sha256`.
- Measured on the same index as Phase 5.

Sweep data: `phase5b_sweep.json`, `phase5b-sweep.log`.

## Code

- `rag.ANSWER_OPTIONS`: goes through `model.generate(options=…)` to answer generation only. Search decisions and the
  judge are not affected.
- `no_repeat.AnswerNoRepeatNGram`: blocks only the answer's own n-grams. transformers' `no_repeat_ngram_size` also
  counts the prompt in a decoder-only model, so it also forbids copying a long phrase from the source verbatim. Unit
  test: `tests/unit/test_answer_no_repeat.py`.
- Judge:
  - `answer_sentences` counts a repeated sentence as one claim and merges its citations (test added).
  - `judge_sha256` now also covers the source code of the `answer_sentences` and `faithfulness` functions. Before, it
    covered only the prompts and the regex; a code change would not have changed the hash.

## Sweep (Phase 5 index, search done once and cached, deterministic generation)

Questions:

- Loop questions: q33, q36, q37, d2q10.
- Number and citation questions: q01, d2q03, d2q05, q09, d3q20.
- Refusal: q43.
- Extra round: q42 and q45. In Phase 5 these two added `[1]…[6]` to the refusal sentence.

| Variant | Loop | Number/citation questions | q42, q45 |
|---|---|---|---|
| base (no setting) | none | 5/5 correct | `[1][2][3][4][5][6]` |
| repetition_penalty 1.05 | none | correct | `[1]` |
| repetition_penalty 1.10 | none | correct | `[1]` |
| no_repeat_ngram_size 8 (HF) | none | **broken**: "JTC **2**/SC42 … **2020**", "**0.7** MeV", "CODATA **1973**, 2018, 2022" | no citation, a refusal repeating the question |
| no_repeat_ngram_size 12 (HF) | none | **broken**: "SC**41**", "× **0-19** C", "theNewtonian" | `[1]…[6]` |
| answer-only 8 | **q36: 3,636 characters**, 178 s | correct | `[1]…[6]` |
| answer-only 12 | q36 842 characters (base 503) | correct | `[1]…[6]` |

Observations:

1. **The loops disappeared by themselves in Phase 5.** With short chunks none of them loops in base either.
2. **The user's warning was confirmed, and worse than expected.** Because HF's n-gram block forbids copying numbers and
   terms from the source, the model slides to the nearest "allowed" token: 2017 → 2020, 0.5 → 0.7 MeV. This is a
   silent factual error; in the metrics it looks "cited and fluent" instead of "wrong".
3. **The answer-only n-gram block** does not break the loop, it changes its form: q36 repeated the same content in
   different words over 3.6 thousand characters. The sentence-repetition counter shows 0 for it.
4. **The repetition penalty** did not break numbers on these 12 questions. It reduced the citation in the refusal
   sentence to `[1]` but not to zero.

## Decision

- **Generation: no setting added (base).** The loop no longer occurs; every added setting brings risk without a
  measurable benefit. `ANSWER_OPTIONS = {}` stays; the plumbing can be used later.
- **Judge: deduplication kept.** No Phase 5 answer has a repeated sentence, so the metrics are the same as Phase 5. The
  full measurement (~70 min) was skipped; generation is deterministic and did not change.
- **Open problem: the citation in the refusal sentence (0.15).** No generation setting solved it. A proposal was made
  to the user: when a refusal is detected in code, replace the answer with a fixed refusal sentence in the question's
  language. This also closes the "English refusal to a Turkish question" limitation of Phase 3c.
