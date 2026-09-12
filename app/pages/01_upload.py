"""
app/pages/01_upload.py
Document Upload page — PDF, image, or text files.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from core.session_state import init_session, get_vs
from core.document_loader import load_document, chunk_text
from app.components.styles import inject_css
from app.components.sidebar import render_sidebar

inject_css()
init_session()
render_sidebar()

st.title("📤 Upload Study Material")
st.markdown(
    "Upload your **PDF, notes (.txt/.md), or textbook images** "
    "to power all study tools."
)

# ── Upload widget ──────────────────────────────────────────────────────────────
uploaded_files = st.file_uploader(
    "Choose files",
    type=["pdf", "txt", "md", "png", "jpg", "jpeg", "webp"],
    accept_multiple_files=True,
    help="Max 50 MB per file. PDFs, plain text, Markdown, and images are supported.",
)

if uploaded_files:
    for uf in uploaded_files:
        # Skip already-uploaded docs
        existing_names = [d["name"] for d in st.session_state["uploaded_docs"]]
        if uf.name in existing_names:
            st.info(f"✅ **{uf.name}** already uploaded.")
            continue

        with st.spinner(f"Processing **{uf.name}**…"):
            try:
                raw_bytes = uf.read()
                text = load_document(uf.name, raw_bytes)
                chunks = chunk_text(text)

                # Index into vector store
                vs = get_vs()
                vs.add_chunks(chunks, doc_name=uf.name)

                # Save to session
                st.session_state["uploaded_docs"].append(
                    {"name": uf.name, "text": text, "chunks": len(chunks)}
                )
                st.success(
                    f"✅ **{uf.name}** processed — {len(chunks)} chunks indexed."
                )
            except Exception as e:
                st.error(f"❌ Error processing **{uf.name}**: {e}")

# ── Uploaded docs table ───────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📚 Uploaded Documents")

if not st.session_state["uploaded_docs"]:
    st.info("No documents uploaded yet. Use the uploader above.")
else:
    for doc in st.session_state["uploaded_docs"]:
        with st.expander(f"📄 {doc['name']}  —  {doc['chunks']} chunks"):
            preview = doc["text"][:800]
            st.text(preview + ("…" if len(doc["text"]) > 800 else ""))

    if st.button("🗑️ Clear All Documents", type="secondary"):
        st.session_state["uploaded_docs"] = []
        get_vs().reset()
        st.success("All documents cleared.")
        st.rerun()
