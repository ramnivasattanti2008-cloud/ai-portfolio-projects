"""
AI Weather Insights Bot — Intelligent Weather Analysis
Built by Attanti Ramnivas | AI/ML Developer

Features:
- Fetch weather data for any city
- AI-generated insights (not just raw numbers)
- Historical comparison
- Outfit recommendations
- Travel alerts
- Agricultural insights
"""

import os
import requests
import streamlit as st
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Weather Insights", page_icon="🌤️", layout="wide")
st.title("🌤️ AI Weather Insights Bot")
st.markdown("Not just weather data — intelligent weather analysis powered by AI")

# ─── CONFIG ──────────────────────────────────────────────
OPENWEATHER_API = os.getenv("OPENWEATHER_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# ─── WEATHER API ─────────────────────────────────────────
def get_weather(city):
    if not OPENWEATHER_API:
        return None, "⚠️ Set OPENWEATHER_API_KEY in .env file"

    try:
        geo_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API}&units=metric"
        geo_resp = requests.get(geo_url, timeout=10).json()

        if geo_resp.get("cod") != 200:
            return None, f"❌ City not found: {geo_resp.get('message', '')}"

        weather = geo_resp["weather"][0]
        main = geo_resp["main"]
        wind = geo_resp["wind"]
        clouds = geo_resp["clouds"]
        visibility = geo_resp.get("visibility", 10000)

        return {
            "city": geo_resp["name"],
            "country": geo_resp["sys"]["country"],
            "lat": geo_resp["coord"]["lat"],
            "lon": geo_resp["coord"]["lon"],
            "temp": round(main["temp"], 1),
            "feels_like": round(main["feels_like"], 1),
            "humidity": main["humidity"],
            "pressure": main["pressure"],
            "wind_speed": wind["speed"],
            "wind_deg": wind.get("deg", 0),
            "clouds": clouds["all"],
            "visibility": visibility,
            "condition": weather["main"],
            "description": weather["description"].title(),
            "icon": weather["icon"],
            "sunrise": geo_resp["sys"]["sunrise"],
            "sunset": geo_resp["sys"]["sunset"],
            "timezone": geo_resp["timezone"],
            "dt": geo_resp["dt"]
        }, None

    except Exception as e:
        return None, f"❌ Error: {str(e)}"

def get_forecast(city):
    """Get 5-day forecast"""
    if not OPENWEATHER_API:
        return None
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API}&units=metric"
        resp = requests.get(url, timeout=10).json()
        if resp.get("cod") != "200":
            return None
        return resp["list"]
    except:
        return None

# ─── AI INSIGHTS ─────────────────────────────────────────
def generate_ai_insight(weather_data, forecast_data, api_key):
    if not api_key:
        return get_basic_insights(weather_data)

    try:
        from google.generativeai import GenerativeModel
        model = GenerativeModel("gemini-2.0-flash")

        prompt = f"""You are a friendly AI weather analyst. Give practical, useful insights for someone in this location.

CURRENT WEATHER:
- City: {weather_data['city']}, {weather_data['country']}
- Temperature: {weather_data['temp']}°C (feels like {weather_data['feels_like']}°C)
- Condition: {weather_data['description']}
- Humidity: {weather_data['humidity']}%
- Wind: {weather_data['wind_speed']} m/s
- Cloud cover: {weather_data['clouds']}%

Give insights on:
1. 🧥 What to wear today
2. 🏃 Outdoor activity recommendation
3. 🌧️ Rain/umbrella advice
4. 💧 Hydration/health tip
5. ☀️ UV/sun protection
6. 🚗 Traffic/commute impact
7. 🌾 Agriculture/farming tip (if relevant)

Keep it practical, friendly, and use emojis. 5-7 bullet points max."""

        response = model.generate_content(prompt)
        return response.text
    except:
        return get_basic_insights(weather_data)

def get_basic_insights(weather):
    """Fallback when no AI API"""
    temp = weather["temp"]
    humidity = weather["humidity"]
    wind = weather["wind_speed"]
    condition = weather["condition"]

    insights = []

    # Clothing
    if temp < 15:
        insights.append("🧥 Wear warm layers — it's chilly!")
    elif temp < 25:
        insights.append("👕 Light comfortable clothing — pleasant weather!")
    else:
        insights.append("🩳 Wear light, breathable clothes — it's hot!")

    # Rain
    if condition in ["Rain", "Drizzle", "Thunderstorm"]:
        insights.append("☔ Carry an umbrella — rain expected!")
    else:
        insights.append("☀️ No rain expected — enjoy outdoor plans!")

    # Wind
    if wind > 8:
        insights.append("💨 Strong winds — secure loose items!")
    elif wind > 5:
        insights.append("🌬️ Moderate breeze — comfortable!")

    # Humidity
    if humidity > 80:
        insights.append("💧 High humidity — stay hydrated!")
    elif humidity < 30:
        insights.append("🏜️ Low humidity — dry skin possible!")

    # UV/Health
    if weather["clouds"] < 30:
        insights.append("🧴 High UV — apply sunscreen!")
    if temp > 35:
        insights.append("⚠️ Heat alert — avoid prolonged sun exposure!")
    if temp < 10:
        insights.append("❄️ Cold alert — bundle up warmly!")

    return "\n".join(f"• {i}" for i in insights)

def get_outfit_recommendation(weather):
    temp = weather["temp"]
    condition = weather["condition"]

    if temp < 10:
        return "🧥 Heavy jacket, scarf, gloves, boots"
    elif temp < 18:
        return "🧥 Light jacket or sweater, jeans, closed shoes"
    elif temp < 25:
        return "👕 T-shirt, light pants, comfortable shoes"
    elif temp < 32:
        return "🩳 Shorts, breathable shirt, sandals"
    else:
        return "🩱 Minimal, loose, light-colored clothing — stay cool!"

# ─── UI ──────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ API Keys")
    ow_key = st.text_input("OpenWeather API", type="password",
                           value=OPENWEATHER_API if OPENWEATHER_API else "",
                           help="Get free: openweathermap.org/api")
    gemini_key = st.text_input("Google Gemini API", type="password",
                               value=GOOGLE_API_KEY if GOOGLE_API_KEY else "",
                               help="Get free: aistudio.google.com")

    if ow_key:
        os.environ["OPENWEATHER_API_KEY"] = ow_key
    if gemini_key:
        os.environ["GOOGLE_API_KEY"] = gemini_key

    st.markdown("---")
    st.markdown("**Free API Keys:**")
    st.markdown("[OpenWeather](https://openweathermap.org/api)")
    st.markdown("[Google AI Studio](https://aistudio.google.com)")

# Main input
city = st.text_input(
    "🌍 Enter city name:",
    placeholder="e.g., Bengaluru, Mumbai, Delhi..."
)

if city:
    weather, error = get_weather(city)

    if error:
        st.error(error)
    else:
        # Current weather cards
        st.subheader(f"🌤️ {weather['city']}, {weather['country']} — Now")

        col_w1, col_w2, col_w3, col_w4 = st.columns(4)
        with col_w1:
            st.metric("🌡️ Temperature", f"{weather['temp']}°C",
                     delta=f"Feels like {weather['feels_like']}°C")
        with col_w2:
            st.metric("💧 Humidity", f"{weather['humidity']}%",
                     delta="High" if weather["humidity"] > 70 else "Low" if weather["humidity"] < 40 else "Normal")
        with col_w3:
            st.metric("💨 Wind", f"{weather['wind_speed']} m/s",
                     delta=f"Direction: {weather['wind_deg']}°")
        with col_w4:
            st.metric("☁️ Clouds", f"{weather['clouds']}%",
                     delta="Clear" if weather["clouds"] < 30 else "Cloudy")

        st.markdown(f"**{weather['description']}** | Feels like {weather['feels_like']}°C")

        # AI Insights
        st.divider()
        st.subheader("🧠 AI Weather Insights")

        forecast = get_forecast(city)
        insight = generate_ai_insight(weather, forecast, os.getenv("GOOGLE_API_KEY"))
        st.markdown(insight)

        # Outfit recommendation
        outfit = get_outfit_recommendation(weather)
        st.info(f"👔 Recommended outfit: {outfit}")

        # Forecast
        if forecast:
            st.divider()
            st.subheader("📅 5-Day Forecast")

            daily = {}
            for entry in forecast:
                dt = datetime.fromtimestamp(entry["dt"])
                day = dt.strftime("%a %b %d")
                if day not in daily:
                    daily[day] = {
                        "temp": entry["main"]["temp"],
                        "condition": entry["weather"][0]["main"],
                        "desc": entry["weather"][0]["description"],
                        "humidity": entry["main"]["humidity"],
                        "count": 1
                    }
                else:
                    daily[day]["temp"] = (daily[day]["temp"] + entry["main"]["temp"]) / 2
                    daily[day]["count"] += 1

            cols = st.columns(len(daily))
            for i, (day, data) in enumerate(daily.items()):
                with cols[i]:
                    st.markdown(f"**{day}**")
                    st.markdown(f"{data['condition']}")
                    st.markdown(f"🌡️ {data['temp']:.0f}°C")
                    st.markdown(f"💧 {data['humidity']}%")

        # Travel alert
        st.divider()
        st.subheader("🚗 Travel & Commute Alert")

        alerts = []
        if weather["wind_speed"] > 10:
            alerts.append("⚠️ Strong winds — drive carefully!")
        if weather["visibility"] < 5000:
            alerts.append("🌫️ Low visibility — slow down!")
        if weather["condition"] in ["Rain", "Thunderstorm"]:
            alerts.append("🌧️ Wet roads likely — allow extra travel time!")
        if weather["temp"] > 38:
            alerts.append("🔥 Extreme heat — avoid midday travel!")
        if weather["temp"] < 5:
            alerts.append("❄️ Freezing conditions — check vehicle coolant!")

        if alerts:
            for a in alerts:
                st.warning(a)
        else:
            st.success("✅ No weather alerts — conditions look good!")

st.caption("Built by Attanti Ramnivas | Powered by OpenWeather + Gemini | Streamlit")
