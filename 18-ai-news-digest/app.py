"""
AI News Digest - Personalized daily AI news with summaries
"""
import streamlit as st
import google.genai as genai
import os

st.set_page_config(page_title="AI News Digest", page_icon="NEWS", layout="wide")

if "news_articles" not in st.session_state:
    st.session_state.news_articles = []
if "summaries" not in st.session_state:
    st.session_state.summaries = {}

st.title("AI News Digest")
st.markdown("*Your personalized AI-curated daily news briefing*")

with st.sidebar:
    st.title("Preferences")
    categories = st.multiselect("Select topics", [
        "Technology", "AI", "Science", "Business", "Health", "Sports", "Entertainment"
    ], default=["Technology", "AI"])
    region = st.selectbox("News region", ["India", "US", "UK", "Global"])
    show_images = st.checkbox("Show article images", value=True)
    if st.button("Refresh News"):
        st.session_state.news_articles = []
        st.session_state.summaries = {}
        st.rerun()
    st.metric("Articles", len(st.session_state.news_articles))
    st.metric("Summarized", len(st.session_state.summaries))

SAMPLE_NEWS = [
    {"title": "Google Announces Gemini 2.0 with Enhanced Capabilities",
     "description": "Google unveils Gemini 2.0 featuring improved multimodal reasoning, real-time processing, and better integration across Google services.",
     "source": "TechCrunch", "category": "AI"},
    {"title": "India AI Startup Funding Reaches 5 Billion in 2024",
     "description": "Indian AI startups have raised over 5 billion in funding, marking a 150% increase from the previous year.",
     "source": "YourStory", "category": "Business"},
    {"title": "Researchers Develop New AI Model Compression Method",
     "description": "A team of researchers has developed a novel technique for compressing large language models while maintaining accuracy.",
     "source": "MIT Tech Review", "category": "Science"},
    {"title": "OpenAI Releases New Safety Guidelines for AI Development",
     "description": "OpenAI has published comprehensive safety guidelines emphasizing responsible AI development and deployment practices.",
     "source": "The Verge", "category": "AI"},
    {"title": "Tech Giants Form Coalition for AI Ethics Standards",
     "description": "Major technology companies have joined forces to establish industry-wide standards for ethical AI development.",
     "source": "Wired", "category": "Technology"},
    {"title": "Breakthrough in Quantum Computing Could Revolutionize AI",
     "description": "Scientists have achieved a significant breakthrough in quantum computing that could dramatically accelerate AI model training.",
     "source": "Nature", "category": "Science"},
]

if not st.session_state.news_articles:
    st.session_state.news_articles = SAMPLE_NEWS
    st.info("Using sample news. Set NEWS_API_KEY for live news!")

st.subheader(f"Latest News ({len(st.session_state.news_articles)} articles)")

for i, article in enumerate(st.session_state.news_articles):
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"**{i+1}**")
        with col2:
            st.markdown(f"**{article['title']}**")
            st.caption(f"{article['source']}")
            st.markdown(article['description'][:200] + "...")
            
            if st.button(f"Summarize", key=f"sum_{i}"):
                if os.environ.get("GOOGLE_API_KEY"):
                    client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
                    prompt = f"Summarize this news article in 3 bullet points:

Title: {article['title']}
{article['description']}"
                    response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
                    st.session_state.summaries[article['title']] = response.text
                    st.rerun()
            
            if article['title'] in st.session_state.summaries:
                with st.expander("AI Summary"):
                    st.markdown(st.session_state.summaries[article['title']])
        st.markdown("---")

if st.button("Generate AI Briefing", type="primary"):
    if os.environ.get("GOOGLE_API_KEY"):
        client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        with st.spinner("Creating your briefing..."):
            news_text = "
".join([f"- {a['title']}: {a['description']}" for a in st.session_state.news_articles])
            prompt = f"Create a personalized daily news briefing based on these articles. Focus on: {', '.join(categories)}

Articles:
{news_text}

Format as:
1. Top Stories - 2-3 most important with context
2. What It Means - Why these matter
3. Quick Takes - One-line summaries"
            response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
            st.markdown("---")
            st.markdown(response.text)
    else:
        st.error("Please set GOOGLE_API_KEY")
