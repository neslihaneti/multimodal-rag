import os
import re

from PIL import Image

import db
from model import count_tokens, embed_texts, generate, generate_stream, rerank_scores

CANDIDATES = 40         # hybrid search results passed to the reranker
TOP_K = 6               # chunks given to the answer model
MAX_SEARCH_ROUNDS = 3   # agentic search: first search + up to 2 follow-up searches
MAX_PAGE_IMAGES = 2  # 1 image was 1 s faster but answered q24 and q29 wrongly (a repetition loop); 3 is 2 s slower (phases/faz-8)
IMAGE_MAX_SIDE = 896  # 1280 cost ~1.170 prompt tokens per page and the same answers (phases/faz-6a)
# Prompts are kept under this many tokens: on MPS the generator crashes on long prompts (model.MAX_INPUT_TOKENS)
PROMPT_TOKEN_BUDGET = int(os.getenv("PROMPT_TOKEN_BUDGET", "9000"))
MIN_CHUNKS = 3
# Characters held back at most while waiting for the end of the first sentence: a refusal shows within them
# (the same decisions as on the whole first sentence for all 82 dev answers; phases/faz-8)
FIRST_SENTENCE_MAX = 60
# When the best reranked chunk scores at least this much, the results count as enough without asking the model
# (None: always ask). Every answerable development question already stopped after one search (phases/faz-6)
ENOUGH_SCORE = 0.5  # answerable dev questions: 62 of 69 score above it; unanswerable ones at most 0.34

NOT_FOUND = re.compile(r"bilgi (verilmemiş|bulunmamakta|bulunmuyor|yer almamakta|yer almıyor|yok)|belirtilmemiş|not (mentioned|found|contain|provide)|no information", re.IGNORECASE)

# The model's refusal is replaced by a fixed sentence without citations: the prompt alone did not stop it from citing
# excerpts while refusing, nor from refusing a Turkish question in English (phases/faz-5b)
REFUSAL = {"tr": "Belgelerde bu konuda bilgi yok.", "en": "The documents do not contain information about this."}
# No re.IGNORECASE: with it "ı" also matches "i" and "I", and every English question looks Turkish
TURKISH = re.compile(r"[çğıöşüÇĞİÖŞÜ]|\b(?:[Nn]e|[Nn]eler|[Nn]edir|[Hh]angi|[Kk]aç|[Nn]asıl|[Nn]eden|[Nn]için|m[iıuü]|ve|ile|için|bu|bir|göre|edilir)\b")


# An explicit request for a language ("İngilizce cevap ver", "answer in Turkish") wins over the question's own language
ASKED_LANGUAGE = {
    "en": re.compile(r"\b(?:in|into) English\b|[İIiı]ngilizce\s+(?:olarak\s+)?(?:cevap|yan[ıi]t|a[çc][ıi]kla|anlat|yaz|s[öo]yle)"),
    "tr": re.compile(r"\b(?:in|into) Turkish\b|[Tt][üu]rk[çc]e\s+(?:olarak\s+)?(?:cevap|yan[ıi]t|a[çc][ıi]kla|anlat|yaz|s[öo]yle)"),
}
LANGUAGE_NAMES = {"tr": "Turkish", "en": "English"}


def question_language(question):
    return "tr" if TURKISH.search(question) else "en"


def answer_language(question):
    for language, request in ASKED_LANGUAGE.items():
        if request.search(question):
            return language
    return question_language(question)


def without_language_request(question):
    """The question without its request for a language: the request words otherwise steer the search away."""
    request = re.compile("|".join(r.pattern for r in ASKED_LANGUAGE.values()))
    sentences = re.split(r"(?<=[.?!])\s+", question.strip())
    kept = [s for s in sentences if not request.search(s)]
    return " ".join(kept) if kept else request.sub("", question).strip(" ,.") or question


def is_refusal(text):
    """True when the answer opens with a refusal; a refusal later in the text may follow a partial answer."""
    first_sentence = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0]
    return bool(NOT_FOUND.search(first_sentence))

# Extra model.generate options for answers only (search decisions and the judge are left as they are; phases/faz-5b)
ANSWER_OPTIONS = {}

REWRITE_PROMPT = """Conversation so far:
{history}

Follow-up question: {question}

Rewrite the follow-up question as a standalone search query that can be understood without the conversation. Keep the language of the question. Answer only with the query."""

SEARCH_DECISION_PROMPT = """Question: {question}

Search results so far:
{context}

Do these results contain enough information to answer the question fully?
If yes, reply exactly: ENOUGH
If not, reply with one line: SEARCH: <a new, different search query that would find the missing information>"""

ANSWER_SYSTEM = "You answer questions about the user's documents. Use only the provided document excerpts and page images; never use outside knowledge."

ANSWER_PROMPT = """Attached page images, in order: {images}

Document excerpts:
{context}

Question: {question}

Answer using only the excerpts and the page images. End every sentence of your answer with the numbers of the excerpts it is based on, in square brackets. This applies to short answers too: even a one-sentence answer must end with its citation, for example: "The device weighs 4 kg [2]." or "Both colours are allowed [1][3]." If the documents do not contain the answer, the rule about citations does not apply: reply only with "The documents do not contain information about this.", with no excerpt numbers. Otherwise write the whole answer in {language}, even when the excerpts are in another language."""


def passage_text(chunk):
    return f"{chunk['context']}\n{chunk['content']}".strip() if chunk["context"] else chunk["content"]


def rerank(query, chunks):
    if not chunks:
        return []
    scores = rerank_scores(query, [passage_text(c) for c in chunks])
    for chunk, score in zip(chunks, scores):
        chunk["rerank_score"] = score
    return sorted(chunks, key=lambda c: c["rerank_score"], reverse=True)


def retrieve(query, top_k=TOP_K):
    candidates = db.hybrid_search(query, embed_texts([query])[0], CANDIDATES)
    return rerank(query, candidates)[:top_k]


def rewrite_query(question, history):
    if not history:
        return question
    lines = [f"{role}: {content[:500]}" for role, content in history[-6:]]
    rewritten = generate(REWRITE_PROMPT.format(history="\n".join(lines), question=question), max_new_tokens=100)
    return rewritten.strip().strip('"') or question


def format_context(chunks):
    return "\n\n".join(
        f"[{i}] {c['file_name']} · page {c['page_number']}" + (f" · {c['heading']}" if c["heading"] else "") + f"\n{c['content']}"
        for i, c in enumerate(chunks, 1)
    )


def decision_prompt(query, chunks):
    return SEARCH_DECISION_PROMPT.format(question=query, context=format_context(chunks))


def agentic_search(query):
    """Search, let the model judge whether the results are enough, and search again with a new query if not."""
    pool, queries = {}, [query]
    for round_no in range(MAX_SEARCH_ROUNDS):
        for chunk in retrieve(queries[-1]):
            pool.setdefault(chunk["id"], chunk)
        if round_no == MAX_SEARCH_ROUNDS - 1 or not pool:
            break
        current = rerank(query, list(pool.values()))[:TOP_K]
        if ENOUGH_SCORE is not None and current[0].get("rerank_score", 0.0) >= ENOUGH_SCORE:
            break
        while len(current) > 1 and count_tokens(decision_prompt(query, current)) > PROMPT_TOKEN_BUDGET:
            current = current[:-1]
        decision = generate(decision_prompt(query, current), max_new_tokens=60)
        match = re.match(r"\s*SEARCH:\s*(.+)", decision, re.IGNORECASE)
        if not match or match.group(1).strip() in queries:
            break
        queries.append(match.group(1).strip())
    # Rank everything gathered against the standalone question
    return rerank(query, list(pool.values()))[:TOP_K], queries


def load_page_image(path):
    image = Image.open(path).convert("RGB")
    image.thumbnail((IMAGE_MAX_SIDE, IMAGE_MAX_SIDE))
    return image


def build_prompt(query, chunks, max_images, language):
    pages = list(dict.fromkeys((c["file_name"], c["page_number"], c["image_path"]) for c in chunks))[:max_images]
    images = [load_page_image(path) for _, _, path in pages]
    image_list = ", ".join(f"{name} page {page}" for name, page, _ in pages) or "none"
    return images, ANSWER_PROMPT.format(images=image_list, context=format_context(chunks), question=query,
                                         language=LANGUAGE_NAMES[language])


def fit_prompt(query, chunks, language="en"):
    """Drop the lowest-ranked chunks down to MIN_CHUNKS, then page images, then more chunks, until the prompt fits."""
    max_images = MAX_PAGE_IMAGES
    while True:
        images, prompt = build_prompt(query, chunks, max_images, language)
        if len(chunks) == 1 and not max_images or count_tokens(prompt, images, ANSWER_SYSTEM) <= PROMPT_TOKEN_BUDGET:
            return chunks, images, prompt
        if len(chunks) > MIN_CHUNKS or not max_images:
            chunks = chunks[:-1]
        else:
            max_images -= 1


def answer(question, history=()):
    *_, result = answer_stream(question, history)
    return result


def answer_stream(question, history=()):
    """Yield the answer text piece by piece as the model writes it, then the result dict as the last item.
    Nothing is shown until the first sentence is complete or FIRST_SENTENCE_MAX characters are written: is_refusal()
    decides on that start, and a refusal is replaced by the fixed sentence (the rest of the generation is then stopped)."""
    query = rewrite_query(without_language_request(question), list(history))
    chunks, queries = agentic_search(query)
    if not chunks:
        text = "No indexed document matched this question. Index a folder of PDFs first."
        yield text
        yield {"answer": text, "raw_answer": text, "sources": [], "queries": queries, "chunks": []}
        return

    # The language comes from the user's own words: a rewritten follow-up query may have lost it
    language = answer_language(question)
    chunks, images, prompt = fit_prompt(query, chunks, language)
    pieces = generate_stream(prompt, images=images, system=ANSWER_SYSTEM, options=ANSWER_OPTIONS)
    raw_text, shown = "", False
    for piece in pieces:
        raw_text += piece
        if shown:
            yield piece
        elif re.search(r"[.!?]\s|\n", raw_text.strip()) or len(raw_text) > FIRST_SENTENCE_MAX:
            if is_refusal(raw_text):
                pieces.close()
                break
            shown = True
            yield raw_text.lstrip()
    raw_text = raw_text.strip()
    refused = not shown and is_refusal(raw_text)  # text already shown stays: the decision was made on its start
    text = REFUSAL[language] if refused else raw_text
    if refused or not shown:
        yield text
    yield _result(text, raw_text, chunks, queries)


def _result(text, raw_text, chunks, queries):
    cited = [int(n) for n in re.findall(r"\[(\d+)\]", text) if 1 <= int(n) <= len(chunks)]
    if NOT_FOUND.search(text):  # small models sometimes cite excerpts even when saying the answer is missing
        cited = []
    sources = list(dict.fromkeys(
        (chunks[n - 1]["file_name"], chunks[n - 1]["page_number"], chunks[n - 1]["image_path"]) for n in cited
    ))
    return {
        "answer": text,
        "raw_answer": raw_text,
        "sources": [{"file_name": f, "page_number": p, "image_path": i} for f, p, i in sources],
        "queries": queries,
        "chunks": chunks,
    }
