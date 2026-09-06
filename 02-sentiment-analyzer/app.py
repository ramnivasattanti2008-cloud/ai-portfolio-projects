"""
Sentiment Analyzer — AI-Powered Text/Review Analysis
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Analyze text for positive/negative/neutral sentiment
- Batch analysis from CSV
- Visual charts (Word cloud, sentiment distribution)
- Aspect-based sentiment (product, service, price, delivery)
- Real-time streaming analysis
"""

import os
import re
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from collections import Counter
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

# ─── CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="Sentiment Analyzer",
    page_icon="💬",
    layout="wide"
)

st.title("💬 AI Sentiment Analyzer")
st.markdown("Analyze text, reviews, and feedback with AI-powered sentiment detection")

# ─── SENTIMENT ENGINE ───────────────────────────────────
def analyze_sentiment(text):
    """Analyze text using TextBlob + custom rules"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 to 1
    subjectivity = blob.sentiment.subjectivity  # 0 to 1

    if polarity > 0.1:
        label = "✅ Positive"
        emoji = "😊"
        score = round((polarity + 1) / 2 * 100)
    elif polarity < -0.1:
        label = "❌ Negative"
        emoji = "😠"
        score = round((polarity + 1) / 2 * 100)
    else:
        label = "⚪ Neutral"
        emoji = "😐"
        score = 50

    return {
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "label": label,
        "emoji": emoji,
        "score": score,
        "words": blob.words,
        "noun_phrases": list(blob.noun_phrases)
    }

def extract_aspects(text):
    """Extract aspect-based sentiments"""
    aspects = {
        "product": [],
        "service": [],
        "price": [],
        "delivery": []
    }
    text_lower = text.lower()

    aspect_keywords = {
        "product": ["product", "quality", "build", "design", "looks", "material"],
        "service": ["service", "support", "help", "response", "staff", "customer"],
        "price": ["price", "cost", "value", "money", "cheap", "expensive", "worth"],
        "delivery": ["delivery", "shipping", "packaging", "arrived", "delay", "fast"]
    }

    for aspect, keywords in aspect_keywords.items():
        for kw in keywords:
            if kw in text_lower:
                idx = text_lower.index(kw)
                start = max(0, idx - 50)
                end = min(len(text), idx + 50)
                snippet = text[start:end]
                result = analyze_sentiment(snippet)
                aspects[aspect].append({
                    "keyword": kw,
                    "snippet": f"...{snippet}...",
                    "sentiment": result["label"]
                })
    return aspects

def get_word_freq(text):
    """Get most common meaningful words"""
    from nltk.corpus import stopwords
    stop = set(stopwords.words('english'))
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    filtered = [w for w in words if w not in stop]
    return Counter(filtered).most_common(20)

# ─── SINGLE TEXT ANALYSIS ────────────────────────────────
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔍 Analyze Text")
    text_input = st.text_area(
        "Enter text or review to analyze:",
        height=200,
        placeholder="Example: The product quality is amazing but delivery was late..."
    )
    analyze_btn = st.button("🚀 Analyze Sentiment", use_container_width=True)

if analyze_btn and text_input:
    result = analyze_sentiment(text_input)
    aspects = extract_aspects(text_input)
    words = get_word_freq(text_input)

    with col2:
        st.subheader("📊 Results")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Polarity", result["polarity"],
                     delta="Positive" if result["polarity"] > 0 else "Negative" if result["polarity"] < 0 else "Neutral")
        with col_b:
            st.metric("Sentiment Score", f"{result['score']}%",
                     delta=result["label"])

        st.markdown(f"### {result['emoji']} {result['label']}")
        st.progress(result["score"] / 100)
        st.caption(f"Subjectivity: {result['subjectivity']} (0=objective, 1=subjective)")

    # Aspect breakdown
    st.subheader("🎯 Aspect-Based Analysis")
    aspect_cols = st.columns(4)
    aspect_icons = {"product": "📦", "service": "🛠️", "price": "💰", "delivery": "🚚"}
    for i, (aspect, mentions) in enumerate(aspects.items()):
        with aspect_cols[i]:
            if mentions:
                pos = sum(1 for m in mentions if "Positive" in m["sentiment"])
                neg = sum(1 for m in mentions if "Negative" in m["sentiment"])
                st.markdown(f"**{aspect_icons[aspect]} {aspect.title()}**")
                st.markdown(f"✅ {pos} positive | ❌ {neg} negative")
                with st.expander("Mentions"):
                    for m in mentions:
                        st.markdown(f"- *{m['snippet']}* → {m['sentiment']}")
            else:
                st.markdown(f"**{aspect_icons[aspect]} {aspect.title()}**")
                st.markdown("😐 No mentions found")

    # Word frequency
    if words:
        st.subheader("📝 Most Common Words")
        df_words = pd.DataFrame(words, columns=["Word", "Count"])
        fig = px.bar(df_words.head(10), x="Word", y="Count",
                     color="Count", title="Top 10 Words")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ─── BATCH CSV ANALYSIS ─────────────────────────────────
st.divider()
st.subheader("📂 Batch Analysis from CSV")

batch_file = st.file_uploader(
    "Upload CSV file with a 'text' or 'review' column:",
    type=["csv"]
)

if batch_file:
    df = pd.read_csv(batch_file)
    st.write("📋 Preview:", df.head())

    text_col = None
    for col in ["text", "review", "comment", "feedback", "message"]:
        if col in df.columns:
            text_col = col
            break

    if not text_col:
        st.error("❌ No recognized text column found (text/review/comment/feedback)")
    else:
        if st.button("⚡ Run Batch Analysis", use_container_width=True):
            results = []
            progress = st.progress(0)

            for i, row in df.iterrows():
                text = str(row[text_col])
                result = analyze_sentiment(text)
                result["text"] = text[:100]
                results.append(result)
                progress.progress((i + 1) / len(df))

            df_result = pd.DataFrame(results)
            df_result["Polarity Score"] = df_result["polarity"]
            df_result["Sentiment"] = df_result["label"]

            # Summary stats
            col_s1, col_s2, col_s3 = st.columns(3)
            total = len(df_result)
            with col_s1:
                pos = (df_result["label"] == "✅ Positive").sum()
                st.metric("✅ Positive", pos, delta=f"{pos/total*100:.1f}%")
            with col_s2:
                neg = (df_result["label"] == "❌ Negative").sum()
                st.metric("❌ Negative", neg, delta=f"{neg/total*100:.1f}%")
            with col_s3:
                neu = (df_result["label"] == "⚪ Neutral").sum()
                st.metric("⚪ Neutral", neu, delta=f"{neu/total*100:.1f}%")

            # Pie chart
            fig_pie = px.pie(
                df_result, names="label", title="Sentiment Distribution",
                color="label",
                color_discrete_map={
                    "✅ Positive": "#00C853",
                    "❌ Negative": "#FF5252",
                    "⚪ Neutral": "#78909C"
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)

            # Histogram
            fig_hist = px.histogram(
                df_result, x="polarity", nbins=30,
                title="Polarity Distribution",
                labels={"polarity": "Polarity (-1 to 1)"}
            )
            st.plotly_chart(fig_hist, use_container_width=True)

            # Download
            csv_out = df_result[["text", "polarity", "subjectivity", "label", "score"]]
            st.download_button(
                "📥 Download Results CSV",
                csv_out.to_csv(index=False),
                "sentiment_results.csv",
                use_container_width=True
            )
            st.dataframe(df_result[["text", "label", "polarity", "score"]], use_container_width=True)

# ─── FOOTER ─────────────────────────────────────────────
st.divider()
st.caption("Built by Attanti Ramnivas | Powered by TextBlob + NLTK | Streamlit")
