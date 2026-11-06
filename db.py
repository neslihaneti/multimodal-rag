import os
import re

import psycopg

from model import EMBED_DIM

PG_HOST = os.getenv("host")
PG_DB   = os.getenv("database_name")
PG_USER = os.getenv("usr_name")
PG_PASS = os.getenv("usr_password")
PG_PORT = os.getenv("port")

RRF_K = 60


def connect():
    return psycopg.connect(dbname=PG_DB, user=PG_USER, password=PG_PASS, host=PG_HOST, port=PG_PORT)


def to_vector(embedding):
    return "[" + ",".join(f"{x:.6f}" for x in embedding) + "]"


def create_tables():
    with connect() as conn:
        conn.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rag_documents (
                id SERIAL PRIMARY KEY,
                file_name TEXT NOT NULL,
                file_hash TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'indexing',
                indexed_at TIMESTAMPTZ NOT NULL DEFAULT now()
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rag_pages (
                id SERIAL PRIMARY KEY,
                document_id INT NOT NULL REFERENCES rag_documents(id) ON DELETE CASCADE,
                page_number INT NOT NULL,
                image_path TEXT NOT NULL,
                ocr_text TEXT NOT NULL
            );
        """)
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS rag_chunks (
                id SERIAL PRIMARY KEY,
                page_id INT NOT NULL REFERENCES rag_pages(id) ON DELETE CASCADE,
                heading TEXT,
                content TEXT NOT NULL,
                context TEXT,
                embedding VECTOR({EMBED_DIM}) NOT NULL,
                tsv TSVECTOR GENERATED ALWAYS AS (
                    to_tsvector('simple', coalesce(heading, '') || ' ' || coalesce(context, '') || ' ' || content)
                ) STORED
            );
        """)
        # Where the page text came from: 'text_layer' (the PDF's own text) or 'ocr' (Chandra)
        conn.execute("ALTER TABLE rag_pages ADD COLUMN IF NOT EXISTS text_source TEXT;")
        conn.execute("CREATE INDEX IF NOT EXISTS rag_chunks_embedding_idx ON rag_chunks USING hnsw (embedding vector_cosine_ops);")
        conn.execute("CREATE INDEX IF NOT EXISTS rag_chunks_tsv_idx ON rag_chunks USING gin (tsv);")


def find_document(file_hash):
    with connect() as conn:
        return conn.execute("SELECT id, status FROM rag_documents WHERE file_hash = %s;", (file_hash,)).fetchone()


def delete_document(document_id):
    with connect() as conn:
        conn.execute("DELETE FROM rag_documents WHERE id = %s;", (document_id,))


def insert_document(file_name, file_hash):
    with connect() as conn:
        return conn.execute(
            "INSERT INTO rag_documents (file_name, file_hash) VALUES (%s, %s) RETURNING id;",
            (file_name, file_hash),
        ).fetchone()[0]


def mark_document_done(document_id):
    with connect() as conn:
        conn.execute("UPDATE rag_documents SET status = 'done', indexed_at = now() WHERE id = %s;", (document_id,))


def insert_page(document_id, page_number, image_path, ocr_text, text_source):
    with connect() as conn:
        return conn.execute(
            "INSERT INTO rag_pages (document_id, page_number, image_path, ocr_text, text_source) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (document_id, page_number, image_path, ocr_text, text_source),
        ).fetchone()[0]


def insert_chunks(page_id, chunks, conn=None):
    if conn is None:
        with connect() as conn:
            return insert_chunks(page_id, chunks, conn)
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO rag_chunks (page_id, heading, content, context, embedding) VALUES (%s, %s, %s, %s, %s::vector);",
            [(page_id, c["heading"], c["content"], c["context"], to_vector(c["embedding"])) for c in chunks],
        )


def insert_page_with_chunks(document_id, page_number, image_path, text, text_source, chunks):
    """One transaction per page, so a page is either fully stored or not at all (indexing can resume per page)."""
    with connect() as conn:
        page_id = conn.execute(
            "INSERT INTO rag_pages (document_id, page_number, image_path, ocr_text, text_source) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
            (document_id, page_number, image_path, text, text_source),
        ).fetchone()[0]
        insert_chunks(page_id, chunks, conn)


def stored_pages(file_name):
    """(page id, page number, page text, chunk contents in order) of every page of a document."""
    with connect() as conn:
        return conn.execute("""
            SELECT p.id, p.page_number, p.ocr_text, coalesce(array_agg(c.content ORDER BY c.id) FILTER (WHERE c.id IS NOT NULL), '{}')
            FROM rag_pages p JOIN rag_documents d ON d.id = p.document_id LEFT JOIN rag_chunks c ON c.page_id = p.id
            WHERE d.file_name = %s GROUP BY p.id ORDER BY p.page_number;
        """, (file_name,)).fetchall()


def replace_page_chunks(page_id, chunks):
    """Swap a page's chunks in one transaction."""
    with connect() as conn:
        conn.execute("DELETE FROM rag_chunks WHERE page_id = %s;", (page_id,))
        insert_chunks(page_id, chunks, conn)


def indexed_page_numbers(document_id):
    with connect() as conn:
        return {row[0] for row in conn.execute("SELECT page_number FROM rag_pages WHERE document_id = %s;", (document_id,))}


def list_documents():
    with connect() as conn:
        return conn.execute("""
            SELECT d.file_name, count(DISTINCT p.id), count(c.id)
            FROM rag_documents d
            LEFT JOIN rag_pages p ON p.document_id = d.id
            LEFT JOIN rag_chunks c ON c.page_id = p.id
            WHERE d.status = 'done'
            GROUP BY d.id ORDER BY d.file_name;
        """).fetchall()


# Question words that match nearly every chunk; left in, they push long chunks to the top of keyword search
# (keyword Recall@6 0.29 with them, 0.86 without; phases/faz-4/RAPOR.md)
STOPWORDS = frozenset("""
a an the and or of to in on for by with from at as is are was were be been being it its this that these those what which
who whom whose when where why how does do did can could should would will shall may might must has have had not no than
then there their they them into about over under after before between according per also any all each such both more most
other some only same so very just
ve veya ile bir bu şu o da de mi mı mu mü ne nedir neler nasıl hangi hangisi kaç için gibi göre olan olarak ise ki çok
daha en her ya
""".split())


def keyword_query(text):
    # OR the words together; AND-ing every word of a natural-language question rarely matches anything
    terms = dict.fromkeys(t for t in re.findall(r"\w+", text.lower()) if len(t) > 2 and t not in STOPWORDS)
    return " | ".join(terms)


SEARCH_COLUMNS = ["id", "file_name", "page_number", "image_path", "heading", "content", "context", "score"]
SEARCH_SELECT = """
    SELECT c.id, d.file_name, p.page_number, p.image_path, c.heading, c.content, c.context, {score}
    FROM rag_chunks c
    JOIN rag_pages p ON p.id = c.page_id
    JOIN rag_documents d ON d.id = p.document_id
"""


def dense_search(query_embedding, limit=40):
    """Vector search alone (used by evaluate.py to measure what each half of hybrid search contributes)."""
    with connect() as conn:
        rows = conn.execute(SEARCH_SELECT.format(score="1 - (c.embedding <=> %(vec)s::vector)") + """
            WHERE d.status = 'done' ORDER BY c.embedding <=> %(vec)s::vector LIMIT %(n)s;
        """, {"vec": to_vector(query_embedding), "n": limit}).fetchall()
    return [dict(zip(SEARCH_COLUMNS, row)) for row in rows]


def keyword_search(query_text, limit=40):
    """Full-text search alone, with the same query terms and ranking hybrid_search uses.
    ts_rank's normalisation 1 divides by the log of the chunk length, so long chunks no longer win on many weak matches."""
    terms = keyword_query(query_text)
    if not terms:
        return []
    with connect() as conn:
        rows = conn.execute(SEARCH_SELECT.format(score="ts_rank(c.tsv, q, 1)") + """
            , to_tsquery('simple', %(terms)s) q
            WHERE d.status = 'done' AND c.tsv @@ q ORDER BY ts_rank(c.tsv, q, 1) DESC LIMIT %(n)s;
        """, {"terms": terms, "n": limit}).fetchall()
    return [dict(zip(SEARCH_COLUMNS, row)) for row in rows]


def hybrid_search(query_text, query_embedding, limit=40):
    """Dense (pgvector cosine) + keyword (Postgres full-text) search fused with Reciprocal Rank Fusion."""
    params = {"vec": to_vector(query_embedding), "terms": keyword_query(query_text), "n": limit, "k": RRF_K}
    with connect() as conn:
        rows = conn.execute("""
            WITH ready AS (  -- rank only chunks of fully indexed documents, or half-indexed ones shift the ranks
                SELECT c.id, c.embedding, c.tsv
                FROM rag_chunks c JOIN rag_pages p ON p.id = c.page_id JOIN rag_documents d ON d.id = p.document_id
                WHERE d.status = 'done'
            ),
            dense AS (
                SELECT id, row_number() OVER (ORDER BY embedding <=> %(vec)s::vector) AS r
                FROM ready
                ORDER BY embedding <=> %(vec)s::vector
                LIMIT %(n)s
            ),
            sparse AS (
                SELECT id, row_number() OVER (ORDER BY ts_rank(tsv, q, 1) DESC) AS r
                FROM ready, to_tsquery('simple', %(terms)s) q
                WHERE %(terms)s <> '' AND tsv @@ q
                ORDER BY ts_rank(tsv, q, 1) DESC
                LIMIT %(n)s
            ),
            fused AS (
                SELECT id, coalesce(1.0 / (%(k)s + dense.r), 0) + coalesce(1.0 / (%(k)s + sparse.r), 0) AS score
                FROM dense FULL OUTER JOIN sparse USING (id)
            )
            SELECT c.id, d.file_name, p.page_number, p.image_path, c.heading, c.content, c.context, f.score
            FROM fused f
            JOIN rag_chunks c ON c.id = f.id
            JOIN rag_pages p ON p.id = c.page_id
            JOIN rag_documents d ON d.id = p.document_id
            ORDER BY f.score DESC
            LIMIT %(n)s;
        """, params).fetchall()
    return [dict(zip(SEARCH_COLUMNS, row)) for row in rows]
