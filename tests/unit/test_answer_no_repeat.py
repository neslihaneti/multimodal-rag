"""The answer n-gram block bans repeats inside the answer only, never copying from the prompt."""
import pytest

torch = pytest.importorskip("torch")
no_repeat = pytest.importorskip("no_repeat")


def banned(ids, size, prompt_length):
    scores = torch.zeros(1, 10)
    no_repeat.AnswerNoRepeatNGram(size, prompt_length)(torch.tensor([ids]), scores)
    return {i for i in range(10) if scores[0, i] == -float("inf")}


def test_a_repeated_answer_ngram_is_banned():
    # answer 1 2 3 1 2: "1 2" was followed by 3 before, so 3 is banned now
    assert banned([7, 7, 1, 2, 3, 1, 2], size=3, prompt_length=2) == {3}


def test_ngrams_of_the_prompt_do_not_count():
    # the prompt has "1 2 3", the answer so far is "1 2": copying the prompt is allowed
    assert banned([1, 2, 3, 1, 2], size=3, prompt_length=3) == set()
