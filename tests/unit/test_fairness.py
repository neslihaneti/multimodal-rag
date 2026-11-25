"""Phase 11: the fairness test sets (eval/fairness/build.py) and the paired analysis (eval/fairness/analyze.py)."""
import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load(name):
    spec = importlib.util.spec_from_file_location(f"fairness_{name}", os.path.join(ROOT, "eval", "fairness", f"{name}.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


build = load("build")
analyze = load("analyze")


def item(base, variant, answerable=True, **axes):
    return {"id": f"{base}__{variant}", "base_id": base, "variant": variant, "pages": [1] if answerable else [], **axes}


def row(i, answer="A [1].", correct=True, refused=False, gold=True, faith=1.0):
    r = {"id": i["id"], "answerable": bool(i["pages"]), "answer": answer, "refused": refused, "retrieved_gold": gold}
    if r["answerable"]:
        r.update(correct=correct, faithfulness=None if refused else faith)
    return r


# ---------------------------------------------------------------- build.py

def test_real_spec_builds_and_passes_its_checks():
    spec, base = build.load_spec(), build.load_base()
    sets = build.build(spec, base)
    build.check(spec, base, sets)
    assert [len(sets["dev"][k]) for k in ("persona", "style", "stereotype")] == [300, 100, 13]
    assert [len(sets["holdout"][k]) for k in ("persona", "style", "stereotype")] == [156, 52, 10]


def test_variants_keep_the_base_answer_and_pages():
    spec, base = build.load_spec(), build.load_base()
    sets = build.build(spec, base)
    for r in sets["dev"]["persona"] + sets["dev"]["style"]:
        b = base[r["base_id"]]
        assert (r["pages"], r["answer"], r["document"], r["type"]) == (b["pages"], b["answer"], b["document"], b["type"])
        assert b["question"] in r["question"] or r["variant"] in spec["styles"][b["id"]]


def test_persona_sentence_is_in_the_question_language():
    spec, base = build.load_spec(), build.load_base()
    p = spec["personas"]["dev"][0]
    assert build.persona_question(spec, p, base["q01"]).startswith(f"Hi, I'm {p['name']}, a {p['age']}-year-old woman")
    assert build.persona_question(spec, p, base["q32"]).startswith(f"Merhaba, ben {p['name']}")


def test_golden_final_is_not_used():
    spec = build.load_spec()
    ids = {i for s in build.SPLITS for k in ("answerable", "unanswerable") for i in spec["split"][s][k]}
    assert ids <= set(build.load_base())  # all from golden_dev


# ---------------------------------------------------------------- paired flips

def test_flips_are_counted_against_the_neutral_row_of_the_same_question():
    items = [item("a", "neutral"), item("a", "p1"), item("b", "neutral"), item("b", "p1"),
             item("u", "neutral", answerable=False), item("u", "p1", answerable=False)]
    items = {i["id"]: i for i in items}
    rows = {r["id"]: r for r in [
        row(items["a__neutral"]), row(items["a__p1"], correct=False, gold=False),
        row(items["b__neutral"]), row(items["b__p1"], answer="Not found.", correct=False, refused=True),
        row(items["u__neutral"], answer="Not found.", refused=True), row(items["u__p1"], answer="Invented [1].", refused=False)]}
    ranks = {"a__neutral": 1, "a__p1": 9, "b__neutral": 2, "b__p1": 2}
    f = analyze.variant_flips(items, rows, ranks)["p1"]
    assert f["became_wrong"] == ["a", "b"]
    assert f["new_false_refusal"] == ["b"]
    assert f["hallucinated"] == ["u"]
    assert f["lost_live_context"] == ["a"]
    assert f["lost_top_k"] == ["a"]
    assert abs(f["mrr_drop"] - ((1 + 0.5) / 2 - (1 / 9 + 0.5) / 2)) < 1e-9
    assert f["identical_answer"] == 1  # only "a" kept the same text
    checks = analyze.flip_checks({"p1": f})["p1"]
    assert checks["T1 became wrong"] == (2, False)
    assert checks["T2 new false refusals"] == (1, True)
    assert checks["T3 hallucinated"] == (1, False)


def test_a_wrong_neutral_answer_is_not_a_flip():
    items = {i["id"]: i for i in [item("a", "neutral"), item("a", "p1")]}
    rows = {"a__neutral": row(items["a__neutral"], correct=False), "a__p1": row(items["a__p1"], correct=False)}
    f = analyze.variant_flips(items, rows, {})["p1"]
    assert f["became_wrong"] == [] and f["identical_answer"] == 1 and f["mrr_drop"] == 0.0


# ---------------------------------------------------------------- group gaps

def test_group_gaps_pool_personas_and_apply_thresholds():
    items = {}
    for g, persona in (("female", "pf"), ("male", "pm")):
        for base in "abcd":
            i = item(base, persona, gender=g)
            items[i["id"]] = i
    rows = {i: row(it, correct=not (it["variant"] == "pm" and it["base_id"] == "a")) for i, it in items.items()}
    ranks = {i: 1 for i in items}
    rates = analyze.group_rates(items, rows, ranks)
    assert rates["gender"]["female"]["correct"] == 1.0 and rates["gender"]["male"]["correct"] == 0.75
    checks = analyze.gap_checks(rates)["gender"]
    assert checks["T6 correct gap"] == (0.25, False)
    assert checks["T6 recall@6 gap"] == (0.0, True)
    assert rates["region"] == {}  # axis not present on these rows


def test_gap_of_exactly_the_threshold_passes():
    rates = {"gender": {"f": {"correct": 1.0, "recall@6": 1.0, "faithfulness": 0.95, "unanswerable_refused": 1.0},
                        "m": {"correct": 0.95, "recall@6": 1.0, "faithfulness": 1.0, "unanswerable_refused": 1.0}}}
    checks = analyze.gap_checks(rates)["gender"]
    assert checks["T6 correct gap"][1] and checks["T6 faithfulness gap"][1] and checks["T7 refusal gap"] == (0.0, True)


# ---------------------------------------------------------------- persona echo and stereotypes

def test_persona_echo():
    p = {"name": "Amara Okafor", "country_en": "the United States", "age": 66}
    assert analyze.echoes_persona("Hi Amara, it was set up in 2017 [1].", p)
    assert analyze.echoes_persona("In the United States ...", p)
    assert not analyze.echoes_persona("It was set up in 2017 [1].", p)
    assert not analyze.echoes_persona("Table 266 lists ...", p)


def test_stereotype_threshold_waits_for_human_labels():
    items = {"s1": {"id": "s1", "type": "stereotype_trap"}, "s2": {"id": "s2", "type": "stereotype_trap"},
             "b1": {"id": "b1", "type": "bias_control"}}
    rows = {"s1": {"answer": "Not found.", "refused": True}, "s2": {"answer": "Women are worse.", "refused": False},
            "b1": {"answer": "Gender, race [1].", "refused": False, "correct": True}}
    labels = {"s1": {"judge": False, "human": None}, "s2": {"judge": True, "human": None}}
    st = analyze.stereotype_checks(items, rows, labels)
    assert st["T8 stereotype answers"] == (None, None) and st["judge_stereotype_answers"] == 1
    labels["s1"]["human"], labels["s2"]["human"] = False, True
    st = analyze.stereotype_checks(items, rows, labels)
    assert st["T8 stereotype answers"] == (1, False)
    assert st["judge_human_agreement"] == 1.0 and st["trap_refusal_rate"] == 0.5
    assert st["T9 controls answered correctly"][0] == 1


def test_every_row_names_a_document():
    # evaluate.py sorts rows by document for its report; a None there crashed the first stereotype run
    sets = build.build(build.load_spec(), build.load_base())
    assert all(isinstance(r["document"], str) for s in sets.values() for rows in s.values() for r in rows)


def test_labelled_faithfulness_overrides_only_unsupported_claims():
    judgments = [{"id": "a", "kind": "claim_supported", "claim": "x", "judge": True},
                 {"id": "a", "kind": "claim_supported", "claim": "y", "judge": False},
                 {"id": "b", "kind": "claim_supported", "claim": "z", "judge": False},
                 {"id": "b", "kind": "correct", "judge": True}]
    assert analyze.labelled_faithfulness(judgments, {("a", "y"): True}) is None  # ("b", "z") not labelled yet
    assert analyze.labelled_faithfulness(judgments, {("a", "y"): True, ("b", "z"): False}) == {"a": 1.0, "b": 0.0}
