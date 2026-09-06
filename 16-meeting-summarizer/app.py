"""
Meeting Summarizer - Auto-transcribe and summarize meetings
"""
import streamlit as st
import google.genai as genai
import os

st.set_page_config(page_title="Meeting Summarizer", page_icon="MEET", layout="wide")

if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "summary" not in st.session_state:
    st.session_state.summary = None
if "action_items" not in st.session_state:
    st.session_state.action_items = None

st.title("AI Meeting Summarizer")
st.markdown("*Paste your meeting transcript or notes and get AI-powered insights*")

with st.sidebar:
    st.title("Settings")
    summary_type = st.selectbox("Summary Style", [
        "Executive Summary", "Detailed Notes", "Bulleted Key Points", "Action-Oriented"
    ])
    include_action = st.checkbox("Action Items", value=True)
    include_decisions = st.checkbox("Decisions Made", value=True)
    include_questions = st.checkbox("Open Questions", value=True)
    if st.button("Clear All"):
        st.session_state.transcript = ""
        st.session_state.summary = None
        st.session_state.action_items = None
        st.rerun()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Input Meeting")
    transcript = st.text_area("Paste meeting transcript or notes:", height=400, placeholder="John: We need to improve the user onboarding flow.
Sarah: I agree. The drop-off rate is 40%.
John: Let us add a tutorial video and simplify the signup form.")
    st.session_state.transcript = transcript

with col2:
    st.subheader("AI Analysis")
    if st.button("Generate Summary", type="primary", use_container_width=True):
        if not st.session_state.transcript:
            st.warning("Please enter meeting content first")
        elif not os.environ.get("GOOGLE_API_KEY"):
            st.error("Please set GOOGLE_API_KEY")
        else:
            client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
            with st.spinner("Analyzing meeting..."):
                sections = []
                if include_action:
                    sections.append("- Action items with owners")
                if include_decisions:
                    sections.append("- Key decisions made")
                if include_questions:
                    sections.append("- Open questions")
                
                prompt = f"Analyze this meeting transcript and provide a {summary_type}:

{st.session_state.transcript}

Include:
" + "
".join(sections)
                response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
                st.session_state.summary = response.text

if st.session_state.summary:
    st.markdown("---")
    st.subheader("Meeting Summary")
    st.markdown(st.session_state.summary)

if st.session_state.action_items:
    with st.expander("Action Items", expanded=True):
        st.markdown(st.session_state.action_items)
