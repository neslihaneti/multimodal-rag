import itertools
import os

from dotenv import load_dotenv
load_dotenv()

import streamlit as st

import db
import rag
from file_processing import list_pdfs
from indexer import index_folder


st.set_page_config(layout="wide")
db.create_tables()

# Sidebar for folder selection
st.sidebar.title("📁 Data Source")

selected_folder = st.sidebar.text_input(
    "Enter folder path:",
    value=os.path.expanduser("~"),
    help="Select a local folder containing PDF files"
)

if os.path.isdir(selected_folder):
    pdf_files = [os.path.basename(p) for p in list_pdfs(selected_folder)]
    st.sidebar.success(f"✓ Folder loaded: {len(pdf_files)} PDF(s) found")
    if pdf_files:
        st.sidebar.write("**PDFs in folder:**")
        for pdf in pdf_files:
            st.sidebar.text(f"• {pdf}")
    st.session_state.data_folder = selected_folder
else:
    st.sidebar.warning("⚠️ Please enter a valid folder path")
    st.session_state.data_folder = None

st.sidebar.divider()

if st.sidebar.button("🔄 Extract & Index PDFs", use_container_width=True):
    if st.session_state.data_folder:
        progress_bar = st.sidebar.progress(0.0)
        status_text = st.sidebar.empty()

        def on_progress(message, fraction):
            progress_bar.progress(min(fraction, 1.0))
            status_text.text(message)

        try:
            summary = index_folder(st.session_state.data_folder, on_progress)
            progress_bar.empty()
            status_text.empty()
            st.sidebar.success(f"✓ Indexed {len(summary['indexed'])} PDF(s), skipped {len(summary['skipped'])} already indexed")
        except Exception as e:
            st.sidebar.error(f"Error processing PDFs: {e}")
    else:
        st.sidebar.error("Please select a valid folder first")

indexed = db.list_documents()
if indexed:
    st.sidebar.divider()
    st.sidebar.write("**Indexed documents:**")
    for file_name, pages, chunks in indexed:
        st.sidebar.text(f"• {file_name} ({pages} pages, {chunks} chunks)")


def show_sources(sources):
    if not sources:
        return
    st.markdown("**📄 Source Pages:**")
    st.image(
        [s["image_path"] for s in sources],
        width=200,
        caption=[f"{s['file_name']} p.{s['page_number']}" for s in sources],
    )


st.title("RAG Chatbot with Source Images")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        show_sources(message.get("sources"))

# RAG akisi: soru sohbet gecmisine gore yeniden yaziliyor, hibrit arama + reranker ile parcalar bulunuyor,
# model gerekirse yeni sorguyla tekrar arıyor, sonra parcalar ve sayfa goruntuleriyle tek seferde cevap uretiliyor.
if prompt := st.chat_input("Ask a question about your documents"):
    history = [(m["role"], m["content"]) for m in st.session_state.messages]
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        result = {}

        def answer_text():
            for item in rag.answer_stream(prompt, history):
                if isinstance(item, dict):
                    result.update(item)
                else:
                    yield item

        # The answer is shown as the model writes it; the spinner covers the search until its first words
        stream = answer_text()
        with st.spinner("Searching and reading your documents..."):
            first = next(stream, "")
        st.write_stream(itertools.chain([first], stream))
        show_sources(result["sources"])
        with st.expander("Search details"):
            st.markdown("**Queries:** " + " → ".join(f"`{q}`" for q in result["queries"]))
            for i, chunk in enumerate(result["chunks"], 1):
                st.markdown(f"**[{i}]** {chunk['file_name']} p.{chunk['page_number']} · rerank {chunk['rerank_score']:.3f}")
                st.caption(chunk["content"][:400])

    st.session_state.messages.append({"role": "assistant", "content": result["answer"], "sources": result["sources"]})
