"""Streamlit runner for the Session 18 deployment app.

Run from the repository root:

    streamlit run App/streamlit_app.py
"""

import time

import streamlit as st

from helpers.chunks import chunk_rag_records
from helpers.duplicates import remove_duplicate_text_from_inventory
from helpers.inventory import build_page_inventory
from helpers.qa import answer_question, retrieve
from helpers.records import build_rag_records
from helpers.storage import require_config, save_records_to_supabase
from helpers.uploads import save_uploaded_pdf


TRAINING_MESSAGE_SECONDS = 0.8

st.set_page_config(page_title="Multi Page RAG", layout="centered")
st.title("Multi Page PDF RAG")
st.caption("Upload a PDF, create embeddings, store them in Supabase, and ask grounded questions.")

uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])

try:
    require_config()
    config_ready = True
except RuntimeError as error:
    config_ready = False
    st.error(str(error))

train_disabled = uploaded_pdf is None or not config_ready

if st.button("Train", type="primary", disabled=train_disabled):
    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.info("Checking uploaded PDF...")
    progress_bar.progress(5)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    status_text.info("Saving uploaded PDF...")
    pdf_path = save_uploaded_pdf(uploaded_pdf)
    progress_bar.progress(12)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    status_text.info("Starting page-by-page scan...")
    progress_bar.progress(18)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    status_text.info("Finding text, tables, and image pages...")
    page_inventory = build_page_inventory(pdf_path)
    progress_bar.progress(38)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    status_text.info("Vision ran only if an image page was found.")
    progress_bar.progress(44)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    status_text.info("Removing repeated table text...")
    page_inventory = remove_duplicate_text_from_inventory(page_inventory)
    progress_bar.progress(55)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    status_text.info("Preparing clean text for search...")
    progress_bar.progress(62)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    status_text.info("Building RAG records...")
    rag_records = build_rag_records(page_inventory)
    progress_bar.progress(70)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    status_text.info("Splitting records into smaller chunks...")
    chunked_records = chunk_rag_records(rag_records)
    progress_bar.progress(82)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    if not chunked_records:
        progress_bar.empty()
        status_text.error("No extractable text was found in this PDF.")
        st.stop()

    status_text.info("Creating embeddings for the chunks...")
    progress_bar.progress(88)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    status_text.info("Uploading embeddings to Supabase...")
    inserted_count = save_records_to_supabase(chunked_records)
    progress_bar.progress(100)
    time.sleep(TRAINING_MESSAGE_SECONDS)

    st.session_state["trained"] = True
    st.session_state["pdf_name"] = uploaded_pdf.name
    st.session_state["inserted_count"] = inserted_count
    progress_bar.empty()
    status_text.success("Training complete. Ask a question below.")

if st.session_state.get("trained"):
    st.divider()
    st.success(f"Stored {st.session_state['inserted_count']} chunks from {st.session_state['pdf_name']}.")
    question = st.text_input("Ask a question")

    if st.button("Ask", disabled=not question.strip()):
        with st.spinner("Thinking..."):
            retrieved_rows = retrieve(question, top_k=4)
            answer = answer_question(question, retrieved_rows)

        st.write(answer)
