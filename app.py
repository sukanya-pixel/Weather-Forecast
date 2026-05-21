import streamlit as st
import requests
import datetime
import matplotlib.pyplot as plt
import base64
import os
import io
import time
from dotenv import load_dotenv
import matplotlib.ticker as ticker

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- CSS (MAIN MAGIC) ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"], [class*="st-"], .stApp, .stApp * {
    font-family: 'Outfit', sans-serif !important;
}
html, body {
    overflow: hidden !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}
body {
    background-color: #012A4A;
}

.stApp {
    background-color: #012A4A;
    overflow: hidden !important;
    height: 100vh !important;
}

[data-testid="stAppViewContainer"], [data-testid="stMain"], .block-container {
    overflow: hidden !important;
}

/* HIDE SCROLLBARS GLOBALLY */
::-webkit-scrollbar {
    display: none !important;
}
* {
    -ms-overflow-style: none !important;  /* IE and Edge */
    scrollbar-width: none !important;  /* Firefox */
}

/* REMOVE STREAMLIT TOP BAR SPACE */
[data-testid="stHeader"] {
    display: none;
}

[data-testid="stToolbar"] {
    right: 1rem;
}

.block-container {
    padding-top: 0rem !important;
    margin-top: -35px !important;
}
/* HEADER */
.header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    font-size:22px;
    font-weight:600;
    margin-bottom:10px;
}

/* INFO BAR */
.info-box {
    background:#e8f0ff;
    padding:12px;
    border-radius:10px;
    margin-bottom:10px;
}

/* CARD STYLE */
.card {
    background:white;
    padding:20px;
    border-radius:25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/* SMALL CARD */
.small-card {
    background:white;
    padding:15px;
    border-radius:12px;
    text-align:center;
    box-shadow: 0 3px 8px rgba(0,0,0,0.08);
}

/* ALERT */
.alert {
    background:#fff4e5;
    padding:15px;
    border-radius:10px;
    color:#a85b00;
    font-weight:500;
}

/* --- WEATHER MAIN CARD --- */
.weather-main-card {
    background: #89C2D9;
    padding: 25px 40px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    height: 230px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
}
.weather-main-top {
    display: flex;
    justify-content: space-between;
}
.weather-temp {
    font-size: 50px;
    font-weight: bold;
    line-height: 1.1;
    color: #012A4A;
}
.weather-temp-unit {
    font-size: 20px;
}
.weather-highlow {
    font-size: 16px;
    margin-top: 1px;
    color: #012A4A;
    font-weight: 600;
}
.weather-desc {
    font-size: 18px;
    margin-top: 1px;
    color: #014F86;
}
.weather-icon {
    width: 120px;
    margin-top: -5px;
}
.weather-metrics-row {
    display: flex;
    gap: 8px;
    margin-top: 10px;
}
.weather-metric-box {
    flex: 1;
    background: #014F86;
    border-radius: 8px;
    padding: 6px 4px;
    text-align: center;
    height: 62px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-sizing: border-box;
}
.metric-label {
    font-size: 14px;
    color: #A9D6E5;
    white-space: nowrap;
}
.metric-value {
    font-size: 15px;
    color: white;
    font-weight: 800;
}

/* --- WIND CARD --- */
.wind-card {
    background: #89C2D9;
    padding: 25px 40px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    height: 230px;
    display: flex;
    flex-direction: column;
    box-sizing: border-box;
}
.wind-card .card-title {
    font-weight: 600;
    font-size: 18px;
    margin-bottom: 10px;
    color: #014F86;
    display: flex;
    align-items: center;
    gap: 8px;
}
.wind-card .card-title img {
    width: 30px;
}
.wind-speed {
    font-size: 34px;
    margin-top: 10px;
    font-weight: bold;
    color: #012A4A;
    line-height: 1;
}
.wind-unit {
    font-size: 18px;
    font-weight: 500;
}
.wind-label {
    font-size: 16px;
    margin-top: 20px;
    margin-bottom: 4px;
    color: #014F86;
}
.wind-bar-container {
    width: 100%;
    margin-top: 5px;
    background-color: #e9ecef;
    border-radius: 4px;
    height: 10px;
    margin-bottom: 6px;
}
.wind-bar-fill {
    background-color: #01497C;
    height: 10px;
    border-radius: 4px;
}
.wind-pct {
    font-size: 16px;
    margin-top: 5px;
    font-weight: 600;
    color: #012A4A;
}

/* --- SUN CARD --- */
.sun-card {
    background: #89C2D9;
    padding: 25px 40px;
    border-radius: 16px;
    height: 230px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-sizing: border-box;
}
.sun-row {
    display: flex;
    flex-direction: column;
}
.sun-title {
    font-size: 18px;
    margin-bottom: 4px;
    font-weight: 500;
    color: #014F86;
    display: flex;
    align-items: center;
    gap: 8px;
}
.sun-title img {
    width: 30px;
}
.sun-time {
    font-size: 26px;
    font-weight: bold;
    padding-left: 38px;
    color: #012A4A;
}
.sun-divider {
    margin: 10px 0;
    border: none;
    border-top: 1px solid #eee;
}

/* --- TREND CARD --- */
.trend-card {
    background: #89C2D9;
    margin-top: 15px;
    padding: 20px;
    border-radius: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    box-sizing: border-box;
}
.trend-chart-img {
    width: 100%;
    height: 220px;
}

/* --- 7-DAY FORECAST CARD --- */
.forecast-card {
    flex: 1;
    height: 130px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: #89c2d9;
    padding: 8px 5px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    box-sizing: border-box;
}
.forecast-date {
    font-size: 14px;
    color: #01497C;
    font-weight: 600;
}
.forecast-icon-container img {
    width: 30px;
}
.forecast-temp {
    font-weight: bold;
    color: #012A4A;
    font-size: 18px;
}
.forecast-desc {
    font-size: 14px;
    color: #014F86;
    font-weight: 500;
}

/* --- ADDITIONAL DETAILS CARD --- */
.additional-details-card {
    background: #89C2D9;
    border-radius: 15px;
    padding: 10px 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-sizing: border-box;
}
.details-list {
    display: flex;
    gap: 10px;
    align-items: center;
}
.details-item {
    display: flex;
    align-items: center;
    gap: 6px;
}
.details-text {
    font-size: 16px;
    color: #333;
    white-space: nowrap;
}
.details-divider {
    border-left: 1px solid #eef2f6;
    height: 30px;
}

/* --- MOBILE RESPONSIVE MEDIA QUERY --- */
@media (max-width: 768px) {
    /* 1. Global scroll and height behavior */
    html, body {
        overflow-y: auto !important;
        overflow-x: hidden !important;
        height: auto !important;
    }
    
    .stApp {
        overflow-y: auto !important;
        overflow-x: hidden !important;
        height: auto !important;
    }

    [data-testid="stAppViewContainer"], [data-testid="stMain"], .block-container {
        overflow-y: auto !important;
        overflow-x: hidden !important;
        height: auto !important;
    }
    
    .block-container {
        margin-top: 0px !important;
        padding-top: 15px !important;
        padding-bottom: 30px !important;
    }
    
    /* 2. Layout columns stack */
    div[data-testid="stHorizontalBlock"] {
        flex-direction: column !important;
        gap: 15px !important;
    }
    
    /* EXCEPT header bar which must remain a row */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) {
        flex-direction: row !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 10px !important;
    }
    
    /* Columns take full width */
    div[data-testid="column"], div[data-testid="stColumn"] {
        width: 100% !important;
        min-width: 100% !important;
    }
    
    /* Header columns do not wrap and stay inline */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) div[data-testid="column"],
    div[data-testid="stHorizontalBlock"]:has(.header-marker) div[data-testid="stColumn"] {
        width: auto !important;
        min-width: 0 !important;
    }
    
    /* 3. Weather Main Card adjustments */
    .weather-main-card {
        padding: 15px 20px !important;
        height: auto !important;
        gap: 15px !important;
    }
    .weather-main-top {
        align-items: center !important;
    }
    .weather-temp {
        font-size: 40px !important;
    }
    .weather-icon {
        width: 90px !important;
    }
    .weather-metrics-row {
        gap: 6px !important;
    }
    .weather-metric-box {
        height: 55px !important;
        padding: 4px 2px !important;
    }
    .metric-label {
        font-size: 11px !important;
    }
    .metric-value {
        font-size: 12px !important;
    }
    
    /* 4. Wind Card adjustments */
    .wind-card {
        padding: 15px 20px !important;
        height: auto !important;
        gap: 5px !important;
    }
    .wind-speed {
        font-size: 28px !important;
    }
    .wind-label {
        margin-top: 10px !important;
    }
    
    /* 5. Sun Card adjustments */
    .sun-card {
        padding: 15px 20px !important;
        height: auto !important;
        gap: 10px !important;
    }
    .sun-time {
        font-size: 22px !important;
        padding-left: 38px !important;
    }
    .sun-divider {
        margin: 5px 0 !important;
    }
    
    /* 6. Trend Card adjustments */
    .trend-card {
        padding: 15px !important;
        margin-top: 10px !important;
    }
    .trend-chart-img {
        height: auto !important;
        max-height: 200px !important;
        object-fit: contain !important;
    }
    
    /* 7. Forecast container and cards adjustments (swipeable container!) */
    .forecast-container {
        display: flex !important;
        overflow-x: auto !important;
        justify-content: flex-start !important;
        gap: 10px !important;
        padding-bottom: 10px !important;
        margin-top: 10px !important;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none !important; /* Hide scrollbars */
    }
    .forecast-container::-webkit-scrollbar {
        display: none !important; /* Hide scrollbar for Safari/Chrome */
    }
    .forecast-card {
        min-width: 85px !important;
        max-width: 95px !important;
        flex: 0 0 auto !important;
        height: 120px !important;
        padding: 6px 3px !important;
    }
    .forecast-date {
        font-size: 12px !important;
    }
    .forecast-icon-container img {
        width: 25px !important;
    }
    .forecast-temp {
        font-size: 15px !important;
    }
    .forecast-desc {
        font-size: 12px !important;
    }
    
    /* 8. Additional Details adjustments */
    .additional-details-card {
        flex-direction: column !important;
        align-items: stretch !important;
        padding: 15px !important;
        margin-top: 10px !important;
    }
    .details-list {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 12px !important;
        width: 100% !important;
    }
    .details-divider {
        display: none !important; /* Hide visual vertical dividers on vertical stack */
    }
    .details-item {
        width: 100% !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        border-bottom: 1px solid rgba(1, 42, 74, 0.15);
        padding-bottom: 8px;
    }
    .details-item:last-child {
        border-bottom: none !important;
        padding-bottom: 0 !important;
    }
    .details-text {
        font-size: 15px !important;
    }
    .warm-alert-box {
        width: 100% !important;
        margin-top: 10px !important;
    }
    .warm-alert-hidden {
        display: none !important;
    }
    
    /* 9. Header Search Bar Adjustments on Mobile */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) div[data-testid="stElementContainer"]:has(input) {
        width: 160px !important; /* Slightly smaller width on mobile to avoid layout clipping */
    }
    
    /* 10. Scale title size on mobile */
    .app-title {
        margin-top: 5px !important;
        margin-bottom: 5px !important;
    }
    .app-title div {
        font-size: 38px !important;
    }
    .app-title img {
        width: 35px !important;
    }
}

</style>
""", unsafe_allow_html=True)

# ---------------- API ----------------
load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_base64_image(*paths):
    image_path = os.path.join(BASE_DIR, *paths)

    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

search_icon = get_base64_image("Data", "search.png")
gps_icon = get_base64_image("Data", "gps.png")
wind_icon = get_base64_image("Data", "wind.png")
sunrise_icon = get_base64_image("Data", "sunrise.png")
sunset_icon = get_base64_image("Data","sunset.png")
bar_graph_icon = get_base64_image("Data","bar-graph.png")
calendar_icon = get_base64_image("Data","calendar.png")
clouds_icon = get_base64_image("Data","clouds.png")
earth_icon = get_base64_image("Data","earth.png")
temperature_icon_new = get_base64_image("Data","temperature.png")
cloud_icon_new = get_base64_image("Data","Cloud.png")

def get_condition_image_base64(icon_code):
    mapping = {
        '01d': 'sunny.png',
        '01n': 'clear night.png',
        '02d': 'partly-cloudy.png',
        '02n': 'partly-cloudy.png',
        '03d': 'cloudy.png',
        '03n': 'cloudy.png',
        '04d': 'cloudy.png',
        '04n': 'cloudy.png',
        '09d': 'light-rain.png',
        '09n': 'light-rain.png',
        '10d': 'light-rain.png',
        '10n': 'light-rain.png',
        '11d': 'thunderstorm.png',
        '11n': 'thunderstorm.png',
        '13d': 'snowflake.png',
        '13n': 'snowflake.png',
        '50d': 'fog.png',
        '50n': 'fog.png'
    }
    filename = mapping.get(icon_code, 'sunny.png')
    try:
        return get_base64_image("Data","condition",filename)
    except:
        return ""

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_aqi(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    try:
        res = requests.get(url).json()
        pm25 = res['list'][0]['components']['pm2_5']
        
        if pm25 <= 12.0:
            return int(round(((50 - 0) / (12.0 - 0)) * (pm25 - 0) + 0))
        elif pm25 <= 35.4:
            return int(round(((100 - 51) / (35.4 - 12.1)) * (pm25 - 12.1) + 51))
        elif pm25 <= 55.4:
            return int(round(((150 - 101) / (55.4 - 35.5)) * (pm25 - 35.5) + 101))
        elif pm25 <= 150.4:
            return int(round(((200 - 151) / (150.4 - 55.5)) * (pm25 - 55.5) + 151))
        elif pm25 <= 250.4:
            return int(round(((300 - 201) / (250.4 - 150.5)) * (pm25 - 150.5) + 201))
        elif pm25 <= 350.4:
            return int(round(((400 - 301) / (350.4 - 250.5)) * (pm25 - 250.5) + 301))
        else:
            return int(round(((500 - 401) / (500.4 - 350.5)) * (pm25 - 350.5) + 401))
    except:
        return None

# ---------------- STATE ----------------
if "city" not in st.session_state:
    st.session_state.city = "Bhubaneswar"

if "last_valid_city" not in st.session_state:
    st.session_state.last_valid_city = "Bhubaneswar"

if "search" not in st.session_state:
    st.session_state.search = False

# ---------------- HEADER & CARD CSS FIXES ----------------
st.markdown("""
<style>

/* HEADER ROW CONTAINER (NO CARD) */
div[data-testid="stHorizontalBlock"]:has(.header-marker) {
    background: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin-top: 10px;
    margin-bottom: 10px;
    align-items: center !important;
    width: 100% !important;
}

/* REMOVE COLUMN PADDING (important) */
div[data-testid="column"] {
    padding: 0 !important;
}

/* Style search text input globally (completely empty background) */
div[data-testid="stTextInput"] {
    margin-top: 10px !important;
}
div[data-testid="stTextInput"],
div[data-testid="stTextInput"] div,
div[data-testid="stTextInput"] input {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    font-family: 'Outfit', sans-serif !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: rgba(255, 255, 255, 0.6) !important;
    -webkit-text-fill-color: rgba(255, 255, 255, 0.6) !important;
}

/* autofill styling to prevent browser white background */
div[data-testid="stTextInput"] input:-webkit-autofill,
div[data-testid="stTextInput"] input:-webkit-autofill:hover, 
div[data-testid="stTextInput"] input:-webkit-autofill:focus, 
div[data-testid="stTextInput"] input:-webkit-autofill:active {
    -webkit-box-shadow: 0 0 0 1000px #012A4A inset !important;
    -webkit-text-fill-color: white !important;
    transition: background-color 5000s ease-in-out 0s;
}

/* DYNAMIC CARD HOVER EFFECT */
.dynamic-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease !important;
}
.dynamic-card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2) !important;
}

/* HEADER ROW CONTAINER (NO CARD) */
div[data-testid="stHorizontalBlock"]:has(.header-marker) {
    background: transparent !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin-top: 0px !important;
    margin-bottom: 15px;
    align-items: center !important;
    width: 100% !important;
    position: relative !important;
}

/* APP TITLE CONTAINER CSS */
div[data-testid="stElementContainer"]:has(.app-title) {
    margin-bottom: -10px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- APP TITLE ----------------
st.markdown(f"""
<div class="app-title" style="
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;
    margin-top: 10px;
    margin-bottom: -5px;
">
    <img src="data:image/png;base64,{clouds_icon}" width="50" style="filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.15));">
    <div style="
        font-size:58px;
        font-weight:800;
        color:White;
        letter-spacing:1.5px;
        font-family:'Outfit', sans-serif;
    ">
        SkyFlow
    </div>
</div>
""", unsafe_allow_html=True)

# HEADER BLOCK

# Define search submit function first
def submit_search():
    new_city = st.session_state.search_input.strip()
    if new_city:
        st.session_state.city = new_city
        st.session_state.search = False  # Collapse back to icon after search
        if 'weather_cache' in st.session_state:
            del st.session_state.weather_cache

if not st.session_state.search:
    col1, col2 = st.columns([15, 1])
else:
    col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"""
    <div class="header-marker" style="
        display:flex;
        align-items:center;
        gap:8px;
        font-size:22px;
        font-weight:600;
        color:white;
        margin:0;
        padding:0;
        line-height:1;
        white-space: nowrap;
    ">
        <img src="data:image/png;base64,{gps_icon}" width="35" style="margin:0; padding:0; display:block;">
        <span style="margin:0; padding:0; line-height:1; display:flex; align-items:center; height:26px;">{st.session_state.city.title()}</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if not st.session_state.search:
        st.markdown(f"""
        <style>
        /* Target the element container for the button and text input */
        div[data-testid="stVerticalBlock"] > div:has(button),
        div[data-testid="stElementContainer"]:has(button) {{
            display: flex;
            justify-content: flex-end;
            width: 100%;
        }}
        
        button[kind="secondary"] {{
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            width: 32px !important;
            height: 32px !important;
            min-width: 0 !important;
            padding: 0 !important;
            position: absolute !important;
            right: 0 !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
        }}
        button[kind="secondary"]::after {{
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url("data:image/png;base64,{search_icon}");
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center;
        }}
        button[kind="secondary"] p {{
            display: none !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        if st.button("Search", key="toggle_search_on"):
            st.session_state.search = True
            st.rerun()
    else:
        st.markdown(f"""
        <style>
        /* Absolute position the active search input container to flush right */
        div[data-testid="stHorizontalBlock"]:has(.header-marker) div[data-testid="stElementContainer"]:has(input) {{
            position: absolute !important;
            right: 0 !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
            width: 280px !important;
            z-index: 100;
        }}
        /* Ensure the inner Streamlit wrappers stretch fully and have no padding */
        div[data-testid="stHorizontalBlock"]:has(.header-marker) div[data-testid="stElementContainer"]:has(input) div {{
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: visible !important;
        }}
        /* Style the baseweb wrapper to create the invisible box */
        div[data-testid="stHorizontalBlock"]:has(.header-marker) div[data-baseweb="input"] {{
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            height: 32px !important;
            min-height: 32px !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }}
        /* Style the input text */
        div[data-testid="stHorizontalBlock"]:has(.header-marker) input {{
            color: white !important;
            padding: 0 15px !important;
            background: transparent !important;
            border: none !important;
            height: 32px !important;
            width: 100% !important;
        }}
        /* Hide labels and instructions to prevent extra layout padding */
        div[data-testid="stHorizontalBlock"]:has(.header-marker) label,
        div[data-testid="stHorizontalBlock"]:has(.header-marker) div[data-testid="InputInstructions"] {{
            display: none !important;
            margin: 0 !important;
            height: 0 !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        st.text_input("Search City", placeholder="Search here...", key="search_input", on_change=submit_search, label_visibility="collapsed")
        
        # Hide the close button container using CSS
        st.markdown("""
        <style>
        div[data-testid="stHorizontalBlock"]:has(.header-marker) div[data-testid="stElementContainer"]:has(button) {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        if st.button("close_search_btn", key="close_search_btn"):
            st.session_state.search = False
            st.rerun()

        # Injected script via st.html to close on click outside
        st.html("""
<script>
setTimeout(() => {
    function handleClickOutside(e) {
        const searchContainer = document.querySelector('div[data-testid="stTextInput"]');
        if (!searchContainer) {
            document.removeEventListener('click', handleClickOutside);
            delete window.__handleClickOutside;
            return;
        }
        // If click is outside the search container
        if (!searchContainer.contains(e.target)) {
            const closeButton = Array.from(document.querySelectorAll('button')).find(btn => btn.textContent.includes('close_search_btn'));
            if (closeButton) {
                closeButton.click();
            }
            document.removeEventListener('click', handleClickOutside);
            delete window.__handleClickOutside;
        }
    }
    
    if (window.__handleClickOutside) {
        document.removeEventListener('click', window.__handleClickOutside);
    }
    window.__handleClickOutside = handleClickOutside;
    document.addEventListener('click', handleClickOutside);
}, 200);
</script>
""", unsafe_allow_javascript=True)


city = st.session_state.city

# ---------------- FETCH ----------------
import time

cache_valid = False
if 'weather_cache' in st.session_state and st.session_state.get('weather_cache_city') == city:
    # Check if cache is older than 10 minutes (600 seconds)
    if time.time() - st.session_state.get('weather_cache_time', 0) < 600:
        cache_valid = True

if not cache_valid:
    try:
        data = get_weather(city)
        if str(data.get("cod")) != "200":
            msg = data.get("message", "City not found").capitalize()
            st.error(f"🔍 {msg}: '{city.title()}' not found. Please try another city.")
            # Revert to last valid city so the user is not stuck on an invalid city
            st.session_state.city = st.session_state.last_valid_city
            st.stop()

        forecast = get_forecast(city)
        if str(forecast.get("cod")) != "200":
            msg = forecast.get("message", "Error fetching forecast data").capitalize()
            st.error(f"❌ Forecast Error: {msg}")
            st.session_state.city = st.session_state.last_valid_city
            st.stop()

        lat = data['coord']['lat']
        lon = data['coord']['lon']
        aqi_val = get_aqi(lat, lon)
        
        st.session_state.weather_cache = {
            'data': data,
            'forecast': forecast,
            'aqi_val': aqi_val
        }
        st.session_state.weather_cache_city = city
        st.session_state.weather_cache_time = time.time()
        st.session_state.last_valid_city = city  # Update last valid city on successful fetch
    except requests.exceptions.RequestException as e:
        st.error("🔌 Network Connection Error: Unable to connect to the weather service. Please check your internet connection.")
        st.stop()
    except (KeyError, TypeError, IndexError) as e:
        st.error("❌ Data Error: The weather service returned unexpected or incomplete data format. Please try again later.")
        st.stop()
else:
    data = st.session_state.weather_cache['data']
    forecast = st.session_state.weather_cache['forecast']
    aqi_val = st.session_state.weather_cache['aqi_val']

# ---------------- MAIN CARDS ----------------
col1, col2, col3 = st.columns([1.3, 1, 1], gap="large")

# WEATHER CARD
with col1:
    icon = data['weather'][0]['icon']
    icon_b64 = get_condition_image_base64(icon)
    desc = data['weather'][0]['description'].title()
    temp = int(data['main']['temp'])
    forecast_temps = [item['main']['temp'] for item in forecast['list'][:8]]
    temp_min = int(min(forecast_temps + [data['main']['temp']]))
    temp_max = int(max(forecast_temps + [data['main']['temp']]))
    pressure = data['main']['pressure']
    visibility = data['visibility'] // 1000
    humidity = data['main']['humidity']
    precip_prob = int(forecast['list'][0].get('pop', 0) * 100)
    st.markdown(f"""
    <div class="dynamic-card weather-main-card">
        <div class="weather-main-top">
            <div class="weather-main-left">
                <div class="weather-temp">{temp}°<span class="weather-temp-unit">C</span></div>
                <div class="weather-highlow"><span style="color: #0d6efd;">▲</span> High: {temp_max}° &nbsp; <span style="color: #0d6efd;">▼</span> Low: {temp_min}°</div>
                <div class="weather-desc">{desc}</div>
            </div>
            <div class="weather-main-right">
                <img class="weather-icon" src="data:image/png;base64,{icon_b64}">
            </div>
        </div>
        <div class="weather-metrics-row">
            <div class="dynamic-card weather-metric-box">
                <div class="metric-label">Pressure</div>
                <div class="metric-value">{pressure} mb</div>
            </div>
            <div class="dynamic-card weather-metric-box">
                <div class="metric-label">Visibility</div>
                <div class="metric-value">{visibility} km</div>
            </div>
            <div class="dynamic-card weather-metric-box">
                <div class="metric-label">Humidity</div>
                <div class="metric-value">{humidity}%</div>
            </div>
            <div class="dynamic-card weather-metric-box">
                <div class="metric-label">Precipitation</div>
                <div class="metric-value">{precip_prob}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
 
# WIND CARD
with col2:
    speed = data['wind']['speed']
    pct = min(int(speed * 10), 100)
    st.markdown(f"""
    <div class="dynamic-card wind-card">
        <div class="card-title"><img src="data:image/png;base64,{wind_icon}"> Wind Info</div>
        <div class="wind-speed">{speed} <span class="wind-unit">m/s</span></div>
        <div class="wind-label">Wind Speed</div>
        <div class="wind-bar-container">
            <div class="wind-bar-fill" style="width: {pct}%;"></div>
        </div>
        <div class="wind-pct">{pct}%</div>
    </div>
    """, unsafe_allow_html=True)
 
# SUN CARD
with col3:
    sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
     
    st.markdown(f"""
    <div class="dynamic-card sun-card">
        <div class="sun-row">
            <div class="sun-title"><img src="data:image/png;base64,{sunrise_icon}"> Sunrise:</div>
            <div class="sun-time">{sunrise}</div>
        </div>
        <hr class="sun-divider">
        <div class="sun-row">
            <div class="sun-title"><img src="data:image/png;base64,{sunset_icon}"> Sunset:</div>
            <div class="sun-time">{sunset}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- GRAPH & FORECAST ROW ----------------
st.markdown("<div style='height:5px;'></div>", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    st.markdown(f"<div style='display:flex; align-items:center; gap:8px; font-weight: 600; font-size: 20px; color: White; margin-bottom: 10px;'><img src='data:image/png;base64,{bar_graph_icon}' width='30' height='30'><span>Temperature Trend (Next 24 Hours)</span></div>", unsafe_allow_html=True)
    
    tz_offset = datetime.timedelta(seconds=data['timezone'])
    
    # Collect raw points (timestamp, temp)
    raw_points = [(data['dt'], data['main']['temp'])]
    for item in forecast['list']:
        if item['dt'] > data['dt']:
            raw_points.append((item['dt'], item['main']['temp']))
            if len(raw_points) >= 8:
                break
                
    # Linearly interpolate a point in between each consecutive pair
    interpolated_points = []
    for i in range(len(raw_points)):
        interpolated_points.append(raw_points[i])
        if i < len(raw_points) - 1:
            dt1, temp1 = raw_points[i]
            dt2, temp2 = raw_points[i+1]
            mid_dt = (dt1 + dt2) / 2
            mid_temp = (temp1 + temp2) / 2
            interpolated_points.append((mid_dt, mid_temp))
            
    temps = []
    tick_positions = []
    tick_labels = []
    
    for idx, (dt, temp) in enumerate(interpolated_points):
        temps.append(temp)
        if idx % 2 == 0:
            time_local = datetime.datetime.fromtimestamp(dt, datetime.timezone.utc) + tz_offset
            tick_labels.append(time_local.strftime('%H:%M'))
            tick_positions.append(idx)
        
    fig, ax = plt.subplots(figsize=(8,4.3))
    ax.plot(range(len(temps)), temps, marker='o', color='#0d6efd', linewidth=2)
    ax.margins(x=0.05, y=0.15)
    ax.set_facecolor('#89C2D9')
    fig.patch.set_facecolor('#89C2D9')
    ax.grid(axis='y', linestyle='-', alpha=0.3)
    ax.grid(axis='x', linestyle='-', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#89C2D9')
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, fontsize=14, color='#012A4A')
    ax.tick_params(axis='x', length=0, pad=2, colors='#012A4A', labelsize=14)
    ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=6))
    plt.yticks(fontsize=14, color='#012A4A')
    ax.tick_params(axis='y', length=0, pad=3, colors='#012A4A', labelsize=14)
    ax.set_ylabel('°C', color='#012A4A', fontsize=16, rotation=0, labelpad=15)
    fig.tight_layout(pad=1.5)
    
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight', facecolor=fig.get_facecolor())
    img_b64 = base64.b64encode(buf.getvalue()).decode()
    st.markdown(f"""
    <div class="dynamic-card trend-card">
        <img src="data:image/png;base64,{img_b64}" class="trend-chart-img">
    </div>
    """, unsafe_allow_html=True)

with col_right:
    st.markdown(f"<div style='display:flex; align-items:center; gap:8px; font-weight: 600; font-size: 20px; color: White; margin-bottom: 10px;'><img src='data:image/png;base64,{calendar_icon}' width='30' height='30'><span>7-Day Forecast</span></div>", unsafe_allow_html=True)
    
    html_boxes = "<div class='forecast-container' style='display:flex; gap:8px; justify-content:space-between;'>"
    num_days_available = len(forecast['list']) // 8
    for i in range(7):
        if i < num_days_available:
            d = forecast['list'][i*8]
            dt_obj = datetime.datetime.strptime(d['dt_txt'], '%Y-%m-%d %H:%M:%S')
            temp = int(d['main']['temp'])
            desc = d['weather'][0]['main']
            icon = d['weather'][0]['icon']
        else:
            # Extrapolate for Day 6 and Day 7
            d = forecast['list'][(num_days_available - 1) * 8]
            base_dt = datetime.datetime.strptime(d['dt_txt'], '%Y-%m-%d %H:%M:%S')
            dt_obj = base_dt + datetime.timedelta(days=i - (num_days_available - 1))
            temp = int(d['main']['temp'] + (1 if i == 5 else -1))
            desc = d['weather'][0]['main']
            icon = d['weather'][0]['icon']
            
        date_str = dt_obj.strftime('%d %b')
        icon_b64 = get_condition_image_base64(icon)
        html_boxes += f"""<div class="dynamic-card forecast-card">
                        <div class="forecast-date">{date_str}</div>
                        <div class="forecast-icon-container"><img src="data:image/png;base64,{icon_b64}"></div>
                        <div class="forecast-temp">{temp}°C</div>
                        <div class="forecast-desc">{desc}</div>
                    </div>"""
    html_boxes += "</div>"
    st.markdown(html_boxes, unsafe_allow_html=True)

    # ---------------- EXTRA ----------------
    st.markdown("<div style='height:5px;'></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex; align-items:center; gap:8px; font-weight: 600; font-size: 20px; color: White; margin-bottom: 10px;'><img src='data:image/png;base64,{earth_icon}' width='30' height='30'><span>Additional Details</span></div>", unsafe_allow_html=True)
    
    warm_alert = ""
    if data['main']['temp'] > 30:
        warm_alert = "<div class='warm-alert-box' style='background: #fff9e6; border: 1px solid #ffeeba; border-radius: 12px; padding: 12px 15px; color: #856404; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.02); width: 250px; box-sizing: border-box; height: 44px;'><svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' fill='#ff9800' class='bi bi-exclamation-triangle-fill' viewBox='0 0 16 16'><path d='M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2'/></svg><span>Warm Alert: Stay hydrated!</span></div>"
    else:
        warm_alert = "<div class='warm-alert-box warm-alert-hidden' style='width: 260px; height: 44px; visibility: hidden;'></div>"
        
    lat = data['coord']['lat']
    lon = data['coord']['lon']
    if aqi_val is None:
        aqi_desc = "N/A"
    elif aqi_val <= 50:
        aqi_desc = "Good"
    elif aqi_val <= 100:
        aqi_desc = "Moderate"
    elif aqi_val <= 300:
        aqi_desc = "Unhealthy"
    else:
        aqi_desc = "Hazardous"
        
    aqi_display = f"{aqi_val} ({aqi_desc})" if aqi_val is not None else "N/A"

    st.markdown(f"""
    <div class="dynamic-card additional-details-card">
        <div class="details-list">
            <div class="details-item">
                <img src="data:image/png;base64,{temperature_icon_new}" width="25" height="25">
                <span class="details-text">Feels Like: <b>{int(data['main']['feels_like'])} °C</b></span>
            </div>
            <div class="details-divider"></div>
            <div class="details-item">
                <img src="data:image/png;base64,{cloud_icon_new}" width="25" height="25">
                <span class="details-text">Cloud Cover: <b>{data['clouds']['all']}%</b></span>
            </div>
            <div class="details-divider"></div>
            <div class="details-item">
                <img src="data:image/png;base64,{wind_icon}" width="25" height="25">
                <span class="details-text">AQI: <b>{aqi_display}</b></span>
            </div>
        </div>
        {warm_alert}
    </div>
    """, unsafe_allow_html=True)