"""
app/pages/03_flashcards.py
Flashcard viewer — interactive flip-card style UI.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from core.session_state import init_session
from agents.flashcard_agent import FlashcardAgent
from app.components.styles import inject_css

inject_css()
init_session()

st.title("🃏 Flashcards")
st.markdown(
    "Auto-generate term-definition flashcards from your uploaded material. "
    "Click **Flip** to reveal the definition."
)

docs = st.session_state["uploaded_docs"]
if not docs:
    st.warning("⬅️ Upload a document first.")
    st.stop()

doc_names = [d["name"] for d in docs]
selected = st.selectbox("📄 Select document", doc_names)
doc = next(d for d in docs if d["name"] == selected)

num_cards = st.slider("Number of flashcards", 5, 20, 10)

if st.button("🃏 Generate Flashcards", type="primary"):
    with st.spinner("Generating flashcards with IBM Granite…"):
        agent = FlashcardAgent()
        cards = agent.generate_flashcards(doc["text"], num_cards=num_cards)
        st.session_state["flashcards"][selected] = cards

cards = st.session_state["flashcards"].get(selected, [])

if not cards:
    st.info("Click **Generate Flashcards** above to start.")
    st.stop()

# ── Flashcard navigator ────────────────────────────────────────────────────────
st.markdown(f"**{len(cards)} flashcards** generated for *{selected}*")
st.markdown("---")

if "fc_index" not in st.session_state:
    st.session_state["fc_index"] = 0
if "fc_show_def" not in st.session_state:
    st.session_state["fc_show_def"] = False

idx = st.session_state["fc_index"] % len(cards)
card = cards[idx]

# Card display
if st.session_state["fc_show_def"]:
    st.markdown(
        f'<div class="fc-inner fc-back">📖 {card["definition"]}</div>',
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        f'<div class="fc-inner">💡 {card["term"]}</div>',
        unsafe_allow_html=True,
    )

st.markdown(f"<center><small>{idx + 1} / {len(cards)}</small></center>", unsafe_allow_html=True)
st.markdown("")

btn_col1, btn_col2, btn_col3 = st.columns(3)
with btn_col1:
    if st.button("⬅️ Previous"):
        st.session_state["fc_index"] = (idx - 1) % len(cards)
        st.session_state["fc_show_def"] = False
        st.rerun()
with btn_col2:
    label = "🔍 Show Definition" if not st.session_state["fc_show_def"] else "🔙 Show Term"
    if st.button(label):
        st.session_state["fc_show_def"] = not st.session_state["fc_show_def"]
        st.rerun()
with btn_col3:
    if st.button("➡️ Next"):
        st.session_state["fc_index"] = (idx + 1) % len(cards)
        st.session_state["fc_show_def"] = False
        st.rerun()

# ── All cards table ────────────────────────────────────────────────────────────
with st.expander("📋 View All Flashcards"):
    for i, c in enumerate(cards):
        st.markdown(f"**{i+1}. {c['term']}**")
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{c['definition']}")
        st.markdown("")
