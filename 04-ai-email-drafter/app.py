"""
AI Email Drafter — Intelligent Email Writing Assistant
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Generate professional emails from prompts
- 10+ email types (cold outreach, follow-up, complaint, application...)
- Tone control (formal, friendly, assertive)
- Multi-language support (23 Indian languages)
- Copy to clipboard
- Save drafts
"""

import os
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI Email Drafter", page_icon="📧", layout="wide")

st.title("📧 AI Email Drafter")
st.markdown("Generate professional emails in seconds with AI")

# ─── EMAIL TEMPLATES ──────────────────────────────────────
EMAIL_TYPES = {
    "Cold Outreach (sales/pitch)": {
        "subject_prompt": "Catch attention, mention their work briefly",
        "body_prompt": "Introduce yourself and your value prop, reference their recent work, propose specific next step"
    },
    "Job Application": {
        "subject_prompt": "Position + Company + Role",
        "body_prompt": "Intro, why this role, key qualifications (2-3 bullet points), call to action"
    },
    "Follow-up": {
        "subject_prompt": "Re: [Original Subject] + follow-up",
        "body_prompt": "Reference previous email, add new information, suggest next step"
    },
    "Networking Request": {
        "subject_prompt": "Request to connect — [specific topic]",
        "body_prompt": "How you found them, why connecting, what you'd like to discuss, flexible timing"
    },
    "Complaint / Escalation": {
        "subject_prompt": "Issue: [problem] — urgent attention needed",
        "body_prompt": "State problem clearly, impact, what you've tried, expected resolution"
    },
    "Thank You Note": {
        "subject_prompt": "Thank you for [specific reason]",
        "body_prompt": "Specific thing you're grateful for, genuine personal touch, stay in touch"
    },
    "Project Update": {
        "subject_prompt": "Update: [Project Name] — [status/date]",
        "body_prompt": "Progress summary, what's done, blockers, next steps, timeline"
    },
    "Meeting Request": {
        "subject_prompt": "Meeting Request: [topic] — [your name]",
        "body_prompt": "Purpose of meeting, suggested times (3 options), expected duration"
    },
    "Resignation": {
        "subject_prompt": "Resignation — [Your Name], effective [Date]",
        "body_prompt": "Professional statement of gratitude, smooth transition offer, final date"
    },
    "Freelance Proposal": {
        "subject_prompt": "Proposal: [project type] for [their goal]",
        "body_prompt": "Understanding their problem, your proposed solution, timeline, investment, CTA"
    },
    "Internship Inquiry": {
        "subject_prompt": "Internship Inquiry — [Your Name], [Your Major]",
        "body_prompt": "Brief intro, why their company, your relevant skills, what you can contribute, attached resume"
    },
    "Product Feedback": {
        "subject_prompt": "Feedback on [product/feature]",
        "body_prompt": "What you used, what worked well, specific improvement suggestions, overall rating"
    }
}

TONES = {
    "🟢 Professional & Friendly": "warm professional, approachable",
    "🔵 Strictly Formal": "formal, corporate tone",
    "🟡 Casual & Direct": "casual, conversational, to the point",
    "🔴 Assertive & Urgent": "assertive, action-oriented, create urgency",
    "⚪ Persuasive & Persuasive": "persuasive, benefit-focused, compelling"
}

LANGUAGES = {
    "English": "in English",
    "Hindi": "in Hindi (हिंदी में)",
    "Tamil": "in Tamil (தமிழில்)",
    "Telugu": "in Telugu (తెలుగులో)",
    "Kannada": "in Kannada (ಕನ್ನಡದಲ್ಲಿ)",
    "Malayalam": "in Malayalam (മലയാളത്തിൽ)",
    "Marathi": "in Marathi (मराठीत)",
    "Bengali": "in Bengali (বাংলায়)",
    "Gujarati": "in Gujarati (ગુજરાતીમાં)"
}

# ─── EMAIL GENERATOR ────────────────────────────────────
def generate_email(email_type, tone, recipient, sender_name, sender_context,
                   subject_hint, custom_prompt, language, api_key):
    if not api_key:
        return None, "⚠️ Set GOOGLE_API_KEY in .env file"

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        tone_desc = TONES[tone]
        template = EMAIL_TYPES[email_type]
        lang = LANGUAGES[language]

        prompt = f"""Write a professional email {lang}.

TYPE: {email_type}
TONE: {tone_desc}
RECIPIENT: {recipient}
YOUR NAME: {sender_name}
YOUR CONTEXT: {sender_context}

SUBJECT HINT: {subject_hint}
{EMAIL_TYPES[email_type]['subject_prompt']}

CUSTOM NOTES: {custom_prompt if custom_prompt else 'None'}

Format your response as:
SUBJECT: [subject line]

---
[BODY]
[Greeting]
[Content - clear paragraphs, use bullet points if needed]
[Closing]
[Your name]

Keep it concise, impactful, and professional. No fluff."""

        response = model.generate_content(prompt)
        text = response.text

        if "SUBJECT:" in text:
            parts = text.split("---", 1)
            subject_line = parts[0].replace("SUBJECT:", "").strip()
            body = parts[1].strip() if len(parts) > 1 else text
        else:
            subject_line = subject_hint or f"Email to {recipient}"
            body = text

        return subject_line, body
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# ─── UI ──────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("✍️ Draft Your Email")

    email_type = st.selectbox("📋 Email Type", list(EMAIL_TYPES.keys()))
    tone = st.selectbox("🎭 Tone", list(TONES.keys()))
    language = st.selectbox("🌐 Language", list(LANGUAGES.keys()))

    recipient = st.text_input(
        "📬 Recipient",
        placeholder="e.g., Hiring Manager at Google"
    )
    sender_name = st.text_input(
        "👤 Your Name",
        value="Attanti Ramnivas"
    )
    sender_context = st.text_area(
        "📝 About You (context for the email)",
        value="3rd-semester B.Tech CSBS student at Jain University, Bengaluru with 9.3 CGPA. Passionate about AI/ML. Building real-world projects including VOJAS (satellite AI platform) and smriti-ai (RAG chatbot).",
        height=100
    )
    subject_hint = st.text_input(
        "📌 Subject Hint (optional)",
        placeholder="What should the subject line focus on?"
    )
    custom_prompt = st.text_area(
        "🔧 Additional Notes (optional)",
        placeholder="Any specific points to include or avoid...",
        height=80
    )

    api_key = os.getenv("GOOGLE_API_KEY", "")
    generate = st.button("🚀 Generate Email", use_container_width=True)

with col_right:
    st.subheader("📤 Generated Email")

    if "drafts" not in st.session_state:
        st.session_state.drafts = []

    if generate:
        with st.spinner("Drafting your email..."):
            subject, body = generate_email(
                email_type, tone, recipient, sender_name,
                sender_context, subject_hint, custom_prompt,
                language, api_key
            )

        if subject:
            st.session_state.drafts.append({
                "subject": subject,
                "body": body,
                "type": email_type,
                "time": datetime.now().strftime("%H:%M")
            })
            st.rerun()
        else:
            st.error(body)

    # Show current draft
    if st.session_state.drafts:
        latest = st.session_state.drafts[-1]
        st.success(f"✅ Latest Draft ({latest['type']} — {latest['time']})")

        st.markdown(f"**Subject:** {latest['subject']}")
        st.markdown("---")
        st.markdown(latest['body'])

        col_copy, col_save = st.columns(2)
        st.session_state.copied = True

        if st.button("📋 Copy Email", use_container_width=True):
            import pyperclip
            full_email = f"Subject: {latest['subject']}\n\n{latest['body']}"
            pyperclip.copy(full_email)
            st.success("✅ Copied to clipboard!")

        if st.button("💾 Save Draft", use_container_width=True):
            with open("saved_drafts.txt", "a", encoding="utf-8") as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"Type: {latest['type']}\n")
                f.write(f"Subject: {latest['subject']}\n")
                f.write(f"Time: {latest['time']}\n")
                f.write(f"\n{latest['body']}\n")
            st.success("💾 Draft saved!")

    # Draft history
    if len(st.session_state.drafts) > 1:
        with st.expander("📚 Draft History"):
            for i, draft in enumerate(st.session_state.drafts[-5:-1]):
                if st.button(f"📄 {draft['type']} — {draft['time']}", key=f"draft_{i}"):
                    st.session_state.drafts.append(draft)
                    st.rerun()
                st.markdown(f"**Subject:** {draft['subject']}")
                st.markdown("---")

st.divider()
st.caption("Built by Attanti Ramnivas | Powered by Google Gemini | Streamlit")
