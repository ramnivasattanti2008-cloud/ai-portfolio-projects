"""
YouTube Comment Analyzer — AI-Powered YouTube Feedback Analysis
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Fetch comments from any YouTube video
- Sentiment analysis (positive/negative/neutral)
- Spam detection
- Engagement metrics
- Word cloud & visualizations
- Export results
"""

import os
import re
import isodate
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from textblob import TextBlob
from collections import Counter
from googleapiclient.discovery import build

# ─── CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="YouTube Comment Analyzer",
    page_icon="📺",
    layout="wide"
)

st.title("📺 YouTube Comment Analyzer")
st.markdown("Extract, analyze, and visualize comments from any YouTube video")

API_KEY = os.getenv("YOUTUBE_API_KEY")

# ─── YOUTUBE API ─────────────────────────────────────────
def get_youtube_client():
    if not API_KEY:
        st.error("⚠️ Set YOUTUBE_API_KEY in your .env file")
        return None
    return build("youtube", "v3", developerKey=API_KEY)

def extract_video_id(url):
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"([a-zA-Z0-9_-]{11})"
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_info(youtube, video_id):
    resp = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    ).execute()
    if not resp["items"]:
        return None
    item = resp["items"][0]
    return {
        "title": item["snippet"]["title"],
        "channel": item["snippet"]["channelTitle"],
        "views": int(item["statistics"].get("viewCount", 0)),
        "likes": int(item["statistics"].get("likeCount", 0)),
        "comments": int(item["statistics"].get("commentCount", 0)),
        "duration": item["contentDetails"]["duration"],
        "published": item["snippet"]["publishedAt"][:10]
    }

def get_comments(youtube, video_id, max_results=500):
    comments = []
    next_page = None
    while len(comments) < max_results:
        resp = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=next_page,
            maxResults=min(100, max_results - len(comments)),
            textFormat="plainText"
        ).execute()
        for item in resp["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "author": comment["authorDisplayName"],
                "text": comment["textDisplay"],
                "likes": comment["likeCount"],
                "published": comment["publishedAt"][:10],
                "is_reply": item["snippet"]["isReply"],
                "total_replies": item["snippet"]["totalReplyCount"]
            })
        next_page = resp.get("nextPageToken")
        if not next_page:
            break
    return comments

# ─── ANALYSIS ENGINE ────────────────────────────────────
def analyze_comment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    spam_keywords = ["subscribe", "follow", "check out", "free money",
                     "DM me", "www.", "http", ".com", "lottery", "winner"]
    spam_score = sum(1 for kw in spam_keywords if kw.lower() in text.lower())

    if spam_score >= 2:
        sentiment = "🚫 Spam"
        emoji = "🚫"
    elif polarity > 0.1:
        sentiment = "✅ Positive"
        emoji = "😊"
    elif polarity < -0.1:
        sentiment = "❌ Negative"
        emoji = "😠"
    else:
        sentiment = "⚪ Neutral"
        emoji = "😐"

    return {
        "polarity": round(polarity, 3),
        "subjectivity": round(subjectivity, 3),
        "sentiment": sentiment,
        "emoji": emoji,
        "spam_score": spam_score,
        "word_count": len(text.split())
    }

# ─── UI ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")
    st.text_input("YouTube API Key", type="password",
                  value=API_KEY if API_KEY else "",
                  help="Get free key: console.cloud.google.com → YouTube Data API v3")
    max_comments = st.slider("Max comments to fetch", 50, 500, 200)
    st.markdown("---")
    st.caption("Get API key: [console.cloud.google.com](https://console.cloud.google.com)")

# URL input
url = st.text_input(
    "🎬 Enter YouTube Video URL:",
    placeholder="https://www.youtube.com/watch?v=..."
)

if url:
    video_id = extract_video_id(url)
    if not video_id:
        st.error("❌ Invalid YouTube URL")
    else:
        youtube = get_youtube_client()
        if youtube:
            with st.spinner("Fetching video info..."):
                info = get_video_info(youtube, video_id)

            if not info:
                st.error("❌ Video not found or comments disabled")
            else:
                # Video stats
                col_v1, col_v2, col_v3, col_v4 = st.columns(4)
                with col_v1:
                    st.metric("👁️ Views", f"{info['views']:,}")
                with col_v2:
                    st.metric("👍 Likes", f"{info['likes']:,}")
                with col_v3:
                    st.metric("💬 Comments", f"{info['comments']:,}")
                with col_v4:
                    ratio = info['likes'] / max(info['views'], 1) * 100
                    st.metric("Like/View %", f"{ratio:.1f}%")

                st.markdown(f"**{info['title']}**")
                st.markdown(f"📺 {info['channel']} | 📅 {info['published']}")

                # Fetch comments
                if st.button("🔍 Fetch & Analyze Comments", use_container_width=True):
                    with st.spinner(f"Fetching up to {max_comments} comments..."):
                        comments = get_comments(youtube, video_id, max_comments)

                    if not comments:
                        st.warning("No comments found (or comments are disabled)")
                    else:
                        # Analyze
                        results = []
                        for c in comments:
                            analysis = analyze_comment(c["text"])
                            results.append({**c, **analysis})

                        df = pd.DataFrame(results)

                        # Summary
                        st.divider()
                        st.subheader("📊 Sentiment Overview")
                        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                        total = len(df)
                        with col_s1:
                            pos = (df["sentiment"] == "✅ Positive").sum()
                            st.metric("✅ Positive", pos, delta=f"{pos/total*100:.1f}%")
                        with col_s2:
                            neg = (df["sentiment"] == "❌ Negative").sum()
                            st.metric("❌ Negative", neg, delta=f"{neg/total*100:.1f}%")
                        with col_s3:
                            neu = (df["sentiment"] == "⚪ Neutral").sum()
                            st.metric("⚪ Neutral", neu, delta=f"{neu/total*100:.1f}%")
                        with col_s4:
                            spam = (df["sentiment"] == "🚫 Spam").sum()
                            st.metric("🚫 Spam", spam, delta=f"{spam/total*100:.1f}%")

                        # Charts
                        col_c1, col_c2 = st.columns(2)
                        with col_c1:
                            fig_pie = px.pie(
                                df, names="sentiment", title="Sentiment Distribution",
                                color="sentiment",
                                color_discrete_map={
                                    "✅ Positive": "#00C853",
                                    "❌ Negative": "#FF5252",
                                    "⚪ Neutral": "#78909C",
                                    "🚫 Spam": "#FFB300"
                                }
                            )
                            st.plotly_chart(fig_pie, use_container_width=True)

                        with col_c2:
                            fig_bar = px.histogram(
                                df, x="polarity", nbins=30,
                                title="Polarity Distribution",
                                labels={"polarity": "Polarity (-1 to 1)"}
                            )
                            st.plotly_chart(fig_bar, use_container_width=True)

                        # Top positive/negative
                        col_t1, col_t2 = st.columns(2)
                        with col_t1:
                            st.subheader("😊 Top Positive Comments")
                            top_pos = df.nlargest(3, "polarity")[["author", "text", "polarity", "likes"]]
                            for _, row in top_pos.iterrows():
                                st.markdown(f"**@{row['author']}** ({row['likes']} 👍)")
                                st.markdown(f"_{row['text'][:150]}_")
                                st.markdown("")
                        with col_t2:
                            st.subheader("😠 Top Negative Comments")
                            top_neg = df.nsmallest(3, "polarity")[["author", "text", "polarity", "likes"]]
                            for _, row in top_neg.iterrows():
                                st.markdown(f"**@{row['author']}** ({row['likes']} 👍)")
                                st.markdown(f"_{row['text'][:150]}_")
                                st.markdown("")

                        # Spam
                        st.subheader("🚫 Spam Comments")
                        spam_df = df[df["sentiment"] == "🚫 Spam"]
                        if len(spam_df) > 0:
                            st.dataframe(spam_df[["author", "text", "likes"]], use_container_width=True)
                        else:
                            st.success("No spam detected!")

                        # Download
                        st.divider()
                        csv_out = df[["author", "text", "sentiment", "polarity",
                                      "subjectivity", "spam_score", "likes", "published"]]
                        st.download_button(
                            "📥 Download Full Analysis CSV",
                            csv_out.to_csv(index=False),
                            "youtube_comment_analysis.csv",
                            use_container_width=True
                        )

                        st.dataframe(
                            df[["text", "sentiment", "polarity", "likes"]],
                            use_container_width=True,
                            height=300
                        )
