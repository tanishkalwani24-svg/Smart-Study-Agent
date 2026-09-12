"""
app/main.py
Smart Study Generator Agent — Streamlit application entry point.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from core.session_state import init_session
from app.components.styles import inject_css
from app.components.sidebar import render_sidebar

st.set_page_config(
    page_title="Smart Study Generator Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()
init_session()
render_sidebar()

# ── Hero Banner ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
        <h1>🎓 Smart Study Generator Agent</h1>
        <p>Powered by IBM Granite &nbsp;·&nbsp; watsonx.ai &nbsp;·&nbsp; Langflow — Your AI-powered study companion</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Quick-stats row ───────────────────────────────────────────────────────────
docs   = len(st.session_state.get("uploaded_docs", []))
cards  = sum(len(v) for v in st.session_state.get("flashcards", {}).values())
quests = sum(len(v) for v in st.session_state.get("quizzes", {}).values())
done   = len(st.session_state.get("progress", {}).get("completed", []))

col1, col2, col3, col4 = st.columns(4)
col1.metric("📄 Documents Uploaded",   docs)
col2.metric("🃏 Flashcards Generated", cards)
col3.metric("❓ Quiz Questions Ready", quests)
col4.metric("✅ Topics Completed",     done)

st.markdown("---")

# ── Navigation cards ─────────────────────────────────────────────────────────
st.markdown("### 🧭 What would you like to do?")

row1 = st.columns(4)
page_cards = [
    ("fc-blue",   "📤 Upload Document",      "Upload PDFs, notes, or images",           "upload"),
    ("fc-purple", "📝 Chapter Summary",      "AI-generated summaries of your material", "summary"),
    ("fc-green",  "🃏 Flashcards",           "Auto-created term-definition cards",      "flashcards"),
    ("fc-orange", "❓ Quiz Generator",       "MCQ quizzes with instant scoring",        "quiz"),
]
for col, (colour, label, desc, slug) in zip(row1, page_cards):
    col.markdown(
        f'<a href="/{slug}" target="_self" class="fcard-link">'
        f'<div class="fcard {colour}">'
        f'<b>{label}</b>'
        f'<br>'
        f'<small>{desc}</small>'
        f'</div>'
        f'</a>',
        unsafe_allow_html=True,
    )

row2 = st.columns(4)
page_cards2 = [
    ("fc-pink",   "💬 Ask a Question (RAG)", "Chat with your documents via RAG",        "qa"),
    ("fc-teal",   "📅 Study Planner",        "Personalised day-by-day study schedule",  "planner"),
    ("fc-indigo", "📊 Progress Dashboard",   "Track milestones and weak areas",         "dashboard"),
]
for col, (colour, label, desc, slug) in zip(row2, page_cards2):
    col.markdown(
        f'<a href="/{slug}" target="_self" class="fcard-link">'
        f'<div class="fcard {colour}">'
        f'<b>{label}</b>'
        f'<br>'
        f'<small>{desc}</small>'
        f'</div>'
        f'</a>',
        unsafe_allow_html=True,
    )

st.markdown("---")
st.markdown(
    "<small style='color:#94a3b8;'>Smart Study Generator Agent &nbsp;·&nbsp; "
    "IBM watsonx.ai &nbsp;·&nbsp; Problem Statement #13</small>",
    unsafe_allow_html=True,
)
