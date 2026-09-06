# 📄 AI Document Intelligence Platform

> A unified document intelligence platform — ask questions across all your documents at once

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Gemini](https://img.shields.io/badge/Gemini-LLM-green?logo=google)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?logo=streamlit)

## What it does

Upload multiple documents (PDF, DOCX, TXT, CSV, Images) → Ask questions across ALL of them at once → Get intelligent answers with source citations.

## Architecture

```
User uploads multiple documents
        ↓
Document Processor extracts text
(PDF, DOCX, TXT, CSV, Images with OCR)
        ↓
Text chunking (1500 chars, 200 overlap)
        ↓
Combined context sent to Gemini LLM
        ↓
AI answers based on all documents
        ↓
Sources cited, chat history maintained
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| LLM | Google Gemini 2.0 Flash |
| PDF Processing | PyMuPDF (fitz) |
| DOCX | python-docx |
| CSV | Pandas |
| OCR | pytesseract + Pillow |
| Chat History | Session state |

## Setup

```bash
cd 13-ai-document-intelligence
pip install -r requirements.txt

# Install Tesseract OCR (for image processing)
# Windows: Download from github.com/UB-Mannheim/tesseract/wiki
# Linux: sudo apt install tesseract-ocr
# Mac: brew install tesseract

echo "GOOGLE_API_KEY=your_key_here" > .env
streamlit run app.py
```

## Features

✅ **Multi-format support** — PDF, DOCX, TXT, CSV, Images (PNG/JPG with OCR)
✅ **Cross-document Q&A** — Ask questions across ALL uploaded documents at once
✅ **Chat history** — Context-aware conversations with your documents
✅ **Comprehensive summaries** — AI-generated document summaries
✅ **Entity extraction** — Automatically extract people, places, dates, organizations
✅ **Document comparison** — Compare multiple documents side-by-side
✅ **Source citations** — Know exactly which document your answer comes from
✅ **Chunked processing** — Handles large documents efficiently
✅ **Download chat history** — Export your conversations

## Screens

### Chat with Documents
Ask any question across all your documents simultaneously. The AI considers all documents and provides answers with source citations.

### Document Analysis
- **Summary** — Comprehensive overview of all documents
- **Entity Extraction** — Key people, places, dates, organizations
- **Statistics** — Document count, total text, chunk analysis

### Document Comparison
Compare multiple documents to find:
- Similarities between documents
- Key differences
- Complementary information

## Use Cases

- 📚 Research paper analysis
- 📋 Contract review and comparison
- 📊 Report synthesis
- 📁 Personal knowledge management
- 🔍 Legal document review
- 📈 Business report analysis

---

**Built by Attanti Ramnivas | AI/ML Developer**
**B.Tech CSBS | Jain University, Bengaluru | 9.3 CGPA**
