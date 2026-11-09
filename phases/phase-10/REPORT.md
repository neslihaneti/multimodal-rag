# Phase 10: also search Turkish queries with an English translation (after the final holdout, approved by the user)

After the final holdout; measured on the dev set only.

**Problem:** a question with only a Turkish term, such as "Kavram kayması nedir?", did not find the relevant passage in
the English documents (rerank 0.0 → refusal).

**Change (`rag.py`):** `english_query()` translates a Turkish query into English with the model (`TRANSLATE_PROMPT`);
in the first round both queries are searched and the pools are merged; `rank()` gives each chunk the higher rerank score
of the two queries. The translation appears among the queries in the UI's "Search details". 3 unit tests; unit +
integration 92 passed. By hand: "Kavram kayması nedir?" 0.0 → 0.99 and a correct Turkish answer.

## Dev measurement (82 questions)

| | Phase 9 | Phase 10 |
|---|---|---|
| answer_correctness | 0.97 | **0.99** (only q24 wrong; d2q12 fixed) |
| Turkish: correct / gold page cited / gold page retrieved | 11 / 11 / 11 (of 12) | **12 / 12 / 12** |
| faithfulness (judge) | 0.92 | 0.92 |
| citation_precision / cites_expected_page | 0.86 / 0.91 | 0.88 / 0.93 |
| refusal metrics | 0.00 / 0.00 / 1.00 / 0.00 | same |
| latency p50 / p95 | 20.2 / 58.6 | 24.2 / **75.3** ❌ |
| TTFT p50 / p95 | 13.4 / 34.1 | **17.1** ❌ / 46.7 |

**Latency breakdown:**
- 67 English questions: their answers are **identical** to Phase 9 (the code path did not change), yet the median went
  19.3 → 22.2 s, and d2q09 took +47 s for the same 93-character answer. This increase comes from the measurement
  environment (memory pressure/MPS), not the code.
- 15 Turkish questions: median TTFT 14.2 → 23.3 s (real). Profile (5 questions): translation 0.6–1.3 s, each
  `retrieve` (rerank of 40 candidates) 2–3.5 s; `agentic_search` 7–11 s (previously ~4–5).
- **Proposal (awaiting the user's approval):** merge the candidates of both queries and rerank them once, against the
  English translation only (instead of two separate reranks of 40 plus double scoring). Expected extra cost ~1–2 s.
  Then measure the dev set again.

## Decision (user, 6 November 2026)

The code was **rolled back to Phase 9** (translation removed; the answer-language fix kept). The Phase 10 code is kept
as `phases/phase-10/rag_phase10.py`. Unit + integration 89 passed; `prompt_sha256` 2856d18117b9 = the Phase 9 report.
