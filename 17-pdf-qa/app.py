"""
PDF Q&A - Ask questions about any PDF document
"""
import streamlit as st
import google.genai as genai
import os
import tempfile

st.set_page_config(page_title="PDF QA", page_icon="PDF", layout="wide")

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("AI PDF Q&A")
st.markdown("*Upload a PDF and ask any question about its content*")

with st.sidebar:
    st.title("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    
    if uploaded_file:
        with st.spinner("Extracting text..."):
            try:
                import fitz
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                doc = fitz.open(tmp_path)
                text = "
".join([page.get_text() for page in doc])
                doc.close()
                st.session_state.pdf_text = text
                st.session_state.pdf_name = uploaded_file.name
                st.success(f"Extracted {len(text):,} characters")
            except ImportError:
                st.warning("Install PyMuPDF: pip install pymupdf")

    if st.session_state.pdf_text:
        st.info(f"PDF: {st.session_state.pdf_name}")
        st.metric("Characters", f"{len(st.session_state.pdf_text):,}")
        if st.button("Clear PDF"):
            st.session_state.pdf_text = ""
            st.session_state.pdf_name = ""
            st.session_state.chat_history = []
            st.rerun()

if not st.session_state.pdf_text:
    st.info("Upload a PDF from the sidebar to get started")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("Academic: Research paper summaries")
    with col2:
        st.info("Business: Contract analysis")
    with col3:
        st.info("Technical: Code documentation")
else:
    st.subheader("Ask Questions")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if question := st.chat_input(f"Ask about {st.session_state.pdf_name}..."):
        if os.environ.get("GOOGLE_API_KEY"):
            client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
            st.session_state.chat_history.append({"role": "user", "content": question})
            pdf_context = st.session_state.pdf_text[:15000]
            prompt = f"You are an AI assistant analyzing a PDF document. Answer based ONLY on the provided text.

Document: {pdf_context}

Question: {question}

If the answer is not in the document, say so."
            response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            st.rerun()

    quick_questions = ["What is this document about?", "What are the main points?", "Summarize in 3 bullet points"]
    cols = st.columns(3)
    for i, q in enumerate(quick_questions):
        if cols[i].button(q):
            if os.environ.get("GOOGLE_API_KEY"):
                client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
                st.session_state.chat_history.append({"role": "user", "content": q})
                prompt = f"Document: {st.session_state.pdf_text[:15000]}

Question: {q}"
                response = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                st.rerun()
