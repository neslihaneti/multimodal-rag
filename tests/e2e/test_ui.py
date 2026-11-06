"""Browser test of the Streamlit app against the real index (doc1.pdf must be indexed). Needs: pip install playwright
and `playwright install chromium`. Starts its own Streamlit server on UI_TEST_PORT (default 8599)."""
import os
import subprocess
import sys
import time
import urllib.request

import pytest
from dotenv import dotenv_values

playwright = pytest.importorskip("playwright.sync_api")

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PORT = int(os.getenv("UI_TEST_PORT", "8599"))
URL = f"http://localhost:{PORT}"
ANSWER_TIMEOUT_MS = 300_000  # the first question also loads the models


@pytest.fixture(scope="module")
def app():
    env = {**os.environ, **dotenv_values(os.path.join(ROOT, ".env"))}  # the real index, not a test database
    server = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "app.py", "--server.port", str(PORT), "--server.headless", "true"],
        cwd=ROOT, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:
                if urllib.request.urlopen(f"{URL}/_stcore/health", timeout=1).status == 200:
                    break
            except OSError:
                time.sleep(1)
        else:
            pytest.fail("Streamlit did not start")
        yield URL
    finally:
        server.terminate()
        try:
            server.wait(10)
        except subprocess.TimeoutExpired:
            server.kill()  # a running generate() can ignore SIGTERM


@pytest.fixture(scope="module")
def page(app):
    with playwright.sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1400, "height": 1000})
        page.goto(app)
        yield page
        browser.close()


def test_page_loads_with_the_indexed_documents(page):
    expect = playwright.expect
    expect(page.get_by_role("heading", name="RAG Chatbot with Source Images")).to_be_visible(timeout=60_000)
    expect(page.get_by_text("doc1.pdf (", exact=False)).to_be_visible()


def test_question_gets_an_answer_with_loading_source_images(page):
    expect = playwright.expect
    page.get_by_placeholder("Ask a question about your documents").fill("Yapay zeka tabanlı sistemlerde hangi test seviyeleri vardır?")
    page.keyboard.press("Enter")

    answer = page.locator('[data-testid="stChatMessage"]').nth(1)
    expect(answer.get_by_text("Source Pages")).to_be_visible(timeout=ANSWER_TIMEOUT_MS)
    expect(answer).to_contain_text("kabul", ignore_case=True)
    expect(answer).to_contain_text("doc1.pdf p.51")

    images = answer.locator('img[src*="/media/"]')
    expect(images.first).to_be_visible()
    for i in range(images.count()):
        image = images.nth(i)
        assert image.evaluate("img => img.complete && img.naturalWidth > 0"), "a source image did not load"
        assert page.request.get(image.get_attribute("src")).ok


def test_search_details_show_queries_and_ranked_chunks(page):
    expect = playwright.expect
    answer = page.locator('[data-testid="stChatMessage"]').nth(1)
    answer.get_by_text("Search details").click()
    expect(answer.get_by_text("Queries:")).to_be_visible()
    expect(answer).to_contain_text("rerank")


def test_english_follow_up_question(page):
    expect = playwright.expect
    page.get_by_placeholder("Ask a question about your documents").fill("What does full neuron coverage require?")
    page.keyboard.press("Enter")
    answer = page.locator('[data-testid="stChatMessage"]').nth(3)
    expect(answer.get_by_text("Source Pages")).to_be_visible(timeout=ANSWER_TIMEOUT_MS)
    expect(answer).to_contain_text("zero")
    expect(answer).to_contain_text("doc1.pdf p.47")
    expect(answer.locator('img[src*="/media/"]').first).to_be_visible()


def test_turkish_refusal_is_in_turkish_without_sources(page):
    expect = playwright.expect
    page.get_by_placeholder("Ask a question about your documents").fill("Kubernetes'te bir pod nasıl yeniden başlatılır?")
    page.keyboard.press("Enter")
    answer = page.locator('[data-testid="stChatMessage"]').nth(5)
    expect(answer).to_contain_text("Belgelerde bu konuda bilgi yok.", timeout=ANSWER_TIMEOUT_MS)
    expect(answer.get_by_text("Source Pages")).to_have_count(0)
