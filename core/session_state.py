"""
core/session_state.py
Streamlit session-state helpers.
VectorStore is created once per server process via st.cache_resource,
so the 40-second model-load only happens on the very first page hit.
"""
import streamlit as st


@st.cache_resource(show_spinner="Loading AI vector store…")
def _get_vector_store():
    """Create VectorStore once per server process and cache it."""
    from core.vector_store import VectorStore
    return VectorStore()


def init_session():
    """Initialise all required session-state keys on first load."""
    defaults = {
        "uploaded_docs":        [],
        "summaries":            {},
        "flashcards":           {},
        "quizzes":              {},
        "study_plan":           None,
        "progress": {
            "completed":  [],
            "weak_areas": [],
            "milestones": [],
        },
        "exam_date":            None,
        "study_hours_per_day":  2,
        "topics":               [],
        "qa_history":           [],
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

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


def get_vs():
    """Return the shared cached VectorStore instance."""
    return _get_vector_store()
