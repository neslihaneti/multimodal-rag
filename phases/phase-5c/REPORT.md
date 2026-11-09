# Phase 5c — Fixed refusal sentence (in the question's language, without citations)

Date: 5 November 2026. User approval: the proposal and the success-criteria update together.

## Problem

- In Phase 5, q42 and q45 added `[1]…[6]` to the refusal sentence (`unanswerable_with_citation` 0.15).
- None of the generation settings of Phase 5b brought this to zero.
- Another limitation has been open since Phase 3c: a Turkish question gets an English refusal (q44, q45, d3u03).

## Change (`rag.py`)

- `is_refusal(text)`: counts as a refusal if the refusal phrase (`NOT_FOUND`) is in the **first sentence** of the answer.
  - If the refusal phrase follows a partial answer ("X is 5 [1]. Y is not mentioned."), the text is not changed.
  - So a correct partial answer is not deleted.
- When a refusal is detected, `answer` becomes the fixed sentence in the question's language:
  - Turkish: "Belgelerde bu konuda bilgi yok."
  - English: "The documents do not contain information about this."
- The model's text is kept in the `raw_answer` field.
- `question_language`: `tr` if there is a Turkish letter or a Turkish question/conjunction word.
  - `re.IGNORECASE` is not used: in Python, with this flag `ı` matches both `i` and `I`, and every English question
    looked Turkish.
- "bulunmuyor" and "yer almıyor" were added to the `NOT_FOUND` pattern.

## Measurement and report (`evaluate.py`)

- `unanswerable_with_citation` is now measured on the answer the system returns (SUCCESS_CRITERIA.md updated).
- The rate in the model's raw text is reported for information in the `raw_unanswerable_with_citation` row.
- `raw_answer` and `raw_cited` were added to each row.
- `prompt_sha256` also covers the refusal sentences, the regexes and the code of `is_refusal`.

## Tests

Unit tests (`tests/unit/test_answer_citations.py`):

- English and Turkish refusals become the fixed sentence and show no sources. Cases tested:
  - a refusal with citations,
  - an English refusal to a Turkish question,
  - a refusal plus extra explanation.
- If the refusal phrase follows a partial answer, the text is kept.
- Both fixed sentences are recognised by `NOT_FOUND` and `is_refusal`.
- `question_language` matches the golden `lang` field on 82 of the 82 development questions.

E2E tests (real model):

- `tests/e2e/test_refusal_judge.py` — the judge's `REFUSAL_PROMPT`:
  - counted the fixed sentence as a refusal on 13 of 13 unanswerable questions (100%),
  - did not count two real answers (TR and EN) as refusals,
  - result: 15/15 passed.
- `tests/e2e/test_ui.py::test_turkish_refusal_is_in_turkish_without_sources`: the UI shows the Turkish refusal and no
  sources. The UI tests are run after the baseline.

## Offline effect (simulation on the Phase 5 answers)

- 13 of the 13 unanswerable questions become the fixed sentence; none of the 69 answerable questions changes.
- `unanswerable_with_citation`: 0.15 → 0.00. 0.15 remains in the raw text.
- Turkish refusals: q44, q45 and d3u03 are now in Turkish.

The real measurement is done in the new baseline after the whole of doc3 is indexed.
