"""
app/pages/07_dashboard.py
Progress Dashboard — completed topics, weak areas, milestones.
Uses Plotly for visual charts.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from core.session_state import init_session
from app.components.styles import inject_css

inject_css()
init_session()

st.title("📊 Progress Dashboard")
st.markdown("Track your study milestones, identify weak areas, and celebrate progress.")

progress = st.session_state["progress"]
completed = progress.get("completed", [])
weak      = progress.get("weak_areas", [])
milestone = progress.get("milestones", [])
topics    = st.session_state.get("topics", [])
docs      = st.session_state.get("uploaded_docs", [])
cards     = sum(len(v) for v in st.session_state.get("flashcards", {}).values())
quests    = sum(len(v) for v in st.session_state.get("quizzes", {}).values())
qa_count  = len(st.session_state.get("qa_history", []))

# ── KPI row ────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📄 Docs Uploaded",    len(docs))
k2.metric("✅ Topics Completed", len(completed))
k3.metric("⚠️ Weak Areas",      len(weak))
k4.metric("🃏 Flashcards",       cards)
k5.metric("❓ Quiz Questions",   quests)

st.markdown("---")

# ── Topic progress pie ─────────────────────────────────────────────────────────
all_topics = list(set(topics + [d["name"] for d in docs]))

if all_topics:
    n_done = len([t for t in all_topics if t in completed])
    n_pending = len(all_topics) - n_done

    fig_pie = go.Figure(
        go.Pie(
            labels=["Completed", "Pending"],
            values=[max(n_done, 0.001), max(n_pending, 0.001)],
            hole=0.55,
            marker_colors=["#057a55", "#e5e7eb"],
            textinfo="label+percent",
        )
    )
    fig_pie.update_layout(
        title="Topic Completion",
        height=320,
        margin=dict(t=40, b=10, l=10, r=10),
        showlegend=False,
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("Add topics in the **Study Planner** to see completion stats.")

# ── Activity bar chart ─────────────────────────────────────────────────────────
st.markdown("### 📈 Activity Overview")
activity_labels = ["Docs Uploaded", "Summaries", "Flashcard Sets", "Quiz Sets", "Q&A Queries"]
activity_values = [
    len(docs),
    len(st.session_state.get("summaries", {})),
    len(st.session_state.get("flashcards", {})),
    len(st.session_state.get("quizzes", {})),
    qa_count,
]
fig_bar = px.bar(
    x=activity_labels,
    y=activity_values,
    color=activity_labels,
    color_discrete_sequence=["#1a56db", "#7e3af2", "#057a55", "#c27803", "#0891b2"],
    labels={"x": "Activity", "y": "Count"},
)
fig_bar.update_layout(
    height=300,
    margin=dict(t=10, b=10),
    showlegend=False,
)
st.plotly_chart(fig_bar, use_container_width=True)

# ── Weak areas ─────────────────────────────────────────────────────────────────
st.markdown("### ⚠️ Weak Areas (Need Revision)")
if weak:
    for w in weak:
        st.markdown(
            f'<span class="badge badge-red">⚠ {w}</span>&nbsp;',
            unsafe_allow_html=True,
        )
else:
    st.success("🎉 No weak areas identified yet. Keep quizzing!")

# ── Milestones ─────────────────────────────────────────────────────────────────
st.markdown("### 🏁 Study Milestones")
if milestone:
    for i, m in enumerate(milestone):
        st.markdown(f"🏆 Milestone {i+1}: {m}")
else:
    st.info("Milestones will appear after generating a study plan.")

# ── Completed topics ───────────────────────────────────────────────────────────
st.markdown("### ✅ Completed Topics")
if completed:
    for c in completed:
        st.markdown(
            f'<span class="badge badge-green">✅ {c}</span>&nbsp;',
            unsafe_allow_html=True,
        )
else:
    st.info("Complete summaries and quizzes to mark topics as done.")

# ── Manual controls ────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### ✏️ Manual Progress Update")
col_add, col_weak = st.columns(2)
with col_add:
    new_topic = st.text_input("Mark topic as completed")
    if st.button("✅ Mark Complete") and new_topic:
        if new_topic not in st.session_state["progress"]["completed"]:
            st.session_state["progress"]["completed"].append(new_topic)
        st.rerun()
with col_weak:
    new_weak = st.text_input("Flag as weak area")
    if st.button("⚠️ Add Weak Area") and new_weak:
        if new_weak not in st.session_state["progress"]["weak_areas"]:
            st.session_state["progress"]["weak_areas"].append(new_weak)
        st.rerun()
