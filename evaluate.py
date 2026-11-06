"""Measure retrieval and answer quality on a golden question set. Every run writes a dated report to reports/.

Usage:
    python evaluate.py retrieval                    # compare vector, keyword, hybrid and reranked search
    python evaluate.py answers [--limit N]          # generate answers and judge them with the local model
    python evaluate.py answers --resume             # continue an interrupted answers run
    python evaluate.py label reports/<run>-judgments.jsonl       # stratified sample of judge decisions to label by hand
    python evaluate.py calibrate <labelled file>                 # agreement between the judge and your own labels

Each line of the golden set is one JSON object:
    {"id": "q01", "type": "factual", "lang": "en", "question": "...", "document": "doc1.pdf",
     "pages": [18], "needs_all_pages": false, "answer": "expected answer, or null when the documents do not contain it"}
"pages" lists every page that holds the answer: finding any one of them counts as a hit, unless needs_all_pages is true.
"""
import argparse
import hashlib
import inspect
import json
import os
import re
import time
from collections import defaultdict
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

import db
import model
import rag
from model import embed_texts, generate

# Development set: doc1 + doc2 + the doc3 sample (the final holdout set is run separately with --golden)
GOLDEN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "eval", "golden_dev.jsonl")
REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
K = rag.TOP_K
MIN_N = 8  # below this a per-type rate is informational only (phases/BASARI_TANIMI.md)

CORRECTNESS_PROMPT = """Question: {question}
Expected answer: {expected}
Given answer: {given}

Does the given answer answer the question with facts that agree with the expected answer? Extra correct detail in the given answer is fine. Details of the expected answer that the question does not ask for may be missing from the given answer. Reply exactly CORRECT or INCORRECT."""

REFUSAL_PROMPT = """Question: {question}
Answer: {given}

Does the answer say that the documents do not contain the requested information (instead of answering it)? Reply exactly YES or NO."""

SUPPORT_PROMPT = """Context:
{context}

Statement: {claim}

Is the statement directly supported by the context? The statement and the context may be in different languages: compare the meaning. Reply exactly YES or NO."""

# One answer sentence with the [n] markers that follow it; a decimal point ("1.6") or an abbreviation followed by a
# lower-case word ("Corp. reflector") does not end a sentence
SENTENCE = re.compile(r"[^\n]+?(?:[.!?](?:\s*\[\d+\])*(?=\s*$|\s+(?![a-zçğıöşü]))|$)", re.MULTILINE)


def load_golden(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def first_hit_rank(chunks, item):
    """1-based rank of the first chunk from an expected page, or None."""
    gold = {(item["document"], p) for p in item["pages"]}
    return next((i for i, c in enumerate(chunks, 1) if (c["file_name"], c["page_number"]) in gold), None)


def pages_covered(chunks, item):
    found = {(c["file_name"], c["page_number"]) for c in chunks}
    return sum((item["document"], p) in found for p in item["pages"]) / len(item["pages"])


def run_info(golden_path):
    with open(golden_path, "rb") as f:
        golden_hash = hashlib.sha256(f.read()).hexdigest()[:12]
    with db.connect() as conn:
        chunks, documents = conn.execute(
            "SELECT count(c.id), count(DISTINCT d.id) FROM rag_chunks c JOIN rag_pages p ON p.id = c.page_id "
            "JOIN rag_documents d ON d.id = p.document_id WHERE d.status = 'done';").fetchone()
    return {
        "time": datetime.now().isoformat(timespec="seconds"),
        "golden": os.path.basename(golden_path), "golden_sha256": golden_hash,
        "indexed_documents": documents, "indexed_chunks": chunks,
        "embedder": model.EMBED_MODEL_NAME, "reranker": model.RERANK_MODEL_NAME, "generator": model.GEN_MODEL_NAME,
        # Which prompts were measured: a resumed run reloads the code, so a changed prompt shows up here
        "prompt_sha256": hashlib.sha256((rag.ANSWER_SYSTEM + rag.ANSWER_PROMPT + json.dumps(rag.REFUSAL) + rag.NOT_FOUND.pattern
                                         + rag.TURKISH.pattern + inspect.getsource(rag.is_refusal)
                                         + inspect.getsource(rag.answer_language) + inspect.getsource(rag.without_language_request)
                                         + "".join(r.pattern for r in rag.ASKED_LANGUAGE.values())).encode()).hexdigest()[:12],
        "judge_sha256": hashlib.sha256((CORRECTNESS_PROMPT + REFUSAL_PROMPT + SUPPORT_PROMPT + SENTENCE.pattern + inspect.getsource(answer_sentences) + inspect.getsource(faithfulness)).encode()).hexdigest()[:12],
        "candidates": rag.CANDIDATES, "top_k": rag.TOP_K, "max_search_rounds": rag.MAX_SEARCH_ROUNDS, "rrf_k": db.RRF_K,
        "image_max_side": rag.IMAGE_MAX_SIDE, "enough_score": rag.ENOUGH_SCORE,
        "max_page_images": rag.MAX_PAGE_IMAGES, "first_sentence_max": rag.FIRST_SENTENCE_MAX,
    }


def write_report(kind, info, markdown, data):
    os.makedirs(REPORT_DIR, exist_ok=True)
    stem = os.path.join(REPORT_DIR, f"{datetime.now():%Y%m%d-%H%M}-{kind}")
    header = f"# {kind.capitalize()} evaluation\n\n" + "\n".join(f"- **{k}**: {v}" for k, v in info.items()) + "\n\n"
    with open(stem + ".md", "w", encoding="utf-8") as f:
        f.write(header + markdown)
    with open(stem + ".json", "w", encoding="utf-8") as f:
        json.dump({"info": info, **data}, f, ensure_ascii=False, indent=2)
    return stem


def percentile(values, q):
    """Nearest-rank percentile."""
    ordered = sorted(values)
    return ordered[max(0, -(-len(ordered) * q // 100) - 1)] if ordered else None


def type_label(name, n):
    return f"{name} ({n})" + ("" if n >= MIN_N else " *")


def md_table(header, rows):
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    return "\n".join(lines + ["| " + " | ".join(str(x) for x in row) + " |" for row in rows]) + "\n"


# ---------------------------------------------------------------- retrieval

def retrieval(args):
    items = load_golden(args.golden)
    answerable = [q for q in items if q["pages"]]
    methods = ["vector", "keyword", "hybrid (RRF)", "vector + reranker", "hybrid + reranker"]
    ranks = {m: [] for m in methods}
    coverage = {m: [] for m in methods}
    top_scores = {"answerable": [], "unanswerable": []}

    for n, item in enumerate(items, 1):
        query = item["question"]
        embedding = embed_texts([query])[0]
        dense = db.dense_search(embedding, rag.CANDIDATES)
        hybrid = db.hybrid_search(query, embedding, rag.CANDIDATES)
        reranked_hybrid = rag.rerank(query, [dict(c) for c in hybrid])
        top_scores["answerable" if item["pages"] else "unanswerable"].append(reranked_hybrid[0]["rerank_score"] if reranked_hybrid else 0.0)
        if not item["pages"]:
            continue
        results = {
            "vector": dense,
            "keyword": db.keyword_search(query, rag.CANDIDATES),
            "hybrid (RRF)": hybrid,
            "vector + reranker": rag.rerank(query, [dict(c) for c in dense]),
            "hybrid + reranker": reranked_hybrid,
        }
        for m in methods:
            ranks[m].append(first_hit_rank(results[m], item))
            coverage[m].append(pages_covered(results[m][:K], item))
        print(f"[{n}/{len(items)}] " + "  ".join(f"{m}={ranks[m][-1] or '-'}" for m in methods) + f"  {query[:60]}")

    def summary(m, subset=None):
        idx = [i for i, q in enumerate(answerable) if subset is None or subset(q)]
        r = [ranks[m][i] for i in idx]
        return {
            "n": len(idx),
            "recall@1": sum(x == 1 for x in r if x) / len(idx),
            f"recall@{K}": sum(bool(x) and x <= K for x in r) / len(idx),
            "mrr": sum(1 / x for x in r if x) / len(idx),
        }

    overall = {m: summary(m) for m in methods}
    multi = [i for i, q in enumerate(answerable) if q["needs_all_pages"]]
    for m in methods:
        overall[m][f"all_pages@{K}"] = sum(coverage[m][i] == 1 for i in multi) / len(multi) if multi else None
    types = sorted({q["type"] for q in answerable})
    by_type = {t: {m: summary(m, lambda q, t=t: q["type"] == t) for m in methods} for t in types}
    documents = sorted({q["document"] for q in answerable})
    by_document = {d: {m: summary(m, lambda q, d=d: q["document"] == d) for m in methods} for d in documents}
    mean = lambda xs: sum(xs) / len(xs) if xs else 0.0

    md = f"## Overall ({len(answerable)} answerable questions)\n\n"
    md += md_table(["Method", "Recall@1", f"Recall@{K}", "MRR", f"All pages@{K} (multi-page)"],
                   [[m, f"{s['recall@1']:.2f}", f"{s[f'recall@{K}']:.2f}", f"{s['mrr']:.3f}",
                     "-" if s[f"all_pages@{K}"] is None else f"{s[f'all_pages@{K}']:.2f}"] for m, s in overall.items()])
    md += f"\n## Recall@{K} by question type\n\n"
    md += md_table(["Type (n)"] + methods, [[type_label(t, by_type[t][methods[0]]['n'])] + [f"{by_type[t][m][f'recall@{K}']:.2f}" for m in methods] for t in types])
    md += f"\n\\* n < {MIN_N}: informational only, no pass/fail threshold.\n"
    md += f"\n## Recall@{K} / MRR by document\n\n"
    md += md_table(["Document (n)"] + methods, [[type_label(d, by_document[d][methods[0]]['n'])]
                   + [f"{by_document[d][m][f'recall@{K}']:.2f} / {by_document[d][m]['mrr']:.2f}" for m in methods] for d in documents])
    md += "\n## Rank of the first correct chunk per question (- = not in the 40 candidates)\n\n"
    md += md_table(["id", "type", "question"] + methods,
                   [[q["id"], q["type"], q["question"][:60]] + [ranks[m][i] or "-" for m in methods] for i, q in enumerate(answerable)])
    md += ("\n## Top reranker score: questions with and without an answer in the documents\n\n"
           + md_table(["", "mean", "min", "max"], [[k, f"{mean(v):.3f}", f"{min(v):.3f}", f"{max(v):.3f}"] for k, v in top_scores.items() if v]))

    info = run_info(args.golden)
    stem = write_report("retrieval", info, md, {"overall": overall, "by_type": by_type, "by_document": by_document, "ranks": {m: dict(zip((q["id"] for q in answerable), ranks[m])) for m in methods}, "top_rerank_scores": top_scores})
    print("\n" + md.split("\n## Rank")[0])
    print(f"Report: {stem}.md")


# ---------------------------------------------------------------- answers

def ask(prompt, max_new_tokens=5):
    return generate(prompt, max_new_tokens=max_new_tokens).strip()


def cited_chunks(text, chunks):
    numbers = dict.fromkeys(int(n) for n in re.findall(r"\[(\d+)\]", text))
    return [chunks[n - 1] for n in numbers if 1 <= n <= len(chunks)]


def answer_sentences(text):
    """(sentence without citation markers, cited excerpt numbers) for each sentence of an answer.
    The answer's own sentences are the claims: an LLM asked to split a one-sentence answer into statements invented
    new ones from its own knowledge, which then counted as unsupported (phases/faz-j/RAPOR.md)."""
    # A sentence the model repeated (a repetition loop) is one claim: its citations are merged
    sentences = {}
    for match in SENTENCE.finditer(text):
        sentence = re.sub(r"^\s*(?:[-*•]|\d+[.)])\s+", "", match.group().strip())
        claim = re.sub(r"\s*\[\d+\]", "", sentence).strip()
        if len(claim) > 3:
            cited = sentences.setdefault(claim, [])
            cited += [n for n in map(int, re.findall(r"\[(\d+)\]", sentence)) if n not in cited]
    return list(sentences.items())[:8]


def faithfulness(answer_text, chunks, judgments, item):
    claims = answer_sentences(answer_text)
    if not claims:
        return None
    supported = 0
    for claim, numbers in claims:
        # A cited sentence is checked against the excerpts it cites only: a shorter context the small judge reads reliably
        cited = [chunks[n - 1] for n in dict.fromkeys(numbers) if 1 <= n <= len(chunks)]
        verdict = ask(SUPPORT_PROMPT.format(context=rag.format_context(cited or chunks), claim=claim))
        ok = verdict.upper().startswith("YES")
        supported += ok
        judgments.append({"id": item["id"], "kind": "claim_supported", "question": item["question"], "claim": claim,
                          "cited": numbers, "judge": ok, "human": None})
    return supported / len(claims)


def load_checkpoint(path, golden_hash):
    """Rows and judgments of questions finished by an interrupted run on the same golden set."""
    rows, judgments = [], []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                saved = json.loads(line)
                if saved["golden_sha256"] == golden_hash:
                    rows.append(saved["row"])
                    judgments.extend(saved["judgments"])
    return rows, judgments


def answers(args):
    items = load_golden(args.golden)
    golden_hash = run_info(args.golden)["golden_sha256"]
    # Each finished question is appended here at once, so an interrupted run can go on with --resume
    checkpoint = os.path.join(REPORT_DIR, "answers-partial.jsonl")
    os.makedirs(REPORT_DIR, exist_ok=True)
    rows, judgments = load_checkpoint(checkpoint, golden_hash) if args.resume else ([], [])
    if not args.resume and os.path.exists(checkpoint):
        os.remove(checkpoint)
    done = {r["id"] for r in rows}
    if done:
        print(f"Resuming: {len(done)} questions already answered")
    for n, item in enumerate(items[: args.limit], 1):
        if item["id"] in done:
            continue
        start = time.time()
        judged_before = len(judgments)
        ttft = None  # time to the first piece of text the user sees (the UI streams the same generator)
        for result in rag.answer_stream(item["question"]):
            if ttft is None and isinstance(result, str):
                ttft = time.time() - start
        latency = time.time() - start
        text, chunks = result["answer"], result["chunks"]
        cited = cited_chunks(text, chunks)
        gold = {(item["document"], p) for p in item["pages"]}
        refused = ask(REFUSAL_PROMPT.format(question=item["question"], given=text)).upper().startswith("YES")
        judgments.append({"id": item["id"], "kind": "refusal", "question": item["question"], "answer": text, "judge": refused, "human": None})
        row = {
            "id": item["id"], "type": item["type"], "document": item["document"], "answerable": bool(item["pages"]), "latency_s": round(latency, 1), "ttft_s": round(ttft, 1),
            "answer": text, "refused": refused, "regex_refused": bool(rag.NOT_FOUND.search(text)),
            # The model's text before rag.answer replaced a refusal; informational (phases/BASARI_TANIMI.md)
            "raw_answer": result.get("raw_answer", text), "raw_cited": bool(cited_chunks(result.get("raw_answer", text), chunks)),
            "search_rounds": len(result["queries"]), "cited": [(c["file_name"], c["page_number"]) for c in cited],
            "retrieved_gold": any((c["file_name"], c["page_number"]) in gold for c in chunks),
        }
        if item["pages"]:
            row["citation_precision"] = sum((c["file_name"], c["page_number"]) in gold for c in cited) / len(cited) if cited else None
            row["cites_gold_page"] = any((c["file_name"], c["page_number"]) in gold for c in cited)
            row["correct"] = ask(CORRECTNESS_PROMPT.format(question=item["question"], expected=item["answer"], given=text)).upper().startswith("CORRECT")
            judgments.append({"id": item["id"], "kind": "correct", "question": item["question"], "expected": item["answer"], "answer": text, "judge": row["correct"], "human": None})
            row["faithfulness"] = None if refused else faithfulness(text, chunks, judgments, item)
        rows.append(row)
        with open(checkpoint, "a", encoding="utf-8") as f:
            f.write(json.dumps({"golden_sha256": golden_hash, "row": row, "judgments": judgments[judged_before:]}, ensure_ascii=False) + "\n")
        print(f"[{n}/{len(items)}] {item['id']} {latency:5.1f}s refused={refused} correct={row.get('correct', '-')} "
              f"faith={row.get('faithfulness')} cites={row['cited']}")

    if len(rows) < len(items):
        print(f"\n{len(rows)}/{len(items)} questions answered so far. Continue with: python evaluate.py answers --resume")
        return
    order = {item["id"]: i for i, item in enumerate(items)}
    rows.sort(key=lambda r: order[r["id"]])

    mean = lambda xs: sum(xs) / len(xs) if xs else None
    fmt = lambda x: "-" if x is None else f"{x:.2f}"
    ans = [r for r in rows if r["answerable"]]
    unans = [r for r in rows if not r["answerable"]]
    metrics = {
        "answer_correctness": mean([r["correct"] for r in ans]),
        "faithfulness": mean([r["faithfulness"] for r in ans if r["faithfulness"] is not None]),
        "citation_precision": mean([r["citation_precision"] for r in ans if r["citation_precision"] is not None]),
        "cites_expected_page": mean([r["cites_gold_page"] for r in ans]),
        "answers_without_citation": mean([not r["cited"] and not r["refused"] for r in ans]),
        "false_refusals": mean([r["refused"] for r in ans]),
        "unanswerable_refused": mean([r["refused"] for r in unans]),
        "unanswerable_with_citation": mean([bool(r["cited"]) for r in unans]),
        "raw_unanswerable_with_citation": mean([r.get("raw_cited", bool(r["cited"])) for r in unans]),
        "mean_latency_s": mean([r["latency_s"] for r in rows]),
        "p50_latency_s": percentile([r["latency_s"] for r in rows], 50),
        "p95_latency_s": percentile([r["latency_s"] for r in rows], 95),
        "p50_ttft_s": percentile([r["ttft_s"] for r in rows if "ttft_s" in r], 50),
        "p95_ttft_s": percentile([r["ttft_s"] for r in rows if "ttft_s" in r], 95),
    }
    md = "## Summary\n\n" + md_table(["Metric", "Value"], [[k, fmt(v)] for k, v in metrics.items()])
    md += "\nJudge: the local generator model. Check it with `python evaluate.py calibrate <run>-judgments.jsonl` after labelling some rows.\n"
    by_type = defaultdict(list)
    for r in ans:
        by_type[r["type"]].append(r)
    md += "\n## By question type\n\n" + md_table(["Type (n)", "correct", "faithfulness", "cites expected page"],
        [[type_label(t, len(rs)), fmt(mean([r["correct"] for r in rs])), fmt(mean([r["faithfulness"] for r in rs if r["faithfulness"] is not None])),
          fmt(mean([r["cites_gold_page"] for r in rs]))] for t, rs in sorted(by_type.items())])
    md += f"\n\\* n < {MIN_N}: informational only, no pass/fail threshold.\n"
    by_document = defaultdict(list)
    for r in rows:
        by_document[r["document"]].append(r)
    md += "\n## By document\n\n" + md_table(["Document (n)", "correct", "faithfulness", "cites expected page", "without citation", "unanswerable refused"],
        [[type_label(d, len(rs)), fmt(mean([r["correct"] for r in rs if r["answerable"]])),
          fmt(mean([r["faithfulness"] for r in rs if r.get("faithfulness") is not None])),
          fmt(mean([r["cites_gold_page"] for r in rs if r["answerable"]])),
          fmt(mean([not r["cited"] and not r["refused"] for r in rs if r["answerable"]])),
          fmt(mean([r["refused"] for r in rs if not r["answerable"]]))] for d, rs in sorted(by_document.items())])
    md += "\n## Per question\n\n" + md_table(["id", "type", "s", "refused", "correct", "faith.", "cited pages", "answer"],
        [[r["id"], r["type"], r["latency_s"], r["refused"], r.get("correct", "-"), fmt(r.get("faithfulness")),
          ", ".join(str(p) for _, p in r["cited"]) or "-", r["answer"][:120].replace("\n", " ").replace("|", "/")] for r in rows])

    info = run_info(args.golden)
    stem = write_report("answers", info, md, {"metrics": metrics, "rows": rows})
    with open(stem + "-judgments.jsonl", "w", encoding="utf-8") as f:
        f.writelines(json.dumps(j, ensure_ascii=False) + "\n" for j in judgments)
    os.remove(checkpoint)
    print("\n" + md.split("\n## Per question")[0])
    print(f"Report: {stem}.md\nJudge decisions to label: {stem}-judgments.jsonl (set \"human\" to true/false)")


# ---------------------------------------------------------------- judge calibration

def cohen_kappa(pairs):
    n = len(pairs)
    observed = sum(a == b for a, b in pairs) / n
    p_judge, p_human = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
    expected = p_judge * p_human + (1 - p_judge) * (1 - p_human)
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)


def label(args):
    """Write a stratified list for human labelling: every negative judge decision + random positives, per kind."""
    import random
    with open(args.judgments, encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    random.seed(args.seed)
    picked = []
    for kind in sorted({r["kind"] for r in rows}):
        of_kind = [r for r in rows if r["kind"] == kind]
        # for "refusal" the rare decision is True (refused); for the others it is False (incorrect / unsupported)
        rare = [r for r in of_kind if r["judge"] == (kind == "refusal")]
        common = [r for r in of_kind if r not in rare]
        picked += rare + random.sample(common, min(len(common), max(0, args.per_kind - len(rare))))
        print(f"{kind:18s} {len(rare)} rare + {min(len(common), max(0, args.per_kind - len(rare)))} random of {len(of_kind)}")
    out = args.judgments.replace(".jsonl", "-to-label.jsonl")
    with open(out, "w", encoding="utf-8") as f:
        f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in picked)
    print(f"Label these {len(picked)} rows (set \"human\" to true/false), then: python evaluate.py calibrate {out}")


def calibrate(args):
    with open(args.judgments, encoding="utf-8") as f:
        rows = [json.loads(line) for line in f if line.strip()]
    labelled = defaultdict(list)
    for r in rows:
        if isinstance(r.get("human"), bool):
            labelled[r["kind"]].append((r["judge"], r["human"]))
    if not labelled:
        print('No labelled rows yet: set "human" to true or false on some rows first.')
        return
    print(f"{'kind':18s} {'n':>4s} {'agreement':>10s} {'kappa':>7s}")
    for kind, pairs in sorted(labelled.items()):
        agreement = sum(a == b for a, b in pairs) / len(pairs)
        print(f"{kind:18s} {len(pairs):4d} {agreement:10.2f} {cohen_kappa(pairs):7.2f}")


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("retrieval", "answers"):
        p = sub.add_parser(name)
        p.add_argument("--golden", default=GOLDEN)
        if name == "answers":
            p.add_argument("--limit", type=int, help="stop after the first N questions (the run can be continued with --resume)")
            p.add_argument("--resume", action="store_true", help="skip questions an interrupted run already answered")
    p = sub.add_parser("label")
    p.add_argument("judgments")
    p.add_argument("--per-kind", type=int, default=30)
    p.add_argument("--seed", type=int, default=0)
    p = sub.add_parser("calibrate")
    p.add_argument("judgments")
    args = parser.parse_args()
    {"retrieval": retrieval, "answers": answers, "label": label, "calibrate": calibrate}[args.command](args)


if __name__ == "__main__":
    main()
