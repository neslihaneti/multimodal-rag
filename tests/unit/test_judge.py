"""How evaluate.py turns an answer into claims and which excerpts the judge sees for each claim."""
import evaluate


def test_each_sentence_is_one_claim_with_its_citations():
    text = "The device weighs 4 kg [2]. Both colours are allowed [1][3]."
    assert evaluate.answer_sentences(text) == [("The device weighs 4 kg.", [2]), ("Both colours are allowed.", [1, 3])]


def test_a_one_sentence_answer_is_one_claim_and_nothing_is_added():
    assert evaluate.answer_sentences("The F1-score is 2PR/(P+R) [1].") == [("The F1-score is 2PR/(P+R).", [1])]


def test_decimals_and_a_citation_after_the_full_stop_stay_in_the_sentence():
    text = "The uncertainty is 1.6 × 10⁻¹⁰. [4] It was set in 2022 [2]."
    assert evaluate.answer_sentences(text) == [("The uncertainty is 1.6 × 10⁻¹⁰.", [4]), ("It was set in 2022.", [2])]


def test_an_abbreviation_inside_a_sentence_does_not_end_it():
    text = "The 15 ft Aerospace Corp. reflector is usable down to 1 mm [1]."
    assert evaluate.answer_sentences(text) == [("The 15 ft Aerospace Corp. reflector is usable down to 1 mm.", [1])]


def test_list_items_are_claims_without_their_bullets():
    text = "Levels:\n- Unit testing [1]\n- Acceptance testing [2]"
    assert evaluate.answer_sentences(text) == [("Levels:", []), ("Unit testing", [1]), ("Acceptance testing", [2])]


def chunk(i):
    return {"file_name": "doc1.pdf", "page_number": i, "heading": "", "content": f"excerpt number {i}", "context": ""}


def test_a_cited_claim_is_checked_against_its_cited_excerpts_only(monkeypatch):
    prompts = []
    monkeypatch.setattr(evaluate, "ask", lambda prompt, max_new_tokens=5: prompts.append(prompt) or "YES")
    judgments = []
    score = evaluate.faithfulness("A is true [2]. B is true.", [chunk(1), chunk(2), chunk(3)], judgments, {"id": "q", "question": "?"})
    assert score == 1.0
    assert "excerpt number 2" in prompts[0] and "excerpt number 1" not in prompts[0]
    # an uncited sentence is checked against every excerpt
    assert all(f"excerpt number {i}" in prompts[1] for i in (1, 2, 3))
    assert [j["cited"] for j in judgments] == [[2], []]


def test_repeated_sentences_count_once_with_merged_citations():
    text = "Back-to-back testing finds failures [1]. Back-to-back testing finds failures [2]. Back-to-back testing finds failures [1]."
    assert evaluate.answer_sentences(text) == [("Back-to-back testing finds failures.", [1, 2])]
