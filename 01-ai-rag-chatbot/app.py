"""
smriti-ai — AI Memory Assistant with RAG
Built by Attanti Ramnivas | AI/ML Developer

Architecture:
1. Load documents (PDF, TXT, CSV)
2. Chunk text into embeddings
3. Store in ChromaDB vector store
4. Query with Gemini LLM + retrieved context
5. Return grounded answer with citations
"""

import os
import streamlit as st
from pathlib import Path
from langchain_community.document_loaders import (
    TextLoader, CSVLoader, PyPDFLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# ─── CONFIG ──────────────────────────────────────────────
st.set_page_config(page_title="smriti-ai", page_icon="🧠")
st.title("🧠 smriti-ai — AI Memory Assistant")

# API Key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ Set GOOGLE_API_KEY in your .env file")
    st.stop()

# ─── INITIALIZE CHROMA PERSISTENCE ───────────────────────
@st.cache_resource
def get_vectorstore():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
    return Chroma(
        persist_directory="./chroma_db",
        embedding_function=embeddings
    )

# ─── DOCUMENT LOADER ─────────────────────────────────────
def load_documents(files):
    docs = []
    for file in files:
        suffix = Path(file.name).suffix.lower()
        with open(f"./uploads/{file.name}", "wb") as f:
            f.write(file.getbuffer())
        path = f"./uploads/{file.name}"
        if suffix == ".txt":
            loader = TextLoader(path)
        elif suffix == ".csv":
            loader = CSVLoader(path)
        elif suffix == ".pdf":
            loader = PyPDFLoader(path)
        else:
            st.warning(f"Unsupported: {file.name}")
            continue
        docs.extend(loader.load())
    return docs

def chunk_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    return splitter.split_documents(docs)

def build_vectorstore(docs):
    os.makedirs("./uploads", exist_ok=True)
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=api_key
    )
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    vectorstore.persist()
    return vectorstore

# ─── QA CHAIN ────────────────────────────────────────────
def get_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4}
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.3,
        convert_system_message_to_human=True
    )
    prompt = PromptTemplate(
        template="""
You are a helpful AI assistant with access to a knowledge base.
Use the retrieved context to answer the user's question accurately.
If the answer isn't in the context, say "I don't have enough information."

CONTEXT:
{context}

QUESTION: {question}

ANSWER:""",
        input_variables=["context", "question"]
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

# ─── UI ──────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vectorstore_ready" not in st.session_state:
    st.session_state.vectorstore_ready = False

# Sidebar: Upload docs
with st.sidebar:
    st.header("📁 Knowledge Base")
    uploaded = st.file_uploader(
        "Upload documents (TXT, CSV, PDF)",
        type=["txt", "csv", "pdf"],
        accept_multiple_files=True
    )
    if uploaded and not st.session_state.vectorstore_ready:
        if st.button("🔨 Build Knowledge Base", use_container_width=True):
            with st.spinner("Loading & indexing documents..."):
                docs = load_documents(uploaded)
                chunks = chunk_documents(docs)
                st.session_state.vectorstore = build_vectorstore(chunks)
                st.session_state.vectorstore_ready = True
            st.success(f"✅ Indexed {len(chunks)} chunks!")

    if st.session_state.vectorstore_ready:
        st.success("✅ Knowledge base ready!")
        if st.button("🗑️ Clear & Reset"):
            import shutil
            shutil.rmtree("./chroma_db", ignore_errors=True)
            shutil.rmtree("./uploads", ignore_errors=True)
            st.session_state.clear()
            st.rerun()

    st.markdown("---")
    st.caption("Built with LangChain + Gemini + ChromaDB")

# Chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if query := st.chat_input("Ask me anything from your documents..."):
    if not st.session_state.vectorstore_ready:
        st.warning("⚠️ Please upload and index documents first!")
    else:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chain = get_qa_chain(st.session_state.vectorstore)
                result = chain(query)
                answer = result["result"]
                sources = result["source_documents"]

            st.markdown(answer)
            with st.expander("📚 Source References"):
                for i, doc in enumerate(sources, 1):
                    st.markdown(f"**{i}.** {doc.page_content[:300]}...")

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
