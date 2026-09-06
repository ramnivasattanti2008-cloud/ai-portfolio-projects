# 🌤️ AI Weather Insights Bot

> Not just weather data — intelligent weather analysis powered by AI with outfit recommendations, travel alerts, and agricultural insights

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![Gemini](https://img.shields.io/badge/Gemini-LLM-green)

## What it does

Enter a city → get current weather + AI-generated insights (what to wear, outdoor activities, travel alerts, agricultural tips).

## Tech Stack

| Layer | Technology |
|-------|------------|
| UI | Streamlit |
| Weather Data | OpenWeatherMap API |
| AI Insights | Google Gemini 2.0 Flash |
| Data | Requests |

## Setup

```bash
cd 06-weather-insights-bot
pip install -r requirements.txt
echo "OPENWEATHER_API_KEY=your_key_here" > .env
echo "GOOGLE_API_KEY=your_key_here" >> .env
streamlit run app.py
```

## Get Free API Keys

- **OpenWeather:** [openweathermap.org/api](https://openweathermap.org/api)
- **Gemini:** [aistudio.google.com](https://aistudio.google.com)

## Features

✅ Current weather (temp, humidity, wind, clouds, visibility)
✅ AI-generated insights (7 categories)
✅ Outfit recommendation based on conditions
✅ 5-day forecast
✅ Travel & commute alerts
✅ Agricultural insights
✅ Works without Gemini (basic insights fallback)

---

**Built by Attanti Ramnivas | AI/ML Developer**
