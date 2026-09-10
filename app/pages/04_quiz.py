"""
app/pages/04_quiz.py
MCQ Quiz page — interactive quiz with scoring.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from core.session_state import init_session
from agents.quiz_agent import QuizAgent
from app.components.styles import inject_css

inject_css()
init_session()

st.title("❓ MCQ Quiz Generator")
st.markdown(
    "Test your understanding with AI-generated multiple-choice questions "
    "powered by **IBM Granite**."
)

docs = st.session_state["uploaded_docs"]
if not docs:
    st.warning("⬅️ Upload a document first.")
    st.stop()

doc_names = [d["name"] for d in docs]
selected = st.selectbox("📄 Select document", doc_names)
doc = next(d for d in docs if d["name"] == selected)

num_q = st.slider("Number of questions", 3, 10, 5)

col1, col2 = st.columns(2)
with col1:
    if st.button("🎯 Generate Quiz", type="primary"):
        with st.spinner("Creating quiz with IBM Granite…"):
            agent = QuizAgent()
            questions = agent.generate_quiz(doc["text"], num_questions=num_q)
            st.session_state["quizzes"][selected] = questions
            st.session_state[f"quiz_answers_{selected}"] = {}
            st.session_state[f"quiz_submitted_{selected}"] = False

questions = st.session_state["quizzes"].get(selected, [])
if not questions:
    st.info("Click **Generate Quiz** to begin.")
    st.stop()

key_ans = f"quiz_answers_{selected}"
key_sub = f"quiz_submitted_{selected}"

if key_ans not in st.session_state:
    st.session_state[key_ans] = {}
if key_sub not in st.session_state:
    st.session_state[key_sub] = False

submitted = st.session_state[key_sub]

st.markdown(f"### 📋 Quiz — {len(questions)} Questions")
st.markdown("---")

for i, q in enumerate(questions):
    st.markdown(f"**Q{i+1}. {q['question']}**")
    opts = q.get("options", {})
    option_list = [f"{k}. {v}" for k, v in opts.items()]

    if not submitted:
        choice = st.radio(
            f"Your answer for Q{i+1}",
            option_list,
            key=f"q_{selected}_{i}",
            label_visibility="collapsed",
        )
        st.session_state[key_ans][i] = choice[0] if choice else None
    else:
        user_ans = st.session_state[key_ans].get(i, "")
        correct = q.get("answer", "")
        is_correct = (user_ans == correct)

        for opt in option_list:
            letter = opt[0]
            if letter == correct and letter == user_ans:
                st.markdown(f"✅ **{opt}** ← Your answer (Correct!)")
            elif letter == correct:
                st.markdown(f"✅ **{opt}** ← Correct answer")
            elif letter == user_ans:
                st.markdown(f"❌ ~~{opt}~~ ← Your answer")
            else:
                st.markdown(f"&nbsp;&nbsp;&nbsp;{opt}")

        if q.get("explanation"):
            st.caption(f"💡 {q['explanation']}")
    st.markdown("")

if not submitted:
    if st.button("✅ Submit Quiz", type="primary"):
        st.session_state[key_sub] = True
        st.rerun()
else:
    # Score
    score = sum(
        1
        for i, q in enumerate(questions)
        if st.session_state[key_ans].get(i) == q.get("answer")
    )
    pct = round(score / len(questions) * 100)
    st.markdown("---")
    st.markdown(f"### 🏆 Score: {score} / {len(questions)} ({pct}%)")

    if pct >= 80:
        st.success("🌟 Excellent! You have a strong grasp of this topic.")
    elif pct >= 50:
        st.warning("📚 Good effort! Review the incorrect answers above.")
    else:
        st.error("🔄 Needs improvement. Consider re-reading the material and retrying.")
        # Flag as weak area
        if selected not in st.session_state["progress"]["weak_areas"]:
            st.session_state["progress"]["weak_areas"].append(selected)

    if st.button("🔄 Retake Quiz"):
        st.session_state[key_ans] = {}
        st.session_state[key_sub] = False
        st.rerun()
