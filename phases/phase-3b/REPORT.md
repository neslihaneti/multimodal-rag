# Phase 3b — Keep the refusal sentence without citations (failed, rolled back)

Date: 4 November 2026. Side effect of Phase 3: on unanswerable questions the model also wrote citations while refusing
(`unanswerable_with_citation` 0.38, target 0.00).

## Change

In ANSWER_PROMPT the refusal rule was moved before the citation rule and written as an exception: "If the documents do
not contain the answer, reply with only one sentence saying so; that sentence has no square brackets and no excerpt
numbers. Otherwise, end every sentence …". Phase 4's `db.py` change was also in place (its effect on the live system was
neutral in the retrieval measurement).

## Result (`reports/20261104-1643-answers.md`, old judge)

| Metric | Phase 3 | Phase 3b |
|---|---|---|
| unanswerable_with_citation | 0.38 | **0.38** (unchanged) |
| answer_correctness | 0.91 | 0.88 |
| faithfulness | 0.94 | 0.95 |
| cites_expected_page | 0.87 | 0.86 |
| answers_without_citation | 0.00 | 0.00 |
| unanswerable_refused | 1.00 | 1.00 |
| p50 / p95 | 43.7 / 84.2 | 41.9 / 88.8 |

- The 5 questions that cited while refusing did it in the same way again: "The provided documents do not contain
  information regarding … [1][2][3][4][5][6]." Neither the order of the rules nor writing the exception explicitly
  affected the 4B model.
- The correctness difference comes from 4 questions (q20, q26, q37 correct → wrong; q36 wrong → correct). In all of
  them the gold page was found in both runs and the answers are almost the same sentences. So the drop most likely
  comes from the judge's borderline decisions, not the prompt. Still, a net drop of 2 questions exceeded the
  regression threshold.

## Decision

The target was not met and a regression is suspected. **The prompt was rolled back to its Phase 3 state.** The next
attempt (Phase 3c) is chosen with a quick sweep instead of a full 82-question run (~80 min): on 13 unanswerable + 6
short-answer questions, search once and compare prompt variants (`scratchpad/refusal_sweep.py`, log
`phases/logs/phase-3c-sweep.log`).

Lesson: trying prompts one by one is expensive. Sweep on a cheap subset first and run the full measurement only with
the winning variant.
