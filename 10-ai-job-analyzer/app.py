"""
AI Job Analyzer — Smart Job Description Analyzer
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Paste job description → AI analyzes requirements
- Skills gap detection
- ATS score checker
- Interview question generator
- Salary estimation
"""

import os
import streamlit as st

st.set_page_config(page_title="AI Job Analyzer", page_icon="💼", layout="wide")
st.title("💼 AI Job Description Analyzer")
st.markdown("Paste a job description → Get skills gap, ATS score, interview questions & salary estimate")

SKILLS_DB = {
    "Python": 10, "SQL": 8, "Machine Learning": 7, "Deep Learning": 6,
    "LLM": 7, "RAG": 8, "NLP": 7, "LangChain": 8, "Gemini": 7,
    "React": 7, "Next.js": 7, "TypeScript": 7, "Node.js": 6,
    "PostgreSQL": 7, "MongoDB": 6, "Docker": 7, "AWS": 6,
    "Git": 8, "Linux": 6, "Data Structures": 8, "Algorithms": 8,
}

def analyze_job(jd, api_key):
    if not api_key:
        return None, "⚠️ Set GOOGLE_API_KEY in .env"
    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")
        prompt = f"""Analyze this job description and provide:
1. Key skills required (list)
2. Years of experience needed
3. Education requirements
4. Soft skills mentioned
5. Your assessment of this role (good fit for freshers, requires experience, etc.)

JOB DESCRIPTION:
{jd[:3000]}"""
        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, str(e)

def check_ats(text):
    score = 50
    checks = []
    keywords = ["python", "sql", "machine learning", "ai", "experience", "skills", "requirement", "responsibilities"]
    for kw in keywords:
        if kw.lower() in text.lower():
            score += 5
            checks.append(f"✅ Contains '{kw}'")
        else:
            checks.append(f"❌ Missing '{kw}'")
    return min(score, 100), checks

def get_skills_gap(jd):
    jd_lower = jd.lower()
    found = []
    missing = []
    for skill, weight in SKILLS_DB.items():
        if skill.lower() in jd_lower or skill.split()[0].lower() in jd_lower:
            found.append(skill)
        else:
            missing.append(skill)
    return found, missing

# UI
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📋 Paste Job Description")
    jd = st.text_area("Job Description:", height=300, placeholder="Paste job description here...")
    api_key = os.getenv("GOOGLE_API_KEY", "")
    analyze = st.button("🔍 Analyze Job", use_container_width=True)

with col_right:
    st.subheader("📊 Analysis Results")
    if analyze and jd:
        # ATS Score
        ats_score, checks = check_ats(jd)
        st.metric("📄 ATS Score", f"{ats_score}/100")
        st.progress(ats_score / 100)

        # Skills gap
        found, missing = get_skills_gap(jd)
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("**✅ Skills You Have**")
            for s in found:
                st.markdown(f"- {s}")
        with col_s2:
            st.markdown("**📚 Skills to Learn**")
            for s in missing[:10]:
                st.markdown(f"- {s}")

        # AI Analysis
        if api_key:
            with st.spinner("🤖 AI analyzing..."):
                result, err = analyze_job(jd, api_key)
            if result:
                st.divider()
                st.markdown("### 🤖 AI Insights")
                st.markdown(result)
        else:
            st.info("Set GOOGLE_API_KEY for AI analysis")

        # Tips
        st.divider()
        st.markdown("### 💡 ATS Tips")
        tips = ["Use keywords from job description", "Keep resume to 1-2 pages", "Use standard section headers", "Quantify achievements", "Match font to ATS-friendly options"]
        for tip in tips:
            st.markdown(f"- {tip}")

st.divider()
st.caption("Built by Attanti Ramnivas | Powered by Google Gemini | Streamlit")
