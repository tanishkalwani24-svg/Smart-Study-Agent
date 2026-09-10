"""
app/pages/02_summary.py
Chapter Summary page — generates Granite-powered summaries.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from core.session_state import init_session
from agents.summary_agent import SummaryAgent
from app.components.styles import inject_css

inject_css()
init_session()

st.title("📝 Chapter Summary")
st.markdown(
    "Select a document and generate a concise, student-friendly summary "
    "using **IBM Granite** via watsonx.ai."
)

docs = st.session_state["uploaded_docs"]
if not docs:
    st.warning("⬅️ Upload a document first on the **Upload** page.")
    st.stop()

doc_names = [d["name"] for d in docs]
selected = st.selectbox("📄 Select document", doc_names)
doc = next(d for d in docs if d["name"] == selected)

cached = st.session_state["summaries"].get(selected)

col1, col2 = st.columns([3, 1])
with col2:
    force = st.checkbox("🔄 Regenerate", value=False)

if st.button("✨ Generate Summary", type="primary") or (cached and not force):
    if cached and not force:
        st.markdown("#### 📋 Summary")
        st.markdown(cached)
    else:
        with st.spinner("IBM Granite is reading your document…"):
            agent = SummaryAgent()
            summary = agent.summarise(doc["text"])
            st.session_state["summaries"][selected] = summary

        st.markdown("#### 📋 Summary")
        st.markdown(summary)

        # Mark topic as partially done
        if selected not in st.session_state["progress"]["completed"]:
            st.session_state["progress"]["completed"].append(selected)

st.markdown("---")
if st.session_state["summaries"]:
    st.subheader("🗂️ Previously Generated Summaries")
    for name, summ in st.session_state["summaries"].items():
        with st.expander(name):
            st.markdown(summ)
