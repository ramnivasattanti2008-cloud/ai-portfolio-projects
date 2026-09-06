"""
AI Meeting Notes Summarizer
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Convert meeting notes → structured summary
- Extract action items with owners + deadlines
- Generate follow-up emails
- Create meeting minutes
- Track decisions made
- Topic tagging + search
- Multi-language support
"""

import os
import streamlit as st
from datetime import datetime
from collections import defaultdict

st.set_page_config(page_title="AI Meeting Notes", page_icon="📝", layout="wide")
st.title("📝 AI Meeting Notes Summarizer")
st.markdown("Paste meeting notes → Get structured summary, action items, decisions & follow-up emails")

# Session state
if "meetings" not in st.session_state:
    st.session_state.meetings = []
if "current_meeting" not in st.session_state:
    st.session_state.current_meeting = {}

# Functions
def analyze_meeting(notes, api_key):
    if not api_key:
        return None, "⚠️ Set GOOGLE_API_KEY in .env"

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""Analyze these meeting notes and provide a structured output.

MEETING NOTES:
{notes}

Provide in this EXACT format:

## SUMMARY
[2-3 sentence overview of the meeting]

## ATTENDEES
[All people mentioned in the meeting]

## KEY DISCUSSION POINTS
[3-5 main points discussed, numbered]

## DECISIONS MADE
[Any decisions or agreements reached, numbered]

## ACTION ITEMS
Format each as:
[ ] @[Owner] - [Task description] - [Deadline if mentioned]

## TOPICS TAGGED
[3-5 relevant topic tags, comma-separated]

## NEXT STEPS
[What should happen next, numbered]

## FOLLOW-UP EMAIL
[Write a professional follow-up email summarizing key points for attendees]

IMPORTANT: Return in valid markdown format. Be specific and extract real names, dates, and details from the notes."""

        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def parse_analysis(analysis_text):
    """Parse the structured analysis into sections"""
    sections = {}
    current_section = None
    current_content = []

    lines = analysis_text.split('\n')
    for line in lines:
        line = line.strip()
        # Check for section headers
        if line.startswith('## ') or line.startswith('**') or line.startswith('### '):
            # Save previous section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            # Start new section
            clean_line = line.replace('## ', '').replace('**', '').replace('# ', '')
            current_section = clean_line
            current_content = []
        elif current_section:
            current_content.append(line)

    # Save last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections

def extract_action_items(text):
    """Extract action items from text"""
    items = []
    for line in text.split('\n'):
        if '[ ]' in line or '@' in line or 'action' in line.lower():
            items.append(line.strip())
    return items

def generate_email(sections, api_key):
    """Generate a follow-up email"""
    if not api_key:
        return "⚠️ Set GOOGLE_API_KEY in .env"

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        summary = sections.get('SUMMARY', '')
        decisions = sections.get('DECISIONS MADE', '')
        actions = sections.get('ACTION ITEMS', '')

        prompt = f"""Write a professional meeting follow-up email based on this meeting summary:

SUMMARY:
{summary}

DECISIONS:
{decisions}

ACTION ITEMS:
{actions}

The email should:
1. Have a clear subject line
2. Briefly summarize key points discussed
3. Clearly list action items with owners
4. Mention next steps
5. Be professional but concise
6. Be suitable for corporate communication

Format as a complete email (Subject + Body)."""

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# UI
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📝 Paste Meeting Notes")

    meeting_title = st.text_input("Meeting Title:", placeholder="e.g., Sprint Planning - Q4 Review")
    date = st.date_input("Meeting Date:", value=datetime.now())

    notes = st.text_area(
        "Meeting Notes:",
        height=300,
        placeholder="""Paste your meeting notes here...

Example format:
Attendees: John, Sarah, Mike
Date: September 6, 2026

Agenda:
1. Sprint review
2. Roadblocks
3. Next sprint planning

Discussion:
- John presented the Q3 results showing 15% growth
- Sarah raised concern about the API integration delays
- Mike discussed the new feature requirements from client
- Team agreed to prioritize the dashboard feature

Decisions:
- Approved the new timeline: Oct 15 deadline
- Sarah will lead the API integration task

Action Items:
- John: Complete dashboard mockups by Sept 10
- Sarah: Fix API issues by Sept 12
- Mike: Submit feature doc by Sept 15"""
    )

    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        st.warning("⚠️ Set GOOGLE_API_KEY in .env for AI analysis")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        analyze = st.button("🔍 Analyze Meeting", use_container_width=True)
    with col_btn2:
        if st.button("💾 Save Meeting", use_container_width=True) and meeting_title:
            st.session_state.meetings.append({
                "title": meeting_title,
                "date": str(date),
                "notes": notes,
                "time": datetime.now().strftime("%H:%M")
            })
            st.success("✅ Meeting saved!")

with col_right:
    st.subheader("📊 Analysis Results")

    if analyze:
        if not notes.strip():
            st.warning("⚠️ Please paste meeting notes first")
        else:
            with st.spinner("🤖 Analyzing meeting notes..."):
                analysis, error = analyze_meeting(notes, api_key)

            if error:
                st.error(error)
            else:
                sections = parse_analysis(analysis)
                st.session_state.current_meeting = {
                    "sections": sections,
                    "raw": analysis
                }

    # Display current analysis
    if st.session_state.current_meeting:
        sections = st.session_state.current_meeting["sections"]

        # Summary card
        if "SUMMARY" in sections:
            with st.container():
                st.markdown("""
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px; border-radius: 10px; margin-bottom: 15px;">
                    <h3 style="color: white; margin: 0;">📋 Meeting Summary</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(sections["SUMMARY"])

        # Tabs for different sections
        tabs = st.tabs(["📌 Points", "✅ Decisions", "📋 Actions", "📧 Email", "📝 Minutes"])

        with tabs[0]:  # Key Points
            if "KEY DISCUSSION POINTS" in sections:
                st.markdown("### Key Discussion Points")
                st.markdown(sections["KEY DISCUSSION POINTS"])
            if "ATTENDEES" in sections:
                st.markdown("### 👥 Attendees")
                st.markdown(sections["ATTENDEES"])
            if "TOPICS TAGGED" in sections:
                st.markdown("### 🏷️ Topics")
                tags = [t.strip() for t in sections["TOPICS TAGGED"].split(',')]
                for tag in tags:
                    st.markdown(f"`{tag}`", unsafe_allow_html=True)

        with tabs[1]:  # Decisions
            if "DECISIONS MADE" in sections:
                st.markdown("### Decisions Made")
                st.markdown(sections["DECISIONS MADE"])
            else:
                st.info("No decisions recorded")
            if "NEXT STEPS" in sections:
                st.markdown("### Next Steps")
                st.markdown(sections["NEXT STEPS"])

        with tabs[2]:  # Action Items
            if "ACTION ITEMS" in sections:
                st.markdown("### Action Items")
                st.markdown(sections["ACTION ITEMS"])
            else:
                st.info("No action items found")

        with tabs[3]:  # Email
            if st.button("📧 Generate Follow-up Email", use_container_width=True):
                email = generate_email(sections, api_key)
                st.session_state.email = email
                st.rerun()

            if "email" in st.session_state:
                st.markdown("### Follow-up Email")
                st.markdown(st.session_state.email)
                if st.button("📋 Copy Email"):
                    import pyperclip
                    pyperclip.copy(st.session_state.email)
                    st.success("✅ Copied!")

        with tabs[4]:  # Minutes
            st.markdown("### 📝 Meeting Minutes")
            minutes = f"""# Meeting Minutes

**Title:** {meeting_title}
**Date:** {date}
**Prepared:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## Summary
{sections.get('SUMMARY', 'N/A')}

## Attendees
{sections.get('ATTENDEES', 'N/A')}

## Discussion Points
{sections.get('KEY DISCUSSION POINTS', 'N/A')}

## Decisions
{sections.get('DECISIONS MADE', 'N/A')}

## Action Items
{sections.get('ACTION ITEMS', 'N/A')}

## Next Steps
{sections.get('NEXT STEPS', 'N/A')}
"""
            st.markdown(minutes)
            if st.button("💾 Download Minutes"):
                st.download_button(
                    "📥 Download as Markdown",
                    minutes,
                    f"meeting_minutes_{date}.md",
                    use_container_width=True
                )

    else:
        st.info("👈 Paste meeting notes and click 'Analyze Meeting'")

# Saved meetings
st.divider()
st.subheader("📁 Saved Meetings")

if st.session_state.meetings:
    for i, m in enumerate(reversed(st.session_state.meetings[-5:])):
        with st.expander(f"📝 {m['title']} — {m['date']} {m['time']}"):
            st.markdown(m['notes'][:500] + "..." if len(m['notes']) > 500 else m['notes'])
            if st.button(f"🗑️ Delete", key=f"del_m_{i}"):
                st.session_state.meetings.remove(m)
                st.rerun()
else:
    st.info("No meetings saved yet")

# Quick templates
st.divider()
st.subheader("📋 Meeting Note Templates")

templates = {
    "Sprint Planning": "Attendees: \nDate: \n\nAgenda:\n1. \n2. \n\nDiscussion:\n- \n\nDecisions:\n- \n\nAction Items:\n- @[Owner] - [Task] - [Deadline]",
    "Client Call": "Client: \nAttendees: \nDate: \n\nPurpose: \n\nKey Points:\n- \n\nClient Requirements:\n- \n\nDecisions:\n- \n\nNext Steps:\n- ",
    "1:1 Meeting": "Employee: \nManager: \nDate: \n\nUpdates:\n- \n\nChallenges:\n- \n\nSupport Needed:\n- \n\nGoals for Next Week:\n- "
}

col_t1, col_t2, col_t3 = st.columns(3)
for i, (name, template) in enumerate(templates.items()):
    with [col_t1, col_t2, col_t3][i]:
        if st.button(f"📄 {name}", use_container_width=True):
            st.info(f"Template loaded! Paste in the notes area.")
            st.code(template, language="text")

st.divider()
st.caption("Built by Attanti Ramnivas | Powered by Google Gemini | Streamlit")
