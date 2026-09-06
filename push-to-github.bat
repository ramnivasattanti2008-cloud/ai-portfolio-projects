@echo off
echo ================================================
echo  PUSH ALL 6 PROJECTS TO GITHUB
echo ================================================
echo.
echo STEP 1: Install Git if not installed
echo STEP 2: Create GitHub repo (github.com/new)
echo STEP 3: Run this script
echo.
pause

cd C:\Users\Ram Nivas\Documents\portfolio-projects

echo.
echo Initializing git...
git init
git add .
git commit -m "Initial commit: 6 AI portfolio projects by Attanti Ramnivas

- smriti-ai: RAG chatbot with Gemini + ChromaDB
- Sentiment Analyzer: NLP text analysis with Plotly
- YouTube Comment Analyzer: YouTube API + sentiment analysis
- AI Email Drafter: Professional email generator
- AI Text Summarizer: Abstractive + extractive summarization
- AI Weather Insights Bot: Weather API + Gemini insights

Co-Authored-By: Claude Code <noreply@anthropic.com>"

echo.
echo ================================================
echo IMPORTANT: Create a new EMPTY repo on GitHub first
echo at: https://github.com/new
echo Name it: ai-portfolio-projects
echo Then paste the commands below:
echo ================================================
echo.
echo git remote add origin https://github.com/YOUR_USERNAME/ai-portfolio-projects.git
echo git branch -M main
echo git push -u origin main
echo.
pause
