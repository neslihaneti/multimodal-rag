# Phase 2 — Stability: crash on long prompts → token budget

Date: 4 November 2026. The answer evaluation of Phase 1b stopped twice at q43 with a process crash (segfault,
`eager_attention_forward`, a 13,298-token prompt). This phase was taken before the citation rate because the crash
also affected the user interface. Detailed diagnosis: [CHALLENGES.md Z10](../CHALLENGES.md); memory problem: Z11.

## Goal

The 82-question development set finishes without crashing; quality metrics are not worse than Phase 1b.

## Change

| File | What |
|---|---|
| `model.py` | Stayed with eager attention on MPS (sdpa produces garbage from ~9.5k tokens on and corrupts later calls too). `MAX_INPUT_TOKENS = 10000`: a prompt above it is refused with a `ValueError` instead of crashing. `count_tokens()`. `torch.mps.empty_cache()` after every `generate` (Z11). |
| `rag.py` | `PROMPT_TOKEN_BUDGET = 9000`. `fit_prompt`: first the lowest-ranked chunks are dropped (down to at least 3), then page images, finally chunks again. The search-decision prompt is trimmed to the same budget. |
| tests | `tests/unit/test_prompt_budget.py` (3), `test_decision_prompt_is_kept_under_the_token_budget`. 43 unit tests in total; all 52 tests passed. |

## Result (`reports/20261104-1330-answers.md`, 82 questions)

The measurement finished in two parts. The first run went up to question 81 and stopped at d3u03 with an **MPS
out-of-memory error**: GBs of eager attention buffers were piling up in the cache. `empty_cache` was added and the last
question was completed with `--resume`. Check: since the prompt did not change (same prompt_sha256), both parts
measure the same system.

| Metric | Target | Phase 1b (first 42, doc1) | **Phase 2 (82)** | Phase 2, doc1 only (45) |
|---|---|---|---|---|
| completed questions | 82 | 42 (crashed) | **82** ✅ | 45 |
| answer_correctness | ≥ 0.85 | 0.92 | **0.91** ✅ | 0.92 |
| faithfulness | ≥ 0.92 | 0.95 | **0.93** ✅ | 0.95 |
| citation_precision | ≥ 0.80 | — | **0.83** ✅ | — |
| cites_expected_page | ≥ 0.85 | 0.70 | **0.62** ❌ | 0.70 |
| answers_without_citation | ≤ 0.05 | 0.30 | **0.30** ❌ | 0.30 |
| false_refusals | ≤ 0.05 | 0.00 | **0.00** ✅ | — |
| unanswerable_refused | ≥ 0.90 | 1.00 (n=5) | **0.92** ✅ (n=13) | 0.88 |
| latency p50 / p95 | ≤ 30 / ≤ 60 s | 41.7 / 76.4 | **49.9 / 97.8** ❌ | — |

| Document (n) | correct | faithfulness | cites expected page | without citation | unanswerable refused |
|---|---|---|---|---|---|
| doc1 (45) | 0.92 | 0.95 | 0.70 | 0.30 | 0.88 |
| doc2 (14) | 0.83 | 0.85 | **0.33** | 0.25 | 1.00 |
| doc3 sample (23) | 0.95 | 0.92 | 0.65 | 0.35 | 1.00 |

Findings:

- **The crash is fixed.** q43 is now correctly refused (122 s). The doc1 results are at the same level as Phase 1b
  (0.92 / 0.95 / 0.70 / 0.30), so the budget did not lower quality on doc1.
- **doc2 is the weak link.** Only 0.33 of its citations point to the correct page; 2 of the 6 wrong answers are among
  the 14 doc2 questions (d2q10, d2q12). This matches the doc2 weakness in retrieval (R@6 0.75): when huge chunks are
  trimmed by the budget, the gold page can be trimmed too → Phase 5 (chunking).
- **Answers without citation 0.30** (the biggest gap). Example: d2q06 is correct but uncited ("The 2022 least-squares
  adjustment used 133 input data and 79 adjusted constants."). The model skips the citation in short one-sentence
  answers → Phase 3.
- **q44 (Kubernetes pod, unanswerable):** the model first gave an invented sentence cited to doc2, then said "metinlerde
  açıklanmamıştır". The refusal regex does not recognise "açıklanmamış" and the answer is partly invented. A separate
  improvement candidate (refusal format); Phase 3's prompt may also affect it, so that is measured first.
- **Latency went up** (p95 97.8 s): doc2/doc3 questions come with long prompts and eager attention is slow. Phase 6.
- The 6 wrong answers: q24, q31, q35 (doc1, since Phase 1), d2q10, d2q12, d3q12; plus the unrefused unanswerable q44.

## Next phase

Phase 3 — citation rate: the instruction "end every sentence with a citation, including one-sentence answers" in ANSWER_PROMPT.
