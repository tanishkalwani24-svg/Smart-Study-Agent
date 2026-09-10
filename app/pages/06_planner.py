"""
app/pages/06_planner.py
Study Planner page — personalised study schedule based on exam date.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from datetime import date, timedelta
from core.session_state import init_session
from agents.planner_agent import StudyPlannerAgent
from app.components.styles import inject_css

inject_css()
init_session()

st.title("📅 Personalised Study Planner")
st.markdown(
    "Tell us your exam date and available study time. "
    "IBM Granite will build a realistic day-by-day study schedule."
)

# ── Input form ─────────────────────────────────────────────────────────────────
with st.form("planner_form"):
    col1, col2 = st.columns(2)
    with col1:
        exam_date = st.date_input(
            "📅 Exam Date",
            value=date.today() + timedelta(days=14),
            min_value=date.today() + timedelta(days=1),
        )
    with col2:
        hours = st.number_input(
            "⏰ Study Hours Per Day", min_value=1.0, max_value=12.0, value=3.0, step=0.5
        )

    topics_raw = st.text_area(
        "📚 Topics to Cover (one per line)",
        placeholder="Operating Systems\nData Structures\nDBMS\nComputer Networks",
        height=120,
    )
    weak_raw = st.text_area(
        "⚠️ Weak Areas (one per line, optional)",
        placeholder="Recursion\nNormalisation",
        height=80,
    )
    submitted = st.form_submit_button("📅 Generate Study Plan", type="primary")

if submitted:
    topics = [t.strip() for t in topics_raw.splitlines() if t.strip()]
    weak = [t.strip() for t in weak_raw.splitlines() if t.strip()]

    if not topics:
        st.error("Please enter at least one topic.")
        st.stop()

    # Persist for dashboard
    st.session_state["exam_date"] = exam_date
    st.session_state["study_hours_per_day"] = hours
    st.session_state["topics"] = topics

    with st.spinner("Building your personalised study plan…"):
        agent = StudyPlannerAgent()
        plan = agent.generate_plan(
            exam_date=exam_date,
            hours_per_day=hours,
            topics=topics,
            weak_areas=weak,
        )
        st.session_state["study_plan"] = plan

        # Auto-populate milestones
        milestones = plan.get("milestones", [])
        st.session_state["progress"]["milestones"] = [m.get("milestone", "") for m in milestones]

plan = st.session_state.get("study_plan")

if not plan:
    st.info("Fill in the form above and click **Generate Study Plan**.")
    st.stop()

if "error" in plan:
    st.error(f"Could not generate plan: {plan['error']}")
    with st.expander("Raw response"):
        st.text(plan.get("raw", ""))
    st.stop()

# ── Plan display ───────────────────────────────────────────────────────────────
total_days = plan.get("total_days", "?")
daily = plan.get("daily_plan", [])
milestones = plan.get("milestones", [])
tips = plan.get("overall_tips", [])

st.success(f"✅ {total_days}-day study plan generated!")

# Timeline
st.markdown("### 🗓️ Daily Schedule")
for day_plan in daily:
    day_num   = day_plan.get("day", "?")
    day_date  = day_plan.get("date", "")
    focus     = ", ".join(day_plan.get("focus_topics", []))
    hrs       = day_plan.get("hours_allocated", hours)
    tasks     = day_plan.get("tasks", [])
    tip       = day_plan.get("tip", "")

    with st.expander(f"📅 Day {day_num}  —  {day_date}  |  {focus}  ({hrs}h)"):
        for t in tasks:
            st.markdown(f"- {t}")
        if tip:
            st.caption(f"💡 Tip: {tip}")

# Milestones
if milestones:
    st.markdown("### 🏁 Milestones")
    for m in milestones:
        st.markdown(f"- **Day {m.get('day')}**: {m.get('milestone')}")

# Overall tips
if tips:
    st.markdown("### 🧠 Overall Study Tips")
    for t in tips:
        st.markdown(f"✔ {t}")
