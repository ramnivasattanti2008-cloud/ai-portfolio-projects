"""
AI Document Intelligence Platform
Built by Attanti Ramnivas | AI/ML Developer

A unified document intelligence platform that:
1. Reads multiple formats (PDF, DOCX, TXT, CSV, Images with OCR)
2. Answers questions across ALL documents at once
3. Generates summaries, reports, and insights
4. Extracts tables, key figures, and entities
5. Compares documents side-by-side
6. Chat history with document memory
"""

import os
import streamlit as st
import tempfile
from pathlib import Path
from datetime import datetime
from collections import defaultdict

st.set_page_config(
    page_title="AI Document Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stMainBlockContainer {padding-top: 1rem;}
.stAppHeader {display: none;}
[data-testid="stToolbar"] {display: none;}
.stAppViewContainer {padding-top: 0;}
.css-1d391kg {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)

# ─── TITLE ────────────────────────────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
    <h1 style="color: white; margin: 0; font-size: 2.5rem;">📄 AI Document Intelligence Platform</h1>
    <p style="color: rgba(255,255,255,0.9); margin: 5px 0 0 0;">Upload documents • Ask questions • Get insights across all files at once</p>
</div>
""", unsafe_allow_html=True)

# ─── CONFIG ──────────────────────────────────────────────
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

if not GOOGLE_API_KEY:
    st.warning("⚠️ Set `GOOGLE_API_KEY` in your `.env` file. Get free key at [aistudio.google.com](https://aistudio.google.com)")

# ─── SESSION STATE ────────────────────────────────────────
def init_state():
    defaults = {
        "documents": [],
        "chat_history": [],
        "uploaded_filenames": [],
        "doc_contents": {},
        "active_tab": "chat",
        "processing": False,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()

# ─── DOCUMENT PROCESSORS ─────────────────────────────────
def extract_text_from_file(file_obj, filename):
    """Extract text from various file formats"""
    suffix = Path(filename).suffix.lower()

    try:
        if suffix == ".txt":
            return file_obj.read().decode("utf-8", errors="ignore")

        elif suffix == ".pdf":
            try:
                import fitz  # PyMuPDF
                file_obj.seek(0)
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                    tmp.write(file_obj.read())
                    tmp_path = tmp.name
                doc = fitz.open(tmp_path)
                text = "\n".join(page.get_text() for page in doc)
                doc.close()
                os.unlink(tmp_path)
                return text
            except ImportError:
                # Fallback
                return f"[PDF content from {filename}]"

        elif suffix == ".docx":
            try:
                from docx import Document
                file_obj.seek(0)
                with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                    tmp.write(file_obj.read())
                    tmp_path = tmp.name
                doc = Document(tmp_path)
                text = "\n".join(para.text for para in doc.paragraphs)
                os.unlink(tmp_path)
                return text
            except ImportError:
                return f"[DOCX content from {filename}]"

        elif suffix in [".csv", ".tsv"]:
            import pandas as pd
            file_obj.seek(0)
            df = pd.read_csv(file_obj)
            text = f"CSV file: {filename}\nColumns: {', '.join(df.columns)}\nShape: {df.shape}\n\n"
            text += df.to_string(max_rows=50)
            return text

        elif suffix in [".png", ".jpg", ".jpeg", ".webp"]:
            try:
                import pytesseract
                from PIL import Image
                file_obj.seek(0)
                img = Image.open(file_obj)
                text = pytesseract.image_to_string(img)
                return f"[OCR from image {filename}]\n{text}"
            except ImportError:
                return f"[Image content from {filename} - OCR not available]"

        else:
            try:
                return file_obj.read().decode("utf-8", errors="ignore")
            except:
                return f"[Content from {filename}]"

    except Exception as e:
        return f"[Error reading {filename}: {str(e)}]"

def chunk_text(text, chunk_size=1500, overlap=200):
    """Split text into overlapping chunks"""
    if not text:
        return []
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks if chunks else [text[:3000]]

def get_combined_context():
    """Combine all document contents"""
    if not st.session_state.doc_contents:
        return "No documents uploaded yet."

    combined = []
    for fname, content in st.session_state.doc_contents.items():
        combined.append(f"=== Document: {fname} ===\n{content[:5000]}")
    return "\n\n".join(combined)

# ─── AI FUNCTIONS ─────────────────────────────────────────
def ask_ai(question, context, history):
    """Query AI with document context and chat history"""
    if not GOOGLE_API_KEY:
        return "⚠️ Please set your GOOGLE_API_KEY in .env file", None

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        history_text = ""
        if history:
            history_text = "\n".join([
                f"User: {h['user']}\nAssistant: {h['ai']}"
                for h in history[-5:]
            ])

        prompt = f"""You are an expert document analyst. You have access to multiple documents.
Answer the user's question based ONLY on the provided document content.
If the answer isn't in the documents, say "Based on the provided documents, I cannot find this information."

Be thorough but concise. Cite which document(s) your answer comes from.

{'='*60}
CHAT HISTORY (recent):
{'='*60}
{history_text if history_text else "No previous messages"}

{'='*60}
DOCUMENT CONTENT:
{'='*60}
{context[:15000]}

{'='*60}
CURRENT QUESTION:
{'='*60}
{question}

ANSWER:"""

        response = model.generate_content(prompt)
        answer = response.text

        # Extract sources
        sources = []
        for fname in st.session_state.doc_contents:
            if any(word.lower() in answer.lower() for word in fname.split(".")[0].split("_")):
                if fname not in sources:
                    sources.append(fname)

        return answer, sources

    except Exception as e:
        return f"❌ Error: {str(e)}", None

def generate_summary(context):
    """Generate a comprehensive summary of all documents"""
    if not GOOGLE_API_KEY:
        return "⚠️ Please set your GOOGLE_API_KEY in .env file", None

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""Analyze the following documents and provide a comprehensive summary.

Your analysis should include:
1. 📋 OVERVIEW: What are these documents about?
2. 🔑 KEY FINDINGS: 5-7 main takeaways
3. 📊 DATA HIGHLIGHTS: Important numbers, dates, names
4. 🔗 CONNECTIONS: How the documents relate to each other
5. 💡 INSIGHTS: What stands out or is notable

DOCUMENTS:
{context[:12000]}

ANALYSIS:"""

        response = model.generate_content(prompt)
        return response.text, None

    except Exception as e:
        return f"❌ Error: {str(e)}", None

def extract_entities(context):
    """Extract named entities from documents"""
    if not GOOGLE_API_KEY:
        return "⚠️ Please set your GOOGLE_API_KEY in .env file", None

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""Extract and categorize key entities from these documents.

For each category, list the entities found:

1. 👤 PEOPLE: Names of people mentioned
2. 🏢 ORGANIZATIONS: Companies, institutions, agencies
3. 📍 LOCATIONS: Cities, countries, places
4. 📅 DATES: Important dates and time periods
5. 💰 NUMBERS: Key statistics, figures, percentages
6. 📝 TERMS: Important technical or domain-specific terms

DOCUMENTS:
{context[:10000]}

ENTITIES:"""

        response = model.generate_content(prompt)
        return response.text, None

    except Exception as e:
        return f"❌ Error: {str(e)}", None

def compare_documents(doc_contents):
    """Compare multiple documents"""
    if not GOOGLE_API_KEY or len(doc_contents) < 2:
        return None

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        docs_text = "\n\n".join([
            f"=== {fname} ===\n{content[:3000]}"
            for fname, content in doc_contents.items()
        ])

        prompt = f"""Compare these documents and highlight:
1. SIMILARITIES: What do they have in common?
2. DIFFERENCES: What are the key differences?
3. COMPLEMENTARY INFO: How do they complement each other?

DOCUMENTS:
{docs_text}

COMPARISON:"""

        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"

# ─── SIDEBAR ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📁 Document Library")

    # File upload
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf", "docx", "txt", "csv", "png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="PDF, DOCX, TXT, CSV, Images (PNG/JPG with OCR)"
    )

    if uploaded_files:
        new_files = [f for f in uploaded_files if f.name not in st.session_state.uploaded_filenames]
        if new_files:
            with st.spinner("📖 Processing documents..."):
                for f in new_files:
                    content = extract_text_from_file(f, f.name)
                    chunks = chunk_text(content)
                    st.session_state.doc_contents[f.name] = content
                    st.session_state.documents.append({
                        "name": f.name,
                        "size": len(content),
                        "chunks": len(chunks),
                        "type": Path(f.name).suffix
                    })
                    st.session_state.uploaded_filenames.append(f.name)
                    st.success(f"✅ Added: {f.name}")

    # Document list
    st.markdown("---")
    st.markdown("**📚 Your Documents:**")

    if st.session_state.documents:
        total_chars = sum(d['size'] for d in st.session_state.documents)
        total_chunks = sum(d['chunks'] for d in st.session_state.documents)

        for doc in st.session_state.documents:
            col1, col2 = st.columns([3, 1])
            with col1:
                icon = {"pdf": "📕", "docx": "📘", "txt": "📝", "csv": "📊", ".png": "🖼️", ".jpg": "🖼️", ".jpeg": "🖼️"}.get(doc['type'], "📄")
                st.markdown(f"{icon} **{doc['name'][:25]}{'...' if len(doc['name']) > 25 else ''}**")
                st.caption(f"{doc['size']:,} chars | {doc['chunks']} chunks")
            with col2:
                if st.button("🗑️", key=f"del_{doc['name']}"):
                    st.session_state.documents = [d for d in st.session_state.documents if d['name'] != doc['name']]
                    st.session_state.uploaded_filenames = [n for n in st.session_state.uploaded_filenames if n != doc['name']]
                    del st.session_state.doc_contents[doc['name']]
                    st.rerun()

        st.markdown(f"**Total:** {len(st.session_state.documents)} docs | {total_chars:,} chars")
    else:
        st.info("📭 No documents uploaded yet")

    # Clear all
    if st.session_state.documents and st.button("🗑️ Clear All Documents", use_container_width=True):
        st.session_state.documents = []
        st.session_state.doc_contents = {}
        st.session_state.uploaded_filenames = []
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")

    # Settings
    st.markdown("**⚙️ Settings**")
    st.caption(f"Model: gemini-2.0-flash")
    st.caption(f"API Key: {'✅ Set' if GOOGLE_API_KEY else '❌ Missing'}")

# ─── MAIN TABS ────────────────────────────────────────────
tab_chat, tab_analyze, tab_compare, tab_history = st.tabs(
    ["💬 Chat with Docs", "📊 Analyze", "⚖️ Compare", "📜 History"]
)

# ─── CHAT TAB ─────────────────────────────────────────────
with tab_chat:
    col_ql, col_qr = st.columns([4, 1])
    with col_ql:
        question = st.text_input(
            "Ask a question about your documents:",
            placeholder="e.g., What are the main findings in these documents?",
            label_visibility="collapsed"
        )
    with col_qr:
        ask = st.button("🔍 Ask", use_container_width=True)

    if ask and question:
        if not st.session_state.doc_contents:
            st.warning("⚠️ Please upload documents first!")
        else:
            with st.spinner("🤖 Analyzing documents..."):
                context = get_combined_context()
                answer, sources = ask_ai(question, context, st.session_state.chat_history)

            st.session_state.chat_history.append({
                "user": question,
                "ai": answer,
                "time": datetime.now().strftime("%H:%M")
            })

            # Display answer
            st.markdown("---")
            st.markdown(f"### 💬 Answer")
            st.markdown(answer)

            if sources:
                st.markdown(f"**📄 Sources:** {', '.join(sources)}")

            # Quick suggestions
            st.markdown("**💡 Try asking:**")
            suggestions = [
                "What is this document about?",
                "What are the key findings?",
                "Summarize the main points",
                "What data or numbers are mentioned?"
            ]
            cols = st.columns(2)
            for i, s in enumerate(suggestions):
                with cols[i % 2]:
                    if st.button(s, key=f"sug_{i}"):
                        st.session_state.chat_history.append({
                            "user": s,
                            "ai": "",
                            "time": datetime.now().strftime("%H:%M")
                        })

    # Chat display
    if st.session_state.chat_history:
        st.markdown("---")
        for i, msg in enumerate(reversed(st.session_state.chat_history[-10:])):
            with st.chat_message("user"):
                st.markdown(f"**You:** {msg['user']}")
            with st.chat_message("assistant"):
                st.markdown(msg['ai'])
                st.caption(f"🕐 {msg['time']}")
            st.markdown("")

# ─── ANALYZE TAB ──────────────────────────────────────────
with tab_analyze:
    if not st.session_state.doc_contents:
        st.info("📭 Upload documents to analyze them")
    else:
        col_a1, col_a2 = st.columns(2)

        with col_a1:
            if st.button("📋 Generate Summary", use_container_width=True):
                with st.spinner("📝 Generating summary..."):
                    context = get_combined_context()
                    summary, _ = generate_summary(context)
                st.session_state.analysis_summary = summary

            if "analysis_summary" in st.session_state:
                st.markdown("#### 📋 Summary")
                st.markdown(st.session_state.analysis_summary)

        with col_a2:
            if st.button("🏷️ Extract Entities", use_container_width=True):
                with st.spinner("🏷️ Extracting entities..."):
                    context = get_combined_context()
                    entities, _ = extract_entities(context)
                st.session_state.analysis_entities = entities

            if "analysis_entities" in st.session_state:
                st.markdown("#### 🏷️ Key Entities")
                st.markdown(st.session_state.analysis_entities)

        # Stats
        st.markdown("---")
        st.markdown("#### 📊 Document Statistics")

        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        with col_s1:
            st.metric("📁 Documents", len(st.session_state.documents))
        with col_s2:
            total = sum(d['size'] for d in st.session_state.documents)
            st.metric("📝 Total Text", f"{total:,} chars")
        with col_s3:
            total_chunks = sum(d['chunks'] for d in st.session_state.documents)
            st.metric("🔢 Chunks", total_chunks)
        with col_s4:
            st.metric("💬 Messages", len(st.session_state.chat_history))

        # Document overview
        st.markdown("#### 📄 Document Overview")
        for doc in st.session_state.documents:
            with st.expander(f"📄 {doc['name']}"):
                content = st.session_state.doc_contents.get(doc['name'], "")[:2000]
                st.markdown(f"**Preview (first 2000 chars):**\n\n{content}...")

# ─── COMPARE TAB ───────────────────────────────────────────
with tab_compare:
    if len(st.session_state.doc_contents) < 2:
        st.info(f"📭 Upload at least 2 documents to compare. Currently: {len(st.session_state.doc_contents)}")
    else:
        st.markdown(f"### ⚖️ Comparing {len(st.session_state.doc_contents)} Documents")

        if st.button("🔍 Run Comparison", use_container_width=True):
            with st.spinner("⚖️ Comparing documents..."):
                comparison = compare_documents(st.session_state.doc_contents)
            st.session_state.comparison_result = comparison

        if "comparison_result" in st.session_state:
            st.markdown("#### Comparison Results")
            st.markdown(st.session_state.comparison_result)

        # Side-by-side
        st.markdown("---")
        st.markdown("#### 📑 Side-by-Side Preview")
        docs = list(st.session_state.doc_contents.items())
        cols = st.columns(len(docs))
        for i, (fname, content) in enumerate(docs):
            with cols[i]:
                st.markdown(f"**{fname}**")
                st.text_area(f"Content", value=content[:1500], height=200, label_visibility="collapsed", key=f"compare_{fname}")

# ─── HISTORY TAB ───────────────────────────────────────────
with tab_history:
    st.markdown("### 📜 Chat History")

    if st.session_state.chat_history:
        for i, msg in enumerate(st.session_state.chat_history):
            with st.expander(f"💬 {msg['time']} — {msg['user'][:50]}..."):
                st.markdown(f"**You:** {msg['user']}")
                st.markdown(f"**AI:** {msg['ai']}")

        col_h1, col_h2 = st.columns(2)
        with col_h1:
            if st.button("📥 Download Chat History", use_container_width=True):
                import json
                history_text = "\n\n".join([
                    f"=== {m['time']} ===\nYou: {m['user']}\n\nAI: {m['ai']}"
                    for m in st.session_state.chat_history
                ])
                st.download_button(
                    "📥 Download as TXT",
                    history_text,
                    "chat_history.txt",
                    use_container_width=True
                )
        with col_h2:
            if st.button("🗑️ Clear Chat History", use_container_width=True):
                st.session_state.chat_history = []
                for key in ["analysis_summary", "analysis_entities", "comparison_result"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
    else:
        st.info("💬 No chat history yet. Ask a question to start!")

st.markdown("---")
st.caption("Built by Attanti Ramnivas | Powered by Google Gemini | Streamlit")
