"""
AI Study Assistant — Smart Learning Tool
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Generate flashcards from any topic/text
- Quiz mode with multiple choice
- Summarize study material
- Create practice questions
- Study planner with spaced repetition
"""

import os
import random
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")
st.title("📚 AI Study Assistant")
st.markdown("Flashcards • Quizzes • Summaries • Practice Questions • Study Planner")

# Session state
if "cards" not in st.session_state:
    st.session_state.cards = []
if "quiz_mode" not in st.session_state:
    st.session_state.quiz_mode = False
if "current_card" not in st.session_state:
    st.session_state.current_card = 0
if "score" not in st.session_state:
    st.session_state.score = {"correct": 0, "total": 0}

# Functions
def generate_flashcards(topic, num_cards, api_key):
    if not api_key:
        return None, "⚠️ Set GOOGLE_API_KEY in .env"

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""Create {num_cards} flashcards about: {topic}

Format each flashcard as:
Q: [Question]
A: [Answer]

Make questions:
- Clear and specific
- Test understanding, not memorization
- Include practical examples where possible

Return ONLY the flashcards in the exact format shown above, no extra text."""

        response = model.generate_content(prompt)
        cards = []
        lines = response.text.split('\n')
        current_q = None
        current_a = None

        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                current_q = line[2:].strip()
            elif line.startswith('A:') and current_q:
                current_a = line[2:].strip()
                cards.append({"question": current_q, "answer": current_a})
                current_q = None
                current_a = None

        return cards, None
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def generate_quiz(topic, num_q, api_key):
    if not api_key:
        return None, "⚠️ Set GOOGLE_API_KEY in .env"

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""Create {num_q} multiple choice quiz questions about: {topic}

Format each question as:
Q: [Question text]
A: [Correct answer]
B: [Wrong answer 1]
C: [Wrong answer 2]
D: [Wrong answer 3]

Make sure:
- Only one correct answer
- Wrong answers are plausible (not obvious)
- Questions test understanding
- Cover different aspects of the topic

Return ONLY the questions in exact format above."""

        response = model.generate_content(prompt)
        questions = []
        lines = response.text.split('\n')
        q_data = {}

        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                q_data['question'] = line[2:].strip()
            elif line.startswith('A:') and 'question' in q_data:
                q_data['correct'] = line[2:].strip()
            elif line.startswith('B:') and 'correct' not in q_data:
                q_data['B'] = line[2:].strip()
            elif line.startswith('C:') and 'B' in q_data:
                q_data['C'] = line[2:].strip()
            elif line.startswith('D:') and 'C' in q_data:
                q_data['D'] = line[2:].strip()
                questions.append(q_data)
                q_data = {}

        return questions, None
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def summarize_text(text, api_key):
    if not api_key:
        return None, "⚠️ Set GOOGLE_API_KEY in .env"

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""Summarize this study material concisely:

{text[:3000]}

Give:
1. Key concepts (bullet points)
2. Important definitions
3. Key formulas or facts
4. Quick memory tricks if applicable"""

        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# UI Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🃏 Flashcards", "📝 Quiz", "📖 Summarize", "📅 Study Planner"])

with tab1:
    st.subheader("🃏 AI Flashcard Generator")

    topic = st.text_input("📚 Topic:", placeholder="e.g., Python Basics, Data Structures, Machine Learning")
    num_cards = st.slider("Number of cards:", 5, 20, 10)

    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        st.warning("⚠️ Set GOOGLE_API_KEY in .env for AI generation")

    col_gen, col_clear = st.columns([1, 1])
    with col_gen:
        generate = st.button("🎯 Generate Flashcards", use_container_width=True)
    with col_clear:
        if st.button("🗑️ Clear Cards", use_container_width=True):
            st.session_state.cards = []
            st.session_state.current_card = 0

    if generate and topic:
        with st.spinner("✨ Generating flashcards..."):
            cards, error = generate_flashcards(topic, num_cards, api_key)

        if error:
            st.error(error)
        else:
            st.session_state.cards = cards
            st.session_state.current_card = 0
            st.success(f"✅ Generated {len(cards)} flashcards!")

    # Flashcard display
    if st.session_state.cards:
        card = st.session_state.cards[st.session_state.current_card]

        st.divider()
        col_prev, col_card, col_next = st.columns([1, 2, 1])

        with col_card:
            with st.container():
                st.markdown(f"<h3 style='text-align:center;'>Card {st.session_state.current_card + 1}/{len(st.session_state.cards)}</h3>",
                           unsafe_allow_html=True)

                if st.session_state.show_answer:
                    st.markdown(f"**❓ Question:**")
                    st.markdown(card['question'])
                    st.divider()
                    st.markdown(f"**💡 Answer:**")
                    st.markdown(card['answer'])

                    if st.button("⬆️ Show Question", use_container_width=True):
                        st.session_state.show_answer = False
                        st.rerun()
                else:
                    st.markdown(f"**❓ Question:**")
                    st.markdown(card['question'])
                    st.markdown("<br>", unsafe_allow_html=True)

                    if st.button("💡 Show Answer", use_container_width=True):
                        st.session_state.show_answer = True
                        st.rerun()

                col_left_btn, col_right_btn = st.columns(2)
                with col_left_btn:
                    if st.button("⬅️ Previous", use_container_width=True):
                        st.session_state.current_card = max(0, st.session_state.current_card - 1)
                        st.session_state.show_answer = False
                        st.rerun()
                with col_right_btn:
                    if st.button("Next ➡️", use_container_width=True):
                        st.session_state.current_card = min(len(st.session_state.cards) - 1, st.session_state.current_card + 1)
                        st.session_state.show_answer = False
                        st.rerun()

                # Shuffle
                if st.button("🔀 Shuffle Cards", use_container_width=True):
                    random.shuffle(st.session_state.cards)
                    st.session_state.current_card = 0
                    st.session_state.show_answer = False
                    st.rerun()

        # Card list
        with st.expander("📋 View All Cards"):
            for i, c in enumerate(st.session_state.cards):
                st.markdown(f"**{i+1}.** {c['question']}")
                st.markdown(f"   → {c['answer']}")
                st.markdown("")
    elif not generate:
        st.info("👆 Generate flashcards or add manually below")

        # Manual card addition
        st.divider()
        st.subheader("➕ Add Card Manually")
        q = st.text_input("Question:")
        a = st.text_input("Answer:")
        if st.button("Add Card", use_container_width=True) and q and a:
            st.session_state.cards.append({"question": q, "answer": a})
            st.success(f"✅ Added! Total: {len(st.session_state.cards)} cards")

with tab2:
    st.subheader("📝 AI Quiz Mode")

    quiz_topic = st.text_input("📚 Quiz Topic:", placeholder="e.g., Python OOP, SQL Basics")
    num_q = st.slider("Questions:", 5, 15, 5)

    col_q1, col_q2 = st.columns([1, 1])
    with col_q1:
        start_quiz = st.button("🎯 Start Quiz", use_container_width=True)
    with col_q2:
        if st.button("🔄 Reset Quiz", use_container_width=True):
            st.session_state.quiz_mode = False
            st.session_state.questions = []
            st.session_state.score = {"correct": 0, "total": 0}

    if start_quiz and quiz_topic:
        with st.spinner("✨ Generating quiz..."):
            questions, error = generate_quiz(quiz_topic, num_q, api_key)

        if error:
            st.error(error)
        else:
            st.session_state.questions = questions
            st.session_state.quiz_idx = 0
            st.session_state.quiz_mode = True
            st.session_state.score = {"correct": 0, "total": 0}
            st.session_state.answered = False
            st.rerun()

    if st.session_state.quiz_mode and st.session_state.questions:
        q_idx = st.session_state.quiz_idx
        if q_idx < len(st.session_state.questions):
            q = st.session_state.questions[q_idx]

            st.markdown(f"**Question {q_idx + 1}/{len(st.session_state.questions)}**")
            st.markdown(f"### {q['question']}")

            options = [q.get('correct', ''), q.get('B', ''), q.get('C', ''), q.get('D', '')]
            random.shuffle(options)

            selected = st.radio("Select your answer:", options, key=f"q_{q_idx}")

            col_submit, col_skip = st.columns([1, 1])
            with col_submit:
                submit = st.button("✅ Submit Answer", use_container_width=True)
            with col_skip:
                skip = st.button("⏭️ Skip", use_container_width=True)

            if submit or skip:
                st.session_state.answered = True
                st.session_state.score["total"] += 1

                correct = selected == q['correct']
                if correct:
                    st.session_state.score["correct"] += 1
                    st.success(f"✅ Correct! {q['correct']}")
                else:
                    st.error(f"❌ Wrong! Correct: {q['correct']}")

                if st.button("➡️ Next Question", use_container_width=True):
                    if st.session_state.quiz_idx < len(st.session_state.questions) - 1:
                        st.session_state.quiz_idx += 1
                        st.session_state.answered = False
                    else:
                        st.balloons()
                        st.success("🎉 Quiz Complete!")
                        st.session_state.quiz_mode = False
                    st.rerun()
        else:
            st.session_state.quiz_mode = False

        # Score
        st.divider()
        score = st.session_state.score
        pct = score["correct"] / max(score["total"], 1) * 100
        st.metric("Score", f"{score['correct']}/{score['total']}", delta=f"{pct:.0f}%")

with tab3:
    st.subheader("📖 AI Text Summarizer")

    text_input = st.text_area("Paste study material:", height=200,
                               placeholder="Paste any text, notes, or study material to summarize...")

    col_sum1, col_sum2 = st.columns([1, 1])
    with col_sum1:
        summarize = st.button("📝 Summarize", use_container_width=True)
    with col_sum2:
        st.session_state.summary = ""

    if summarize and text_input:
        with st.spinner("✨ Summarizing..."):
            result, error = summarize_text(text_input, api_key)

        if error:
            st.error(error)
        else:
            st.session_state.summary = result
            st.rerun()

    if st.session_state.summary:
        st.markdown("### 📋 Summary")
        st.markdown(st.session_state.summary)

        if st.button("📋 Copy Summary"):
            import pyperclip
            pyperclip.copy(st.session_state.summary)
            st.success("✅ Copied!")

with tab4:
    st.subheader("📅 Study Planner")

    st.markdown("**🎯 Weekly Study Plan Template:**")

    plan = {
        "Monday": {"subject": "Python", "topic": "OOP Concepts", "hours": 2, "type": "📖 Theory"},
        "Tuesday": {"subject": "Mathematics", "topic": "Linear Algebra", "hours": 1.5, "type": "📝 Practice"},
        "Wednesday": {"subject": "AI/ML", "topic": "Neural Networks", "hours": 2, "type": "🤖 Project"},
        "Thursday": {"subject": "SQL", "topic": "Joins & Subqueries", "hours": 1.5, "type": "📝 Practice"},
        "Friday": {"subject": "System Design", "topic": "Architecture", "hours": 1, "type": "📖 Theory"},
        "Saturday": {"subject": "Projects", "topic": "Build something", "hours": 3, "type": "🚀 Project"},
        "Sunday": {"subject": "Revision", "topic": "Review weekly topics", "hours": 2, "type": "🔄 Review"},
    }

    cols = st.columns(7)
    days = list(plan.keys())

    for i, day in enumerate(days):
        with cols[i]:
            d = plan[day]
            st.markdown(f"**{day}**")
            st.markdown(f"📚 {d['subject']}")
            st.markdown(f"📝 {d['topic']}")
            st.markdown(f"⏰ {d['hours']}h")
            st.markdown(d['type'])

    st.divider()
    st.markdown("**💡 Spaced Repetition Tips:**")
    tips = [
        "📌 Day 1: Learn new topic",
        "📌 Day 3: First review",
        "📌 Day 7: Second review",
        "📌 Day 14: Third review",
        "📌 Day 30: Final review",
    ]
    for tip in tips:
        st.markdown(tip)

st.divider()
st.caption("Built by Attanti Ramnivas | Powered by Google Gemini | Streamlit")
