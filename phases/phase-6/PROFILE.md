# Phase 6 preparation: latency profile (5 November 2026, full index)

Baseline: p50 31.4 s, p95 63.5 s. Linear fit: time ≈ 10.5 + 0.028 × characters + 16.5 × search rounds (s).
72 of the 82 questions finish in one round (median 30.8 s).

Step-by-step measurement (`scratchpad/profile6.py`, 6 questions):

| question | total | embed+db | rerank (total) | decision `generate` (tokens) | answer `generate` (tokens, output chars) |
|---|---|---|---|---|---|
| q01 | 26.7 | 0.07 | 3.1 | 2.5 s (1,790) | **20.9 s** (5,294, 65) |
| q12 | 21.4 | 0.06 | 2.4 | 1.5 s (1,161) | **17.3 s** (4,665, 120) |
| d3q09 | 27.3 | 0.07 | 3.2 | 2.4 s (1,748) | **21.5 s** (5,413, 111) |
| q31 | 53.5 | 0.07 | 2.7 | 1.3 s (994) | **49.4 s** (4,498, 819) |
| d2q05 | 53.7 | 0.07 | 5.0 | 8.2 s (4,094) | **40.3 s** (7,957, 107) |
| q43 | 65.5 | 0.15 | 10.1 | 2 × 10.2 s (4,252) | **34.8 s** (8,116, 72) |

- **Bottleneck: processing the answer prompt (prefill).**
  - Even a 65-character answer takes 21 s.
  - With the same chunks, the decision prompt without images is ~1,800 tokens; the answer prompt is ~5,300 tokens.
    3 page images add ~3,500 tokens (~1,170 per image).
  - With eager/blocked attention the time grows faster than linearly with tokens: 1.8k tokens 2.5 s, 4.2k tokens 10 s.
- **Long answers:** ~30 s of decoding for 819 characters in q31.
- **Extra search rounds:** each adds a decision call (2–10 s) and a rerank.
