"""
AI Code Reviewer — Intelligent Code Analysis Tool
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Paste any code → AI reviews it
- Bug detection, security issues
- Performance optimization suggestions
- Best practices recommendations
- Multi-language support (Python, JS, TS, Java, C++)
"""

import os
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI Code Reviewer", page_icon="🤖", layout="wide")
st.title("🤖 AI Code Reviewer")
st.markdown("Paste your code → Get instant AI-powered code review with bug detection, security fixes & optimization tips")

# Language detection
LANGUAGES = {
    "Python": "python",
    "JavaScript": "javascript",
    "TypeScript": "typescript",
    "Java": "java",
    "C++": "cpp",
    "Go": "go",
    "Rust": "rust",
    "SQL": "sql"
}

def analyze_code(code, language, api_key):
    if not api_key:
        return None, "⚠️ Set GOOGLE_API_KEY in .env"

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""You are an expert code reviewer. Review the following {language} code.

Provide a structured review with:

1. 🔴 BUGS & ERRORS
   - List specific bugs, logical errors, or runtime issues
   - Show corrected code snippets

2. 🟡 CODE QUALITY
   - Readability, naming conventions, comments
   - Code structure and organization

3. 🔵 PERFORMANCE
   - Optimization suggestions
   - Time/space complexity improvements

4. 🟢 BEST PRACTICES
   - Language-specific best practices to follow
   - Design patterns if applicable

5. 🚨 SECURITY
   - Potential security vulnerabilities
   - Secure coding recommendations

6. 💡 IMPROVEMENTS
   - Refactoring suggestions
   - Alternative implementations

CODE TO REVIEW:
```{language}
{code}
```

Format your response clearly with emojis, code blocks, and actionable feedback."""

        response = model.generate_content(prompt)
        return response.text, None
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# UI
col_left, col_right = st.columns([1, 1])

with col_left:
    st.subheader("📝 Paste Your Code")

    language = st.selectbox("💻 Language", list(LANGUAGES.keys()))
    code = st.text_area(
        "Paste code here:",
        height=400,
        placeholder=f"# Paste your {language} code here...\n\n# Example:\ndef hello():\n#    print('Hello, World!')"
    )

    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        st.warning("⚠️ Set GOOGLE_API_KEY in your .env file")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        review = st.button("🔍 Review Code", use_container_width=True)
    with col_btn2:
        st.session_state.code = code
        if st.button("📋 Clear", use_container_width=True):
            st.session_state.code = ""
            st.rerun()

    # Quick templates
    st.divider()
    st.subheader("📚 Quick Templates")
    templates = {
        "Python Function": "def calculate_fibonacci(n):\n    if n <= 0:\n        return 0\n    elif n == 1:\n        return 1\n    else:\n        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
        "JavaScript Async": "async function fetchData(url) {\n    const response = await fetch(url);\n    const data = await response.json();\n    return data;\n}",
        "SQL Query": "SELECT u.name, COUNT(o.id) as orders\nFROM users u\nLEFT JOIN orders o ON u.id = o.user_id\nGROUP BY u.name\nORDER BY orders DESC\nLIMIT 10;"
    }

    template = st.selectbox("Load template:", ["None"] + list(templates.keys()))
    if template != "None":
        st.code(templates[template], language=LANGUAGES[language].lower())

with col_right:
    st.subheader("📊 Review Results")

    if review:
        if not code.strip():
            st.warning("⚠️ Please paste some code first")
        else:
            with st.spinner("🔄 Analyzing code..."):
                result, error = analyze_code(code, language, api_key)

            if error:
                st.error(error)
            else:
                st.success("✅ Review Complete")

                # Parse sections
                lines = result.split('\n')
                section = None
                sections = {}

                for line in lines:
                    if any(s in line for s in ['🔴', 'BUGS', 'ERRORS']):
                        section = 'bugs'
                        sections.setdefault(section, []).append(line)
                    elif any(s in line for s in ['🟡', 'QUALITY']):
                        section = 'quality'
                        sections.setdefault(section, []).append(line)
                    elif any(s in line for s in ['🔵', 'PERFORMANCE']):
                        section = 'performance'
                        sections.setdefault(section, []).append(line)
                    elif any(s in line for s in ['🟢', 'BEST PRACTICES']):
                        section = 'best'
                        sections.setdefault(section, []).append(line)
                    elif any(s in line for s in ['🚨', 'SECURITY']):
                        section = 'security'
                        sections.setdefault(section, []).append(line)
                    elif any(s in line for s in ['💡', 'IMPROVEMENTS']):
                        section = 'improvements'
                        sections.setdefault(section, []).append(line)
                    elif section:
                        sections[section].append(line)

                # Display with tabs
                tabs = st.tabs([
                    "🔴 Bugs", "🟡 Quality", "🔵 Performance",
                    "🟢 Best Practices", "🚨 Security", "💡 Improvements"
                ])

                tab_map = ['bugs', 'quality', 'performance', 'best', 'security', 'improvements']

                for i, tab in enumerate(tabs):
                    with tab:
                        content = '\n'.join(sections.get(tab_map[i], ["No issues found! ✅"]))
                        st.markdown(content)

                        # Check for code blocks in this section
                        if '```' in content:
                            st.info("📋 Code suggestions found above")

                # Summary score
                st.divider()
                st.subheader("📈 Quick Summary")

                col_s1, col_s2, col_s3 = st.columns(3)

                bug_count = len(sections.get('bugs', [])) // 3
                perf_count = len(sections.get('performance', [])) // 3
                sec_count = len(sections.get('security', [])) // 3

                with col_s1:
                    st.metric("🐛 Bugs Found", bug_count,
                             delta="Fix these first!" if bug_count > 0 else "Clean!")
                with col_s2:
                    st.metric("⚡ Optimizations", perf_count,
                             delta="Can be improved" if perf_count > 0 else "Good!")
                with col_s3:
                    st.metric("🔒 Security", sec_count,
                             delta="Needs attention" if sec_count > 0 else "Safe!")

                # Overall rating
                score = max(0, 100 - bug_count * 15 - perf_count * 5 - sec_count * 20)
                st.progress(score / 100)
                st.markdown(f"**Code Health Score: {score}/100**")

                # Copy review
                if st.button("📋 Copy Full Review"):
                    import pyperclip
                    pyperclip.copy(result)
                    st.success("✅ Copied to clipboard!")

                # Save review
                if st.button("💾 Save Review"):
                    filename = f"code_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"Code Review - {datetime.now()}\n")
                        f.write(f"Language: {language}\n")
                        f.write(f"{'='*50}\n\n")
                        f.write(result)
                    st.success(f"✅ Saved as {filename}")

st.divider()
st.caption("Built by Attanti Ramnivas | Powered by Google Gemini | Streamlit")
