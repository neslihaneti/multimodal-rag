# Phase 7 — Streaming and TTFT measurement

Date: 5 November 2026. Report: `reports/20261105-1344-answers*`. Built on 6a + 6b.

## Change

- `model.generate_stream`: uses `TextIteratorStreamer` and a separate thread.
  - If the reader stops early, a `StoppingCriteria` stops the generation.
  - On an error the stream is closed, so the reader does not hang.
- `rag.answer_stream`: yields the answer piece by piece and the result dict at the end.
  - Nothing is shown before the first sentence ends (at most 300 characters are held back), because `is_refusal`
    looks at the first sentence.
  - On a refusal only the fixed sentence is shown and the generation is stopped.
  - `answer()` reads the same stream to the end; there is one code path.
- `app.py`: a spinner during the search, then `st.write_stream`.
- `evaluate.py`: measures `ttft_s` (the first text piece the user sees) and reports `p50_ttft_s` and `p95_ttft_s`.
- Side effect: since generation stops on refusals, `raw_answer` is the model's first sentence.
  `raw_unanswerable_with_citation` now measures citations in the first sentence.
- Tests: streaming, refusal replacement and stopping the generation, a short answer without a final period.
  Unit + integration 79 passed.

## Result

| Metric | 6b | 7 |
|---|---|---|
| Answers | — | **82/82 identical** |
| Quality | correct 0.99, faith 0.91, prec 0.84, cites 0.90 | same |
| p50 / p95 total | 21.6 / 56.8 s | 19.9 / 56.1 s (generation stops early on refusals) |
| **TTFT p50 / p95** | — | **17.7 / 37.5 s** (target ≤ 10) ❌ |

- In 46 of the 82 questions the first text appears only when the answer is finished. These are one-sentence answers;
  the buffer waits for the first sentence to end.
- Median TTFT on unanswerable questions is 32.7 s: extra search rounds, then the fixed sentence.
- Even the model's own first token arrives at 12–14 s (measured on 7 questions):
  - search and prompt preparation 4–5 s,
  - prefill 7–10 s.
- So the ≤ 10 s target is not met even without the buffer; prefill has to get shorter.

## Decision

Streaming was kept: the answer appears earlier in the UI and the answers did not change.

Options for TTFT were proposed to the user (awaiting approval):

1. fewer page images,
2. sdpa for short prompts (6c),
3. shrink the buffer to the first ~60 characters,
4. revise the target.

## UI e2e

With the streaming UI `tests/e2e` passed 25/25 (135 s), including the Turkish refusal sentence, refusal without
sources and prompt injection tests.
