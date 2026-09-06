"""
AI LinkedIn Post Scheduler — Content Planner & Scheduler
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Generate LinkedIn post ideas with AI
- Content calendar with scheduling
- Hashtag generator
- Best time to post suggestions
- Post templates for different goals
"""

import os
import json
from datetime import datetime, timedelta
import streamlit as st

st.set_page_config(page_title="LinkedIn Post Planner", page_icon="📅", layout="wide")
st.title("📅 AI LinkedIn Post Scheduler & Content Planner")
st.markdown("Generate, plan, and schedule your LinkedIn content with AI-powered suggestions")

# Topics
TOPICS = [
    "AI/ML Development", "Python Projects", "Career Growth",
    "Tech Learning", "Open Source", "Startup Life",
    "Interview Tips", "Side Projects", "Remote Work"
]

TONES = ["Professional", "Inspirational", "Educational", "Storytelling", "Conversational", "Bold"]

GOALS = ["Build Personal Brand", "Get Hired", "Network", "Share Knowledge", "Attract Clients"]

def generate_post(topic, goal, tone, api_key):
    if not api_key:
        return None, "⚠️ Set GOOGLE_API_KEY in .env"

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""Write a LinkedIn post for an Indian tech student/developer.

TOPIC: {topic}
GOAL: {goal}
TONE: {tone}

Requirements:
- 150-300 words (LinkedIn optimal length)
- Hook in first line (people stop scrolling here)
- 3-5 relevant hashtags at the end
- Call to action (ask a question, invite engagement)
- Personal, authentic voice
- Include emojis appropriately
- Indian context is fine (college, campus placements, tech scene)

Format:
[POST CONTENT]

#tag1 #tag2 #tag3 #tag4 #tag5

---
Also suggest:
- Best time to post: [time]
- Target audience: [description]
- Engagement hook: [what makes people comment]"""

        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def generate_hashtags(topic, api_key):
    if not api_key:
        return []

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")
        prompt = f"Give me 15 relevant LinkedIn hashtags for: {topic}. Return ONLY the hashtags separated by spaces, no explanations."
        response = model.generate_content(prompt)
        return response.text.strip().split()
    except:
        return [f"#{topic.replace(' ', '')}" for topic in TOPICS[:5]]

# Session state
if "posts" not in st.session_state:
    st.session_state.posts = []
if "generated" not in st.session_state:
    st.session_state.generated = None

# Sidebar
with st.sidebar:
    st.header("📅 Content Calendar")
    st.markdown("**Best Times to Post (IST):**")
    times = [
        ("Monday", "9:00 AM, 12:00 PM, 6:00 PM"),
        ("Tuesday", "10:00 AM, 1:00 PM, 7:00 PM"),
        ("Wednesday", "9:00 AM, 12:00 PM, 5:00 PM"),
        ("Thursday", "10:00 AM, 1:00 PM, 6:00 PM"),
        ("Friday", "9:00 AM, 11:00 AM, 4:00 PM"),
    ]
    for day, time in times:
        st.markdown(f"**{day}:** {time}")

    st.markdown("---")
    st.markdown("**This Week's Plan:**")
    week_plan = [
        "📝 Monday: Educational post",
        "💡 Wednesday: Project showcase",
        "🎯 Friday: Engagement/Career post",
    ]
    for plan in week_plan:
        st.markdown(plan)

# Main
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("✨ Generate New Post")

    topic = st.selectbox("🎯 Topic", TOPICS)
    goal = st.selectbox("🎯 Goal", GOALS)
    tone = st.selectbox("🎨 Tone", TONES)

    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        st.warning("⚠️ Set GOOGLE_API_KEY in .env for AI generation")

    col_gen1, col_gen2 = st.columns(2)
    with col_gen1:
        generate = st.button("🚀 Generate Post", use_container_width=True)
    with col_gen2:
        if st.button("🎲 Random Topic", use_container_width=True):
            import random
            topic = random.choice(TOPICS)
            st.info(f"Selected: {topic}")

    # Templates
    st.divider()
    st.subheader("📋 Post Templates")

    templates = {
        "🚀 Launch Post": "I just built [project name]. Here's what I learned:\n\n1. [Lesson 1]\n2. [Lesson 2]\n3. [Lesson 3]\n\nWhat would you have done differently? 👇",
        "💡 Learning Post": "The biggest lesson I learned about [topic]:\n\nMost people think [common misconception].\n\nThe truth is [actual insight].\n\nWhat's your experience with this? ⬇️",
        "📊 Stats Post": "I analyzed [something] and found:\n\n📈 [Stat 1]\n📉 [Stat 2]\n🎯 [Stat 3]\n\nKey takeaway: [insight]\n\nHave you noticed this too? Let's discuss 👇",
        "❌ Mistake Post": "I made [mistake] and it cost me [consequence].\n\nHere's what I should have done instead:\n\n[Correct approach]\n\nDon't make the same mistake. Save this post for later 📌",
        "✅ Wins Post": "This week I:\n\n✅ [Achievement 1]\n✅ [Achievement 2]\n✅ [Achievement 3]\n\n[Reflection or next goal]\n\nWhat did you accomplish this week? 👇",
    }

    selected_template = st.selectbox("Load template:", ["None"] + list(templates.keys()))
    if selected_template != "None":
        st.code(templates[selected_template], language="text")

with col_right:
    st.subheader("📤 Generated Post")

    if generate:
        with st.spinner("✨ Generating your post..."):
            result, error = generate_post(topic, goal, tone, api_key)

        if error:
            st.error(error)
        else:
            st.session_state.generated = result
            st.session_state.posts.append({
                "content": result,
                "topic": topic,
                "goal": goal,
                "time": datetime.now()
            })
            st.rerun()

    if st.session_state.generated:
        st.markdown(st.session_state.generated)

        col_copy, col_save, col_clear = st.columns(3)
        if st.button("📋 Copy", use_container_width=True):
            import pyperclip
            pyperclip.copy(st.session_state.generated)
            st.success("✅ Copied!")

        if st.button("💾 Save", use_container_width=True):
            filename = f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(st.session_state.generated)
            st.success(f"✅ Saved as {filename}")

        if st.button("🔄 Generate Another", use_container_width=True):
            st.session_state.generated = None
            st.rerun()
    else:
        st.info("👈 Generate a post to see it here")

        # Show saved posts
        if st.session_state.posts:
            st.divider()
            st.subheader("📚 Saved Posts")
            for i, post in enumerate(reversed(st.session_state.posts[-5:])):
                with st.expander(f"📝 {post['topic']} — {post['time'].strftime('%b %d, %H:%M')}"):
                    st.markdown(post['content'])

# Hashtag Generator
st.divider()
st.subheader("🏷️ Hashtag Generator")

col_h1, col_h2 = st.columns([1, 1])

with col_h1:
    hashtag_topic = st.text_input("Topic for hashtags:", placeholder="e.g., Python, AI, Web Development")
    gen_hashtags = st.button("🎯 Generate Hashtags", use_container_width=True)

with col_h2:
    if gen_hashtags and hashtag_topic:
        hashtags = generate_hashtags(hashtag_topic, api_key)
        st.markdown("**Your Hashtags:**")
        hashtag_html = " ".join(f"`{h}`" for h in hashtags)
        st.markdown(hashtag_html)

        if st.button("📋 Copy Hashtags"):
            import pyperclip
            pyperclip.copy(" ".join(hashtags))
            st.success("✅ Copied!")

# Best practices
st.divider()
st.subheader("📈 LinkedIn Best Practices")

col_bp1, col_bp2, col_bp3 = st.columns(3)

tips = {
    "📝 Content": [
        "Hook in first line (stop the scroll!)",
        "Keep it 150-300 words",
        "Use line breaks (walls of text = no engagement)",
        "Ask a question to drive comments",
        "End with a call to action"
    ],
    "🏷️ Hashtags": [
        "Use 3-5 relevant hashtags",
        "Mix popular + niche hashtags",
        "Include your industry + skills",
        "No #AI #MachineLearning (too generic)",
        "Check what top creators use"
    ],
    "⏰ Timing": [
        "Best: Tue-Thu, 9AM or 12PM IST",
        "Avoid weekends (low engagement)",
        "Post 3x per week maximum",
        "Engage in first 30 minutes",
        "Reply to all comments same day"
    ]
}

for i, (cat, items) in enumerate(tips.items()):
    with [col_bp1, col_bp2, col_bp3][i]:
        st.markdown(f"**{cat}**")
        for item in items:
            st.markdown(f"- {item}")

st.divider()
st.caption("Built by Attanti Ramnivas | Powered by Google Gemini | Streamlit")
