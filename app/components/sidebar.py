"""
app/components/sidebar.py
Shared sidebar rendered on every page — aesthetic dark design + Important Questions.
"""
import streamlit as st
from core.watsonx_client import WatsonxClient


def _get_important_questions(text: str, doc_name: str) -> list[str]:
    """Generate 5 important questions from the document text using AI."""
    cache_key = f"_iq_{doc_name}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    prompt = (
        "You are a study assistant. Based on the following text, generate exactly "
        "5 important exam-style questions that a student should be able to answer. "
        "Return ONLY a numbered list (1. ... 2. ... etc.), no extra text.\n\n"
        f"Text (first 2000 chars):\n{text[:2000]}"
    )
    try:
        client = WatsonxClient()
        raw = client.generate(prompt, max_tokens=400)
        lines = [
            l.strip().lstrip("0123456789.-) ").strip()
            for l in raw.strip().splitlines()
            if l.strip() and l.strip()[0].isdigit()
        ]
        questions = lines[:5] if lines else ["Could not generate questions."]
    except Exception:
        questions = ["AI unavailable."]

    st.session_state[cache_key] = questions
    return questions


def render_sidebar() -> None:
    """Render the navigation sidebar with aesthetic design and important questions."""
    with st.sidebar:
        # ── Brand header ──────────────────────────────────────────────────────
        st.markdown(
            """
            <div class="sb-brand">
                <div class="sb-logo">🎓</div>
                <div class="sb-title">Smart Study Agent</div>
                <div class="sb-sub">IBM Granite · watsonx.ai</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Navigation ────────────────────────────────────────────────────────
        st.markdown('<div class="sb-section-label">NAVIGATE</div>', unsafe_allow_html=True)

        nav_items = [
            ("main.py",                "🏠", "Home"),
            ("pages/01_upload.py",     "📤", "Upload Document"),
            ("pages/02_summary.py",    "📝", "Chapter Summary"),
            ("pages/03_flashcards.py", "🃏", "Flashcards"),
            ("pages/04_quiz.py",       "❓", "Quiz Generator"),
            ("pages/05_qa.py",         "💬", "Ask a Question"),
            ("pages/06_planner.py",    "📅", "Study Planner"),
            ("pages/07_dashboard.py",  "📊", "Progress Dashboard"),
        ]
        for path, icon, label in nav_items:
            st.page_link(path, label=f"{icon}  {label}")

        # ── Session quick-stats ───────────────────────────────────────────────
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-section-label">SESSION STATS</div>', unsafe_allow_html=True)

        docs   = st.session_state.get("uploaded_docs", [])
        cards  = sum(len(v) for v in st.session_state.get("flashcards", {}).values())
        quests = sum(len(v) for v in st.session_state.get("quizzes", {}).values())
        done   = len(st.session_state.get("progress", {}).get("completed", []))

        st.markdown(
            f"""
            <div class="sb-stats-grid">
                <div class="sb-stat"><span class="sb-stat-val">{len(docs)}</span><span class="sb-stat-lbl">📄 Docs</span></div>
                <div class="sb-stat"><span class="sb-stat-val">{cards}</span><span class="sb-stat-lbl">🃏 Cards</span></div>
                <div class="sb-stat"><span class="sb-stat-val">{quests}</span><span class="sb-stat-lbl">❓ Quizzes</span></div>
                <div class="sb-stat"><span class="sb-stat-val">{done}</span><span class="sb-stat-lbl">✅ Done</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Important Questions ───────────────────────────────────────────────
        st.markdown('<div class="sb-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-section-label">🔥 IMPORTANT QUESTIONS</div>', unsafe_allow_html=True)

        if not docs:
            st.markdown(
                '<div class="sb-iq-empty">Upload a document to see important questions here.</div>',
                unsafe_allow_html=True,
            )
        else:
            doc_names = [d["name"] for d in docs]
            selected_doc = st.selectbox(
                "Topic",
                doc_names,
                key="sb_iq_doc",
                label_visibility="collapsed",
            )

            col_gen, col_clear = st.columns([3, 1])
            with col_gen:
                gen_btn = st.button("✨ Generate", key="sb_iq_gen", use_container_width=True)
            with col_clear:
                if st.button("🗑️", key="sb_iq_clear", help="Clear questions"):
                    st.session_state.pop(f"_iq_{selected_doc}", None)
                    st.rerun()

            if gen_btn:
                doc_text = next(d["text"] for d in docs if d["name"] == selected_doc)
                with st.spinner("Generating…"):
                    st.session_state.pop(f"_iq_{selected_doc}", None)
                    _get_important_questions(doc_text, selected_doc)
                st.rerun()

            qs = st.session_state.get(f"_iq_{selected_doc}")
            if qs:
                for i, q in enumerate(qs, 1):
                    st.markdown(
                        f'<div class="sb-iq-item"><span class="sb-iq-num">{i}</span>{q}</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    '<div class="sb-iq-empty">Click ✨ Generate to get important questions.</div>',
                    unsafe_allow_html=True,
                )

        # ── Footer ────────────────────────────────────────────────────────────
        st.markdown(
            '<div class="sb-footer">IBM watsonx.ai · Problem Statement #13</div>',
            unsafe_allow_html=True,
        )
