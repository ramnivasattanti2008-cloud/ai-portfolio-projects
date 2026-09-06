# Deploy: 16 MEETING SUMMARIZER

## Quick Deploy to Streamlit Cloud

### 1. Go to Streamlit Cloud
Visit: https://streamlit.io/cloud

### 2. New App
- Click **"Deploy an app"**
- Repository: `ramnivasattanti2008-cloud/ai-portfolio-projects`
- Branch: `main`
- Path: `16-meeting-summarizer/`

### 3. Add Secrets
In **App Settings → Secrets**:
```
GOOGLE_API_KEY = your_gemini_api_key_here
NEWS_API_KEY = your_newsapi_key_here  # Optional
```

### 4. Deploy
Click **Deploy!**

## Local Development

```bash
cd 16-meeting-summarizer
pip install -r requirements.txt
export GOOGLE_API_KEY=your_key
streamlit run app.py
```

## Get API Keys

- **Gemini API**: https://aistudio.google.com/apikey
- **NewsAPI** (optional): https://newsapi.org/register
