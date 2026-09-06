"""
AI Interview Coach - Mock interview practice with AI feedback
"""
import streamlit as st
import google.genai as genai
import os
from datetime import datetime

st.set_page_config(page_title="AI Interview Coach", page_icon="🎯", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0
if "feedback_mode" not in st.session_state:
    st.session_state.feedback_mode = False

with st.sidebar:
    st.title("Interview Coach")
    interview_type = st.selectbox("Select role", [
        "Software Engineer", "Data Scientist", "ML Engineer", "Full Stack Developer", "Frontend Developer", "Backend Developer"
    ])
    difficulty = st.select_slider("Level", ["Beginner", "Intermediate", "Advanced"], value="Intermediate")
    st.metric("Questions Asked", st.session_state.questions_asked)
    if st.button("Start New Interview"):
        st.session_state.messages = []
        st.session_state.questions_asked = 0
        st.rerun()

st.title("AI Interview Coach")
st.markdown("*Practice makes perfect! Get real-time feedback on your answers.*")

api_key = os.environ.get("GOOGLE_API_KEY", "")
client = genai.Client(api_key=api_key) if api_key else None

if st.session_state.questions_asked == 0 and not st.session_state.messages:
    if st.button("Start Interview", type="primary"):
        if client:
            prompt = f"You are an expert interviewer for a {interview_type} position at {difficulty} level. Ask your first behavioral or technical question."
            response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.session_state.questions_asked = 1
            st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if st.session_state.questions_asked > 0 and st.session_state.questions_asked <= 5:
    if prompt := st.chat_input("Type your answer..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.rerun()

if st.button("Get Feedback") and len(st.session_state.messages) > 1:
    if client:
        user_answers = [m["content"] for m in st.session_state.messages if m["role"] == "user"]
        if user_answers:
            feedback_prompt = f"As an expert interviewer for {interview_type} at {difficulty} level, provide feedback on: {user_answers[-1]}"
            response = client.models.generate_content(model="gemini-2.0-flash", contents=[feedback_prompt])
            st.session_state.messages.append({"role": "assistant", "content": f"Feedback: {response.text}"})
            st.rerun()

if st.session_state.questions_asked > 0 and st.session_state.questions_asked <= 5:
    if st.button("Next Question"):
        if client:
            response = client.models.generate_content(model="gemini-2.0-flash", contents=["Ask the next interview question."])
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.session_state.questions_asked += 1
            st.rerun()

if st.session_state.questions_asked > 5:
    st.success("Interview Complete!")
