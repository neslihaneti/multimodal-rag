# Phase 4 — Keyword search: filler words + length normalisation

Date: 4 November 2026. In Phase 1b keyword search was almost useless (R@6 0.29) and RRF disturbed the vector ranking
(hybrid R@1 0.41 < vector 0.81). There were two causes. The query ORed every word, including fillers such as
"what/the/does…". And `ts_rank_cd` favoured long chunks in multi-term OR queries.

## Change (`db.py`)

- `STOPWORDS`: English and Turkish question/filler words (`what, the, does, …, nedir, hangi, için, …`) are dropped from the query.
- `ts_rank_cd(tsv, q)` → `ts_rank(tsv, q, 1)`. Normalisation 1 divides the score by `1 + log(chunk length)`. Both
  `keyword_search` and the sparse CTE of `hybrid_search` use the same ranking.
- Tests: `test_keyword_query_drops_question_words`. A Turkish test checks that "nedir" is dropped. The integration test
  (D "zebra zebra zebra" > C) also passes with normalisation. Unit + integration 53 tests passed.

## Result (`reports/20261104-1515-retrieval.md`, 69 answerable questions)

| Method | Phase 1b R@1 / R@6 / MRR | **Phase 4 R@1 / R@6 / MRR** |
|---|---|---|
| vector | 0.81 / 0.94 / 0.867 | 0.81 / 0.94 / 0.867 (same) |
| keyword | 0.07 / 0.29 / 0.169 | **0.51 / 0.86 / 0.655** |
| hybrid (RRF) | 0.41 / 0.83 / 0.548 | **0.71 / 0.90 / 0.792** |
| vector + reranker | 0.81 / 0.96 / 0.879 | 0.81 / 0.96 / 0.879 (same) |
| **hybrid + reranker (live)** | 0.81 / 0.96 / 0.880 | **0.81 / 0.96 / 0.879** |

| Document (n), live R@6 / MRR | Phase 1b | Phase 4 |
|---|---|---|
| doc1 (37) | 1.00 / 0.94 | 0.97 / 0.93 |
| doc2 (12) | 0.75 / 0.55 | **0.83 / 0.56** |
| doc3 sample (20) | 1.00 / 0.97 | 1.00 / 0.97 |

5 questions whose rank changed in the live system:

| Question | Phase 1b rank | Phase 4 rank | |
|---|---|---|---|
| d2q03 (G constant, table) | 29 | **6** | entered the top 6 |
| q24 (back-to-back, paraphrase) | 6 | 7 | left the top 6 |
| q17 | 2 | 3 | |
| d2q10 | 14 | 15 | |
| d2q12 | 7 | 8 | |

Findings:

- **Keyword search now works** (R@6 0.29 → 0.86), and RRF no longer disturbs the vector ranking (hybrid R@1 0.41 → 0.71).
  The 0.86 predicted by the scratchpad experiment held.
- **Net effect on the live system is neutral.** The reranker re-orders all 40 candidates; the candidates were mostly
  the same already. One question was gained (d2q03), one lost (q24). The regression rule (a drop on more than one
  question) was not violated.
- The change was kept anyway. The candidate set before the reranker is now more robust for exact terms and codes. RRF's
  own ranking also became meaningful: this matters if the reranker is shortened or skipped later (Phase 6 latency).
- Turkish keyword search is still weak (R@6 0.50): the `simple` dictionary does no stemming ("zehirlenmesi" ≠
  "zehirlenme"). Vector search already carries Turkish (1.00), so no separate phase was opened for now.
- The remaining weakness of doc2 (d2q10 at 15, d2q11, d2q12) comes from long LaTeX/table chunks → Phase 5.

## Next

The answer measurement of Phase 3b (refusal sentence without citations) runs with this code; then Phase 5 chunking.
