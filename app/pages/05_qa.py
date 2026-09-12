"""
app/pages/05_qa.py
RAG-powered Q&A page — asks questions answered from uploaded docs.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from core.session_state import init_session, get_vs
from core.watsonx_client import WatsonxClient
from app.components.styles import inject_css
from app.components.sidebar import render_sidebar

inject_css()
init_session()
render_sidebar()

st.title("💬 Ask a Question (RAG)")
st.markdown(
    "Ask anything about your uploaded documents. The system retrieves the "
    "most relevant passages and uses **IBM Granite** to answer accurately."
)

if not st.session_state["uploaded_docs"]:
    st.warning("⬅️ Upload a document first.")
    st.stop()

if get_vs().count == 0:
    st.warning("Vector store is empty. Please re-upload your documents.")
    st.stop()

RAG_PROMPT = """\
You are a helpful academic assistant. Answer the student's question using ONLY
the context passages provided below. If the answer is not in the context, say
"I could not find that information in the uploaded material."

Context:
---
{context}
---

Student Question: {question}

Answer (clear, concise, student-friendly):
"""

# ── Chat history ───────────────────────────────────────────────────────────────
for chat in st.session_state["qa_history"]:
    with st.chat_message("user"):
        st.markdown(chat["q"])
    with st.chat_message("assistant"):
        st.markdown(chat["a"])

# ── Input ──────────────────────────────────────────────────────────────────────
question = st.chat_input("Ask a question about your study material…")

if question:
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching documents and generating answer…"):
            vs = get_vs()
            chunks = vs.query(question, n_results=4)
            context = "\n\n".join(chunks)

            llm = WatsonxClient()
            prompt = RAG_PROMPT.format(context=context[:3000], question=question)
            answer = llm.generate(prompt, max_tokens=512)

        st.markdown(answer)

        with st.expander("📎 Source passages used"):
            for j, c in enumerate(chunks):
                st.caption(f"Passage {j+1}: {c[:300]}…")

    st.session_state["qa_history"].append({"q": question, "a": answer})

# ── Clear chat ─────────────────────────────────────────────────────────────────
if st.session_state["qa_history"]:
    if st.button("🗑️ Clear Chat History"):
        st.session_state["qa_history"] = []
        st.rerun()
