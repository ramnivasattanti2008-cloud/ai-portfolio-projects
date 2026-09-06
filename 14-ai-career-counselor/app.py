"""
AI Career Counselor — Smart Career Guidance Platform
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Career path recommendation based on skills
- Resume analysis and improvement suggestions
- Interview preparation with AI mock interviews
- Skill gap analysis
- Industry insights and trends
- Personalized learning roadmap
"""

import os
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="AI Career Counselor", page_icon="🎯", layout="wide")
st.title("🎯 AI Career Counselor")
st.markdown("Your personal AI-powered career advisor — resume analysis, mock interviews, skill mapping, and learning roadmaps")

# Session state
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Career data
CAREER_PATHS = {
    "AI/ML Engineer": {
        "skills": ["Python", "Machine Learning", "Deep Learning", "LLMs", "RAG", "PyTorch", "TensorFlow", "SQL", "Git"],
        "salary": "₹8-25 LPA (India) | $120-200K (USA)",
        "growth": "⭐⭐⭐⭐⭐",
        "demand": "Very High",
        "companies": ["Google", "Microsoft", "OpenAI", "Anthropic", "Razorpay", "Google DeepMind"],
        "roadmap": [
            "Master Python & SQL fundamentals",
            "Learn Machine Learning (scikit-learn, regression, classification)",
            "Deep Learning (CNN, RNN, Transformers)",
            "Specialize in LLMs & RAG",
            "Build production ML systems",
            "Contribute to open source"
        ]
    },
    "Full-Stack Developer": {
        "skills": ["JavaScript", "React", "Node.js", "TypeScript", "PostgreSQL", "Docker", "AWS", "Git"],
        "salary": "₹6-18 LPA (India) | $80-150K (USA)",
        "growth": "⭐⭐⭐⭐",
        "demand": "High",
        "companies": ["Google", "Meta", "Amazon", "Flipkart", "Meesho", "Paytm"],
        "roadmap": [
            "HTML, CSS, JavaScript fundamentals",
            "React or Next.js frontend",
            "Node.js or Express backend",
            "Database design (SQL + NoSQL)",
            "DevOps basics (Docker, GitHub Actions)",
            "System design & scalability"
        ]
    },
    "Data Scientist": {
        "skills": ["Python", "SQL", "Statistics", "Machine Learning", "Pandas", "Visualization", "Tableau", "Excel"],
        "salary": "₹7-20 LPA (India) | $90-160K (USA)",
        "growth": "⭐⭐⭐⭐",
        "demand": "High",
        "companies": ["Amazon", "Netflix", "Uber", "Zomato", "Swiggy", "PhonePe"],
        "roadmap": [
            "Statistics & probability fundamentals",
            "Python for data (Pandas, NumPy)",
            "SQL advanced queries",
            "Machine Learning algorithms",
            "Data visualization (Tableau, Plotly)",
            "Big Data basics (Spark, Hadoop)"
        ]
    },
    "Backend Engineer": {
        "skills": ["Python", "Go", "Java", "SQL", "Redis", "Kafka", "Docker", "Kubernetes", "AWS"],
        "salary": "₹8-22 LPA (India) | $100-180K (USA)",
        "growth": "⭐⭐⭐⭐",
        "demand": "Very High",
        "companies": ["Google", "Amazon", "Microsoft", "Razorpay", "CoinDCX", "Cred"],
        "roadmap": [
            "One backend language (Python/Go/Java)",
            "REST API design",
            "Database mastery (SQL + NoSQL)",
            "Caching & message queues",
            "Docker & Kubernetes",
            "System design & microservices"
        ]
    },
    "DevOps Engineer": {
        "skills": ["Linux", "Docker", "Kubernetes", "AWS", "Terraform", "CI/CD", "Python", "Monitoring"],
        "salary": "₹8-20 LPA (India) | $90-160K (USA)",
        "growth": "⭐⭐⭐⭐",
        "demand": "High",
        "companies": ["Google", "Amazon", "Microsoft", "Cloudflare", "Deloitte"],
        "roadmap": [
            "Linux administration basics",
            "Networking fundamentals",
            "Docker & containerization",
            "Kubernetes orchestration",
            "Cloud platforms (AWS/GCP/Azure)",
            "Infrastructure as Code (Terraform)"
        ]
    },
    "Product Manager": {
        "skills": ["Product Strategy", "User Research", "Data Analysis", "Communication", "Agile", "SQL"],
        "salary": "₹12-30 LPA (India) | $120-200K (USA)",
        "growth": "⭐⭐⭐⭐⭐",
        "demand": "High",
        "companies": ["Google", "Meta", "Amazon", "Flipkart", "Meesho", "CRED"],
        "roadmap": [
            "Learn product discovery & user research",
            "Data-driven decision making (SQL, analytics)",
            "Communication & stakeholder management",
            "Agile/Scrum methodologies",
            "Build product sense & intuition",
            "Portfolio of projects & case studies"
        ]
    }
}

def analyze_career_fit(user_skills, target_career):
    career = CAREER_PATHS[target_career]
    user_skills_lower = [s.lower() for s in user_skills]
    career_skills_lower = [s.lower() for s in career["skills"]]

    matched = []
    missing = []
    for skill in career_skills_lower:
        if any(skill in user_skill or user_skill in skill for user_skill in user_skills_lower):
            matched.append(skill)
        else:
            missing.append(skill)

    fit_score = len(matched) / len(career_skills_lower) * 100
    return fit_score, matched, missing

def generate_roadmap(career, api_key):
    if not api_key:
        return None
    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")
        prompt = f"""Create a personalized learning roadmap for someone targeting {career} career.
Include:
1. Week-by-week learning plan (12 weeks)
2. Key milestones
3. Best resources (free)
4. Projects to build
5. How to showcase to employers

Return as structured markdown."""
        response = model.generate_content(prompt)
        return response.text
    except:
        return None

def mock_interview(role, topic, api_key):
    if not api_key:
        return "⚠️ Set GOOGLE_API_KEY for AI-generated questions"
    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")
        prompt = f"""Generate 5 interview questions for a {role} role focusing on {topic}.
For each question include:
1. The question
2. What interviewers look for
3. A strong answer framework
4. Example answer

Format clearly with numbering."""
        response = model.generate_content(prompt)
        return response.text
    except:
        return None

def career_advice(goal, profile, api_key):
    if not api_key:
        return None
    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")
        skills = ", ".join(profile.get("skills", []))
        prompt = f"""Career advice for someone with these skills: {skills}
Their goal: {goal}
Their background: {profile.get('education', 'Student')}
Their experience: {profile.get('experience', 'Fresher')}

Provide:
1. Recommended career paths
2. Immediate next steps
3. 6-month plan
4. Resources to use"""
        response = model.generate_content(prompt)
        return response.text
    except:
        return None

# UI Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 My Profile", "🎯 Career Match", "📝 Mock Interview", "📚 Learning Path", "💬 AI Advisor"
])

# ─── PROFILE TAB ─────────────────────────────────────────
with tab1:
    st.subheader("👤 Your Profile")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Name", value=st.session_state.profile.get("name", ""))
            education = st.selectbox("Education", [
                "B.Tech/BE", "BCA/BSc", "MBA", "M.Tech/ME", "MCA", "Other"
            ], index=0)
            branch = st.text_input("Branch/Specialization", value=st.session_state.profile.get("branch", "CS/IT"))
            year = st.selectbox("Current Year", ["1st", "2nd", "3rd", "4th", "Graduate", "Working Professional"])

        with col2:
            skills = st.text_area(
                "Skills (comma-separated)",
                value=", ".join(st.session_state.profile.get("skills", [])),
                placeholder="Python, SQL, JavaScript, React, Machine Learning..."
            )
            experience = st.selectbox("Experience", [
                "Fresher (0 years)",
                "Intern (0-1 years)",
                "Junior (1-2 years)",
                "Mid-level (3-5 years)",
                "Senior (5+ years)"
            ])
            target = st.text_input("Target Role", value=st.session_state.profile.get("target", ""))

        if st.form_submit_button("💾 Save Profile"):
            st.session_state.profile = {
                "name": name,
                "education": education,
                "branch": branch,
                "year": year,
                "skills": [s.strip() for s in skills.split(",") if s.strip()],
                "experience": experience,
                "target": target
            }
            st.success("✅ Profile saved!")

    # Display profile
    if st.session_state.profile:
        st.divider()
        st.markdown(f"### 📋 {st.session_state.profile.get('name', 'Profile')}")
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            st.metric("Education", st.session_state.profile.get("education", "-"))
        with col_p2:
            st.metric("Experience", st.session_state.profile.get("experience", "-"))
        with col_p3:
            st.metric("Skills", len(st.session_state.profile.get("skills", [])))

        st.markdown("**Skills:** " + ", ".join([f"`{s}`" for s in st.session_state.profile.get("skills", [])]))

# ─── CAREER MATCH TAB ────────────────────────────────────
with tab2:
    st.subheader("🎯 Career Path Matching")

    user_skills = st.session_state.profile.get("skills", [])
    if not user_skills:
        st.warning("⚠️ Please add skills in 'My Profile' tab first")
    else:
        st.markdown(f"**Your skills:** {', '.join(user_skills)}")
        st.divider()

        results = []
        for career in CAREER_PATHS:
            fit, matched, missing = analyze_career_fit(user_skills, career)
            results.append((career, fit, matched, missing))

        results.sort(key=lambda x: x[1], reverse=True)

        for career, fit, matched, missing in results:
            with st.expander(f"🎯 {career} — {fit:.0f}% Match"):
                col_c1, col_c2, col_c3, col_c4 = st.columns(4)
                with col_c1:
                    st.metric("Match Score", f"{fit:.0f}%")
                with col_c2:
                    st.metric("Growth", CAREER_PATHS[career]["growth"])
                with col_c3:
                    st.metric("Demand", CAREER_PATHS[career]["demand"])
                with col_c4:
                    st.metric("Salary", CAREER_PATHS[career]["salary"][:15])

                st.markdown("**Matched skills:**")
                if matched:
                    st.markdown("✅ " + ", ".join([f"`{s}`" for s in matched]))
                else:
                    st.markdown("None")

                st.markdown("**Skills to learn:**")
                if missing:
                    for m in missing[:5]:
                        st.markdown(f"❌ {m}")
                else:
                    st.markdown("🎉 You have all required skills!")

                st.markdown("**Companies hiring:** " + ", ".join(CAREER_PATHS[career]["companies"][:5]))

                # AI roadmap
                api_key = os.getenv("GOOGLE_API_KEY", "")
                if api_key and st.button(f"📚 Get Roadmap for {career}", key=f"road_{career}"):
                    with st.spinner("Generating roadmap..."):
                        roadmap = generate_roadmap(career, api_key)
                    if roadmap:
                        st.markdown("### Your Learning Roadmap")
                        st.markdown(roadmap)

# ─── MOCK INTERVIEW TAB ──────────────────────────────────
with tab3:
    st.subheader("📝 AI Mock Interview")

    col_i1, col_i2 = st.columns([1, 1])
    with col_i1:
        role = st.selectbox("Target Role", list(CAREER_PATHS.keys()))
    with col_i2:
        topic = st.selectbox("Focus Area", [
            "General", "Technical", "Behavioral", "Problem Solving",
            "System Design", "Projects", "Algorithms", "Leadership"
        ])

    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        st.warning("⚠️ Set GOOGLE_API_KEY for AI-generated questions")

    if st.button("🎯 Generate Questions", use_container_width=True):
        questions = mock_interview(role, topic, api_key)
        if questions:
            st.session_state.interview_questions = questions
            st.rerun()

    if st.session_state.interview_questions:
        st.markdown("### Interview Questions")
        st.markdown(st.session_state.interview_questions)

        if st.button("📋 Clear Questions", use_container_width=True):
            st.session_state.interview_questions = []

    # Common questions
    st.divider()
    st.markdown("### 📚 Common Questions by Role")

    common_qs = {
        "AI/ML Engineer": [
            "Explain the difference between supervised and unsupervised learning",
            "What is the vanishing gradient problem?",
            "How would you handle imbalanced datasets?",
            "Explain attention mechanism in Transformers",
            "What is RAG? When would you use it?"
        ],
        "Full-Stack Developer": [
            "Explain the difference between var, let, and const",
            "What is the event loop in JavaScript?",
            "How do you handle authentication in web apps?",
            "Explain REST vs GraphQL",
            "What is Docker and why use it?"
        ],
        "Data Scientist": [
            "What is the difference between correlation and causation?",
            "Explain overfitting and how to prevent it",
            "How do you handle missing values in a dataset?",
            "Explain the bias-variance tradeoff",
            "What is A/B testing and when would you use it?"
        ]
    }

    if role in common_qs:
        st.markdown(f"**{role}:**")
        for i, q in enumerate(common_qs[role], 1):
            st.markdown(f"{i}. {q}")

# ─── LEARNING PATH TAB ──────────────────────────────────
with tab4:
    st.subheader("📚 Personalized Learning Path")

    target = st.selectbox("Select career path:", list(CAREER_PATHS.keys()))

    career = CAREER_PATHS[target]

    st.markdown(f"### 🎯 {target}")

    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        st.metric("Demand", career["demand"])
    with col_l2:
        st.metric("Growth", career["growth"])
    with col_l3:
        st.metric("Salary", career["salary"][:20])

    st.markdown("**Required Skills:**")
    cols_skills = st.columns(3)
    for i, skill in enumerate(career["skills"]):
        with cols_skills[i % 3]:
            st.markdown(f"✅ {skill}")

    st.markdown("**Companies:** " + ", ".join(career["companies"]))

    st.divider()
    st.markdown("### 📅 Suggested Roadmap")

    roadmap_items = career["roadmap"]
    for i, step in enumerate(roadmap_items, 1):
        with st.expander(f"Week {i}: {step}"):
            st.markdown(f"**Focus:** {step}")
            st.markdown("**Action items:**")
            st.markdown("- [ ] Learn core concepts")
            st.markdown("- [ ] Build a small project")
            st.markdown("- [ ] Add to GitHub portfolio")
            st.markdown("- [ ] Write a blog post")
            st.markdown("- [ ] Share on LinkedIn")

    # AI roadmap
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if api_key and st.button("🤖 Generate AI Roadmap", use_container_width=True):
        with st.spinner("Generating personalized roadmap..."):
            roadmap = generate_roadmap(target, api_key)
        if roadmap:
            st.markdown("### 🤖 AI-Generated Personalized Roadmap")
            st.markdown(roadmap)

# ─── AI ADVISOR TAB ──────────────────────────────────────
with tab5:
    st.subheader("💬 AI Career Advisor")

    goal = st.text_input("What career goal do you have?", placeholder="e.g., Get into AI/ML, become a full-stack developer...")

    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key:
        st.warning("⚠️ Set GOOGLE_API_KEY for personalized advice")

    col_adv1, col_adv2 = st.columns([1, 1])
    with col_adv1:
        get_advice = st.button("💡 Get Career Advice", use_container_width=True)
    with col_adv2:
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.chat_history = []

    if get_advice and goal:
        if api_key:
            with st.spinner("🤖 Analyzing your profile..."):
                advice = career_advice(goal, st.session_state.profile, api_key)
            if advice:
                st.session_state.chat_history.append({
                    "user": goal,
                    "ai": advice,
                    "time": datetime.now().strftime("%H:%M")
                })
                st.rerun()
        else:
            st.error("⚠️ Set GOOGLE_API_KEY first")

    # Chat display
    if st.session_state.chat_history:
        for msg in st.session_state.chat_history:
            with st.chat_message("user"):
                st.markdown(f"**Goal:** {msg['user']}")
            with st.chat_message("assistant"):
                st.markdown(msg['ai'])
                st.caption(f"🕐 {msg['time']}")

    # Quick advice
    st.divider()
    st.markdown("### ⚡ Quick Career Tips")

    tips = [
        ("💼 Resume", "Keep it to 1 page, quantify achievements, ATS-friendly keywords"),
        ("🔍 Networking", "Connect with people at target companies, engage on LinkedIn"),
        ("📚 Portfolio", "Showcase projects on GitHub, deploy live demos"),
        ("📝 Interviews", "Practice STAR method, prepare 5 stories from experience"),
        ("🌐 Online Presence", "Optimize LinkedIn, build personal brand, share learnings"),
        ("⏰ Consistency", "30 min/day on skills > 5 hours once a week")
    ]

    cols_t = st.columns(2)
    for i, (title, tip) in enumerate(tips):
        with cols_t[i % 2]:
            st.markdown(f"**{title}:** {tip}")

st.divider()
st.caption("Built by Attanti Ramnivas | Powered by Google Gemini | Streamlit")
