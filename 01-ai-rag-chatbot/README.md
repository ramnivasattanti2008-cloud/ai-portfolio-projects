# 🧠 smriti-ai — AI Memory Assistant

> RAG-powered chatbot that answers questions from your documents using Google Gemini + ChromaDB

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Gemini](https://img.shields.io/badge/Gemini-LLM-green)

## What it does

Upload your documents (PDF, TXT, CSV) → ask questions → get grounded answers with source citations.

## Architecture

```
User Query → Embed (Gemini) → ChromaDB → Retrieved Chunks → LLM → Answer + Citations
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| LLM | Google Gemini 2.0 Flash |
| Embeddings | Gemini Embedding-001 |
| Vector DB | ChromaDB |
| Chunking | LangChain RecursiveCharacterTextSplitter |
| Loaders | PyPDF, CSV, Text |

## Setup

```bash
cd 01-ai-rag-chatbot
pip install -r requirements.txt
echo "GOOGLE_API_KEY=your_key_here" > .env
streamlit run app.py
```

## Get Free API Keys

- **Gemini API:** [aistudio.google.com](https://aistudio.google.com)

## Features

✅ Multi-format document support (PDF, TXT, CSV)
✅ Semantic search with ChromaDB
✅ Source citations from retrieved documents
✅ Persistent vector store
✅ Streaming responses

---

**Built by Attanti Ramnivas | AI/ML Developer**
