"""
core/session_state.py
Streamlit session-state helpers to avoid repeated re-initialisation.
"""
import streamlit as st
from core.vector_store import VectorStore


def init_session():
    """Initialise all required session-state keys on first load."""
    defaults = {
        "uploaded_docs":        [],     # list of {"name": str, "text": str, "chunks": int}
        "vector_store":         None,   # VectorStore instance
        "summaries":            {},     # doc_name -> summary text
        "flashcards":           {},     # doc_name -> list[{"term":, "definition":}]
        "quizzes":              {},     # doc_name -> list[{"question":, "options":[], "answer":}]
        "study_plan":           None,   # structured study plan dict
        "progress": {
            "completed":  [],
            "weak_areas": [],
            "milestones": [],
        },
        "exam_date":            None,
        "study_hours_per_day":  2,
        "topics":               [],
        "qa_history":           [],     # list[{"q": str, "a": str}]
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    # Lazy-init persistent vector store
    if st.session_state["vector_store"] is None:
        st.session_state["vector_store"] = VectorStore()

    # Show credential status banner
    _show_credential_banner()


def _show_credential_banner():
    """Display a status banner showing which AI backend is active."""
    from core.watsonx_client import WatsonxClient
    client = WatsonxClient()
    if client.is_ready:
        labels = {"groq": "Groq", "grok": "Grok (xAI)", "watsonx": "IBM watsonx.ai"}
        backend_label = labels.get(client.backend, client.backend)
        st.success(f"✅ Connected to **{backend_label}** — AI features are live!", icon="🤖")
    else:
        st.warning(
            "**No AI backend connected.** "
            "Add `GROQ_API_KEY` to your `.env` file (free at console.groq.com), "
            "or set `WATSONX_API_KEY` + `WATSONX_PROJECT_ID` for IBM watsonx.ai. "
            "Then restart the app.",
            icon="⚠️",
        )


def get_vs() -> VectorStore:
    """Return the shared VectorStore instance."""
    return st.session_state["vector_store"]
