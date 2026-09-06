# 📝 AI Text Summarizer

> Summarize articles, reports, and documents with AI — extractive + abstractive modes

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Gemini](https://img.shields.io/badge/Gemini-LLM-green)

## What it does

Paste any text or article → choose length → get a concise, accurate summary with key terms highlighted.

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| LLM | Google Gemini 2.0 Flash |
| NLP | NLTK |
| Visualization | Plotly |
| Data | Pandas |

## Setup

```bash
cd 05-text-summarizer
pip install -r requirements.txt
echo "GOOGLE_API_KEY=your_key_here" > .env
streamlit run app.py
```

## Methods

| Method | How it works |
|--------|-------------|
| **AI Abstractive** | Gemini generates a new summary from scratch |
| **Extractive** | TF-IDF scoring extracts most important sentences |

## Features

✅ AI abstractive summarization (Gemini)
✅ Fast extractive summarization (no API needed)
✅ Multiple lengths (short/medium/long/bullet)
✅ Key terms highlighted with frequency bars
✅ Batch CSV summarization
✅ Compression ratio displayed
✅ Copy to clipboard
✅ Download results

---

**Built by Attanti Ramnivas | AI/ML Developer**
