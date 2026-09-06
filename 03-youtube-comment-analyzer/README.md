# 📺 YouTube Comment Analyzer

> Extract and analyze comments from any YouTube video with AI-powered sentiment analysis

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![YouTube API](https://img.shields.io/badge/YouTube-v3-red)

## What it does

Paste a YouTube URL → fetch comments → analyze sentiment → detect spam → visualize results → export data.

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| YouTube API | googleapiclient (YouTube Data API v3) |
| NLP | TextBlob |
| Visualization | Plotly |
| Data | Pandas |

## Setup

```bash
cd 03-youtube-comment-analyzer
pip install -r requirements.txt
echo "YOUTUBE_API_KEY=your_key_here" > .env
streamlit run app.py
```

## Get Free API Key

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create project → Enable "YouTube Data API v3"
3. Create credentials → API Key

## Features

✅ Fetch comments from any YouTube video
✅ Sentiment analysis (positive/negative/neutral/spam)
✅ Spam comment detection
✅ Top positive/negative comment highlights
✅ Engagement metrics (likes per comment)
✅ Sentiment distribution charts
✅ Export results as CSV
✅ Batch analysis up to 500 comments

---

**Built by Attanti Ramnivas | AI/ML Developer**
