import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [ROOT, os.path.join(ROOT, "tests")]

import stubs  # noqa: E402

stubs.install()


import psycopg  # noqa: E402
import pytest  # noqa: E402
from dotenv import load_dotenv  # noqa: E402

import db  # noqa: E402


@pytest.fixture(scope="module")
def test_db():
    load_dotenv(os.path.join(ROOT, ".env"))
    settings = {"PG_HOST": os.getenv("host"), "PG_USER": os.getenv("usr_name"), "PG_PASS": os.getenv("usr_password"),
                "PG_PORT": os.getenv("port"), "PG_DB": os.getenv("TEST_DATABASE_NAME", "rag_test")}
    assert settings["PG_DB"].endswith("_test"), "tests empty the database: never point them at the real index"
    saved = {k: getattr(db, k) for k in settings}
    for k, v in settings.items():
        setattr(db, k, v)
    try:
        with psycopg.connect(dbname="postgres", user=db.PG_USER, password=db.PG_PASS, host=db.PG_HOST,
                             port=db.PG_PORT, autocommit=True, connect_timeout=3) as conn:
            if not conn.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db.PG_DB,)).fetchone():
                conn.execute(f'CREATE DATABASE "{db.PG_DB}"')
    except psycopg.OperationalError as e:
        pytest.skip(f"no PostgreSQL server reachable: {e}")
    db.create_tables()
    with db.connect() as conn:
        conn.execute("TRUNCATE rag_documents RESTART IDENTITY CASCADE;")
    yield
    for k, v in saved.items():
        setattr(db, k, v)
