"""
app/components/sidebar.py
Shared sidebar rendered on every page.
"""
import streamlit as st


def render_sidebar() -> None:
    """Render the navigation sidebar with status indicators."""
    with st.sidebar:
        st.markdown(
            """
            <div style="text-align:center;padding:1rem 0 .5rem 0;">
                <span style="font-size:2rem;">🎓</span><br>
                <strong style="font-size:1rem;color:#1a56db;">Smart Study Agent</strong><br>
                <small style="color:#6b7280;">IBM Granite · watsonx.ai</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        st.markdown("### 📂 Navigation")
        st.page_link("main.py",                    label="🏠 Home")
        st.page_link("pages/01_upload.py",         label="📤 Upload Document")
        st.page_link("pages/02_summary.py",        label="📝 Chapter Summary")
        st.page_link("pages/03_flashcards.py",     label="🃏 Flashcards")
        st.page_link("pages/04_quiz.py",           label="❓ Quiz Generator")
        st.page_link("pages/05_qa.py",             label="💬 Ask a Question")
        st.page_link("pages/06_planner.py",        label="📅 Study Planner")
        st.page_link("pages/07_dashboard.py",      label="📊 Progress Dashboard")

        st.markdown("---")

        # ── Session quick-stats ────────────────────────────────────────────────
        docs   = len(st.session_state.get("uploaded_docs", []))
        cards  = sum(len(v) for v in st.session_state.get("flashcards", {}).values())
        quests = sum(len(v) for v in st.session_state.get("quizzes", {}).values())
        done   = len(st.session_state.get("progress", {}).get("completed", []))

        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        col1.metric("📄 Docs",       docs)
        col2.metric("✅ Done",        done)
        col1.metric("🃏 Cards",      cards)
        col2.metric("❓ Questions",  quests)

        st.markdown("---")
        st.caption("IBM watsonx.ai · Problem Statement #13")
