"""The judge (real model) must count rag.answer's fixed refusal sentences as refusals, in both languages
(phases/faz-5b): otherwise unanswerable_refused would drop although the system refused."""
import json
import os

import pytest

import evaluate
import rag

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
with open(os.path.join(ROOT, "eval", "golden_dev.jsonl"), encoding="utf-8") as f:
    UNANSWERABLE = [q for q in map(json.loads, filter(str.strip, f)) if not q["pages"]]


@pytest.mark.parametrize("item", UNANSWERABLE, ids=lambda q: q["id"])
def test_judge_recognises_the_fixed_refusal(item):
    sentence = rag.REFUSAL[rag.question_language(item["question"])]
    verdict = evaluate.ask(evaluate.REFUSAL_PROMPT.format(question=item["question"], given=sentence))
    assert verdict.upper().startswith("YES"), verdict


@pytest.mark.parametrize("question, given", [
    ("Yapay zeka tabanlı sistemlerde hangi test seviyeleri vardır?", "Girdi verisi testi, ML model testi, bileşen testi ve kabul testi [1]."),
    ("What does full neuron coverage require?", "Full neuron coverage requires every neuron to reach an activation value above zero [2]."),
])
def test_judge_does_not_count_an_answer_as_refusal(question, given):
    assert evaluate.ask(evaluate.REFUSAL_PROMPT.format(question=question, given=given)).upper().startswith("NO")
