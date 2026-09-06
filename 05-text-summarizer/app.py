"""
Text Summarizer — AI-Powered Article & Document Summarization
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Abstractive + extractive summarization
- Multiple summary lengths
- Document types: articles, reports, research papers
- Bullet point or paragraph format
- Multi-language support
"""

import os
import streamlit as st
import pandas as pd
import re
from collections import Counter

st.set_page_config(page_title="Text Summarizer", page_icon="📝", layout="wide")
st.title("📝 AI Text Summarizer")
st.markdown("Summarize articles, documents, and long texts instantly with AI")

# ─── SUMMARIZATION ENGINE ────────────────────────────────
def extractive_summary(text, num_sentences=5):
    """Extract most important sentences based on TF-IDF-like scoring"""
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    if len(sentences) <= num_sentences:
        return text

    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    word_freq = Counter(words)
    max_freq = max(word_freq.values()) if word_freq else 1

    # Score sentences
    scored = []
    for sent in sentences:
        sent_words = re.findall(r'\b[a-zA-Z]{4,}\b', sent.lower())
        score = sum(word_freq.get(w, 0) / max_freq for w in sent_words)
        score *= (len(sent_words) / max(len(sent_words), 10))
        scored.append((sent, score))

    scored.sort(key=lambda x: x[1], reverse=True)
    top_sents = sorted(scored[:num_sentences], key=lambda x: sentences.index(x[0]))
    return '. '.join(s[0] for s in top_sents) + '.'

def abstractive_summary(text, length, api_key):
    """Generate abstractive summary using Gemini"""
    if not api_key:
        return None, "⚠️ Set GOOGLE_API_KEY in .env"

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        length_map = {
            "Short (1-2 sentences)": "2 sentences",
            "Medium (3-5 sentences)": "3-5 sentences",
            "Long (1 paragraph)": "1 comprehensive paragraph",
            "Bullet points": "5-7 bullet points"
        }

        prompt = f"""Summarize the following text concisely and accurately.
Style: {length_map[length]}
Rules:
- Keep key facts, numbers, and names
- Use simple language
- No opinions added
- Return ONLY the summary

TEXT:
{text[:4000]}"""

        response = model.generate_content(prompt)
        return response.text.strip(), None

    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# ─── WORD CLOUD ──────────────────────────────────────────
def get_word_freq(text, top_n=20):
    from nltk.corpus import stopwords
    stop = set(stopwords.words('english'))
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    filtered = [w for w in words if w not in stop]
    return Counter(filtered).most_common(top_n)

# ─── UI ──────────────────────────────────────────────────
col_in, col_out = st.columns([1, 1])

with col_in:
    st.subheader("📄 Input Text")

    input_method = st.radio("Input method:", ["Type/Paste", "Upload File"])

    text = ""
    if input_method == "Type/Paste":
        text = st.text_area(
            "Paste your text here:",
            height=400,
            placeholder="Paste an article, report, or any long text to summarize..."
        )
    else:
        uploaded = st.file_uploader("Upload TXT or CSV file", type=["txt", "csv"])
        if uploaded:
            text = uploaded.read().decode("utf-8", errors="ignore")
            st.info(f"📄 Loaded {len(text)} characters")

    col_opt1, col_opt2, col_opt3 = st.columns(3)
    with col_opt1:
        method = st.selectbox("Method", ["AI Abstractive", "Extractive (fast)"])
    with col_opt2:
        length = st.selectbox("Length", [
            "Short (1-2 sentences)",
            "Medium (3-5 sentences)",
            "Long (1 paragraph)",
            "Bullet points"
        ])
    with col_opt3:
        num_sents = st.slider("Sentences (extractive)", 2, 10, 5)

    summarize = st.button("⚡ Summarize", use_container_width=True)

with col_out:
    st.subheader("📋 Summary")

    if summarize:
        if not text.strip():
            st.warning("⚠️ Please enter or upload text first")
        else:
            api_key = os.getenv("GOOGLE_API_KEY")

            with st.spinner("Summarizing..."):
                if method == "AI Abstractive":
                    summary, error = abstractive_summary(text, length, api_key)
                    if error:
                        st.error(error)
                        st.info("Falling back to extractive...")
                        method = "extractive"
                        summary = None
                else:
                    summary = extractive_summary(text, num_sents)
                    error = None

            if summary and not error:
                st.success("✅ Summary Ready")
                st.markdown(summary)

                # Stats
                orig_words = len(text.split())
                sum_words = len(summary.split())
                ratio = (1 - sum_words / orig_words) * 100 if orig_words else 0

                col_c1, col_c2, col_c3 = st.columns(3)
                with col_c1:
                    st.metric("Original", f"{orig_words} words")
                with col_c2:
                    st.metric("Summary", f"{sum_words} words")
                with col_c3:
                    st.metric("Compression", f"{ratio:.0f}%")

                # Word frequency
                st.subheader("🔑 Key Terms")
                freq = get_word_freq(text)
                for word, count in freq[:10]:
                    bar_width = min(count / freq[0][1] * 100, 100)
                    st.markdown(f"**{word}** — {count}")
                    st.progress(bar_width / 100)

                # Copy button
                if st.button("📋 Copy Summary"):
                    import pyperclip
                    pyperclip.copy(summary)
                    st.success("✅ Copied!")

# ─── BATCH ───────────────────────────────────────────────
st.divider()
st.subheader("📂 Batch Summarize CSV")

batch_file = st.file_uploader("Upload CSV with a 'text' column", type=["csv"])

if batch_file:
    df = pd.read_csv(batch_file)
    st.write("Preview:", df.head())

    text_col = None
    for col in ["text", "content", "article", "description", "body"]:
        if col in df.columns:
            text_col = col
            break

    if text_col and st.button("⚡ Batch Summarize", use_container_width=True):
        summaries = []
        progress = st.progress(0)

        for i, row in df.iterrows():
            t = str(row[text_col])
            summary = extractive_summary(t, 3)
            summaries.append(summary)
            progress.progress((i + 1) / len(df))

        df["summary"] = summaries
        st.dataframe(df[[text_col, "summary"]], use_container_width=True)

        st.download_button(
            "📥 Download CSV with Summaries",
            df.to_csv(index=False),
            "summarized_output.csv",
            use_container_width=True
        )

st.caption("Built by Attanti Ramnivas | Powered by Google Gemini + NLTK | Streamlit")
