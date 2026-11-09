# Phase 9: answer language (after the final holdout, at the user's request)

Done AFTER the final holdout; measured on the dev set only, the final set was not run again.

**Problem:** a Turkish question answered in English ("Yapay zeka tabanlı sistemlerde kavram kayması (concept drift)
nedir ve nasıl test edilir?"; dev q37, final f57). The language was left only to the prompt sentence "Answer in the
same language as the question"; the excerpts, instructions and English terms in the question pulled the 4B model
towards English.

**Change (`rag.py`):**
- `answer_language()`: if the question explicitly asks for a language ("İngilizce cevap ver", "Türkçe olarak açıkla",
  "answer in Turkish", "in English"), that language; otherwise `question_language()`. A language name used as a topic,
  as in "Türkçe keyword araması", does not count as a request.
- `without_language_request()`: the request sentence is removed from the search query (otherwise it disturbed the search).
- `ANSWER_PROMPT`: "Otherwise write the whole answer in {language}, even when the excerpts are in another language."
  The refusal sentence stayed fixed in English in the prompt (when a Turkish refusal was left free, the model wrote
  phrases such as "terimi bulunamadı" that `NOT_FOUND` does not recognise); the code translates it with `REFUSAL[language]`.
- 9 unit tests; unit + integration 89 passed. `prompt_sha256` covers the new functions.

## Dev measurement (82 questions)

| | Phase 8b | Phase 9 |
|---|---|---|
| answer_correctness | 0.97 | 0.97 (same wrong answers: q24, d2q12) |
| faithfulness (judge) | 0.90 | 0.92 |
| citation_precision / cites_expected_page | 0.84 / 0.90 | 0.86 / 0.91 |
| without citation / false refusals / refused / with citation | 0.00 / 0.00 / 1.00 / 0.00 | same |
| latency p50 / p95 | 17.8 / 52.4 | 20.2 / 58.6 |
| TTFT p50 / p95 | 12.9 / 36.4 | 13.4 / 34.1 |
| question language ≠ answer language | 1 (q37) | **0** |

- The p95 increase is the repetition loop moving to another question: d2q10 35 → 152 s (a 4,466-character loop),
  q32 124 → 59 s.
- Remaining finding: a question with only a Turkish term ("Kavram kayması nedir?") does not find the English passage
  (rerank 0.0) → Phase 10: English translation before the search (approved by the user).
