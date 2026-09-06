"""
AI Thumbnail Generator — YouTube Thumbnail Ideas
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Generate thumbnail concepts with AI
- Color palette suggestions
- Text overlay ideas
- Layout suggestions
- Canva integration tips
"""

import os
import streamlit as st

st.set_page_config(page_title="Thumbnail Generator", page_icon="🖼️", layout="wide")
st.title("🖼️ AI YouTube Thumbnail Generator")
st.markdown("Get thumbnail concepts, color palettes, and text ideas for your YouTube videos")

LAYOUTS = {
    "Close-up Face": "Big expressive face, small video frame at corner",
    "Text + Background": "Large bold text, blurred background image",
    "Split Screen": "Before/after comparison side by side",
    "Stacked": "Person on top, text on bottom, background",
    "Minimal": "Simple text + gradient background",
    "Dramatic": "Person with dramatic lighting, small text overlay"
}

COLORS = {
    "Tech/AI": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"],
    "Gaming": ["#00D4FF", "#FF00FF", "#00FF00", "#FFD700", "#FF4500"],
    "Education": ["#3498DB", "#2ECC71", "#F39C12", "#9B59B6", "#1ABC9C"],
    "Lifestyle": ["#E91E63", "#FF9800", "#8BC34A", "#00BCD4", "#673AB7"],
    "Finance": ["#1A237E", "#00C853", "#FFD700", "#C62828", "#1565C0"],
}

def generate_thumbnail_idea(title, topic, api_key):
    if not api_key:
        return None, "⚠️ Set GOOGLE_API_KEY in .env"

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""Give thumbnail ideas for this YouTube video:

Title: {title}
Topic: {topic}

Provide:
1. Thumbnail concept (2-3 sentences)
2. Suggested layout
3. Best color palette (3 options)
4. Text to include (max 3 words)
5. Expression/pose for person in thumbnail
6. Background suggestion

Be specific and actionable."""

        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, str(e)

# UI
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("🎬 Video Details")
    title = st.text_input("📌 Video Title:", placeholder="e.g., I Built an AI Chatbot in 24 Hours")
    topic = st.selectbox("📂 Topic:", ["AI/ML", "Tech", "Gaming", "Education", "Lifestyle", "Finance", "Other"])
    custom_topic = st.text_input("Or specify:", placeholder="e.g., Python tutorials for beginners")

    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        st.warning("⚠️ Set GOOGLE_API_KEY for AI generation")

    layout = st.selectbox("🎨 Preferred Layout:", list(LAYOUTS.keys()))

    col_gen1, col_gen2 = st.columns(2)
    with col_gen1:
        generate = st.button("✨ Generate Ideas", use_container_width=True)
    with col_gen2:
        st.info(f"Layout: {LAYOUTS[layout]}")

with col_right:
    st.subheader("🖼️ Thumbnail Ideas")

    if generate and title:
        if api_key:
            with st.spinner("✨ Generating..."):
                result, err = generate_thumbnail_idea(title, custom_topic or topic, api_key)
            if result:
                st.markdown(result)
            else:
                st.error(err)
        else:
            # Fallback ideas
            st.markdown(f"### 🎬 Concept for: {title}")
            st.markdown(f"**Layout:** {layout} — {LAYOUTS[layout]}")
            st.markdown(f"**Color Palette:** {', '.join(COLORS.get(topic, COLORS['Tech/AI']))}")
            st.markdown(f"**Text:** {title[:30]}...")
            st.info("Set GOOGLE_API_KEY for full AI suggestions")

    # Pre-made templates
    st.divider()
    st.markdown("### 📋 Quick Templates")

    templates = {
        "Challenge": ("Big text '24 HOURS'", "#FF6B6B"),
        "Tutorial": ("Step-by-step numbers", "#3498DB"),
        "Review": ("VS comparison", "#9B59B6"),
        "Top 5/10": ("Bold number", "#2ECC71"),
        "I Tried": ("Person doing something", "#E91E63"),
    }

    for name, (text, color) in templates.items():
        with st.expander(f"📸 {name}"):
            st.markdown(f"**Text:** {text}")
            st.markdown(f"**Color:** {color}")
            st.markdown(f"**Tip:** Use bold, contrasting font")

# Color Palettes
st.divider()
st.subheader("🎨 Color Palettes by Topic")

cols = st.columns(len(COLORS))
for i, (cat, palette) in enumerate(COLORS.items()):
    with cols[i]:
        st.markdown(f"**{cat}**")
        for color in palette:
            st.markdown(f"<div style='background-color:{color}; padding:10px; border-radius:5px;'>{color}</div>", unsafe_allow_html=True)

# Canva Tips
st.divider()
st.subheader("🛠️ Canva Thumbnail Tips")

col_c1, col_c2 = st.columns(2)

tips_left = [
    "Canvas size: 1280 x 720 px",
    "Use bold fonts (Poppins, Montserrat)",
    "High contrast text + background",
    "Max 3-4 colors",
    "Face photos perform 30% better"
]

tips_right = [
    "Leave space at bottom (mobile cut)",
    "Use frames/borders for focus",
    "Add subtle shadow for depth",
    "Test on dark + light thumbnails",
    "A/B test different versions"
]

with col_c1:
    for tip in tips_left:
        st.markdown(f"- {tip}")

with col_c2:
    for tip in tips_right:
        st.markdown(f"- {tip}")

st.divider()
st.caption("Built by Attanti Ramnivas | Powered by Google Gemini | Streamlit")
