import db


def test_keyword_query_ors_unique_words_longer_than_two_letters():
    assert db.keyword_query("Robustness score? Robustness of AI?") == "robustness | score"


def test_keyword_query_drops_question_words():
    assert db.keyword_query("What is the F1-score? Which ones does it have?") == "score | ones"


def test_keyword_query_keeps_turkish_letters():
    assert db.keyword_query("Veri zehirlenmesi nedir?") == "veri | zehirlenmesi"


def test_keyword_query_is_empty_for_short_words():
    assert db.keyword_query("is AI ok?") == ""


def test_to_vector_formats_pgvector_literal():
    assert db.to_vector([0.5, -1, 0.1234567]) == "[0.500000,-1.000000,0.123457]"
