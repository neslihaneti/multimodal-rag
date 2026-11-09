# Phase 3c — Refusal sentence: prompt variant sweep

Date: 4 November 2026. Phase 3b's prompt change had no effect in the full measurement (82 questions, ~80 min). In
this phase a quick sweep replaced the full measurement: 13 unanswerable questions plus 6–11 answerable ones to check
that citations are kept. For each question the search was done once and cached (`scratchpad/refusal_sweep.py`); the
variants only repeated the answer generation. Generation is deterministic (`do_sample=False`). Logs:
`phase-3c-sweep*.log`.

## Reliability of the sweep

In the sweep the Phase 3 prompt cited on the same 5 unanswerable questions as in the full measurement (q45, d2u01,
d3u01, d3u02, d3u03). So the quick sweep reproduces the full measurement exactly.

## Variants (replacing the sentence "If the documents do not contain the answer …")

| Variant | Text | Refusals with citation (13) | Turkish refusal to a Turkish question (q44, q45, d3u03) | Citations on answerable questions |
|---|---|---|---|---|
| faz3 | "… reply with one sentence saying so and do not use any square brackets." | 5 | 1/3 | kept |
| example | + `for example: "The documents do not contain information about this."` | 2 | 1/3 | kept |
| **sep_rule** | "… the rule about citations does not apply: reply only with "The documents do not contain information about this." in the language of the question, with no excerpt numbers." | **0** | 0/3 | kept (6/6) |
| sep_rule_tr | "… reply only with one sentence in the language of the question … such as "…" or "Belgelerde bu konuda bilgi yok."" | 2 | 2/3 | kept (11/11) |
| fixed2 | Two fixed sentences: English, and "Belgelerde bu konuda bilgi yok." for a Turkish question | 1 | 2/3 | kept (11/11) |

Observation: the 4B model drops the citation when it copies a **given fixed sentence**. Told to "write a sentence
like this", it builds a free sentence and the "end every sentence with a citation" rule comes back. When a fixed
sentence and a language instruction are given together, the fixed sentence overrides the language instruction.

## Decision

**sep_rule** was chosen and put into `rag.ANSWER_PROMPT`. Only this variant meets the success target
(`unanswerable_with_citation` 0.00). The refusal regex (`NOT_FOUND`) recognises this sentence (verified).

**Known limitation:** unanswerable questions asked in Turkish are refused in English ("The documents do not contain
information about this."). The Phase 3 prompt also refused 2 of 3 in English, so the problem is not new (1/3 → 0/3).
Answerable Turkish questions are still answered in Turkish. The success criteria have no language metric; this can be
solved in code later (e.g. a fixed sentence in the question's language once a refusal is detected).

The full measurement was done together with Phase J (new judge), so the full metrics of Phase 3c are in the Phase J report.
