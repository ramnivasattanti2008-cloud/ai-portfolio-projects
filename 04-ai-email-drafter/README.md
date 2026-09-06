# 📧 AI Email Drafter

> Generate professional emails in seconds with AI — 12 email types, 5 tones, 9 languages

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Gemini](https://img.shields.io/badge/Gemini-LLM-green)

## What it does

Select email type → enter context → generate professional email in any tone and language.

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| LLM | Google Gemini 2.0 Flash |
| Clipboard | Pyperclip |

## Setup

```bash
cd 04-ai-email-drafter
pip install -r requirements.txt
echo "GOOGLE_API_KEY=your_key_here" > .env
streamlit run app.py
```

## Email Types

✅ Cold Outreach | ✅ Job Application | ✅ Follow-up
✅ Networking | ✅ Complaint | ✅ Thank You
✅ Project Update | ✅ Meeting Request | ✅ Resignation
✅ Freelance Proposal | ✅ Internship Inquiry | ✅ Product Feedback

## Tones

🟢 Professional & Friendly | 🔵 Strictly Formal | 🟡 Casual & Direct
🔴 Assertive & Urgent | ⚪ Persuasive

## Languages

English | Hindi | Tamil | Telugu | Kannada | Malayalam | Marathi | Bengali | Gujarati

---

**Built by Attanti Ramnivas | AI/ML Developer**
