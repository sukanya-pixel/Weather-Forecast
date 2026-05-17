import streamlit as st
import requests
import datetime
import matplotlib.pyplot as plt
import base64
import os
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
    background-color: #013a63;
}

.stApp {
    background-color: #013a63;
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

</style>
""", unsafe_allow_html=True)

# ---------------- API ----------------
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

search_icon = get_base64_image(r"Data\search.png")
gps_icon = get_base64_image(r"Data\gps.png")
wind_icon = get_base64_image(r"Data\wind.png")
sunrise_icon = get_base64_image(r"Data\sunrise.png")
sunset_icon = get_base64_image(r"Data\sunset.png")
bar_graph_icon = get_base64_image(r"Data\bar-graph.png")
calendar_icon = get_base64_image(r"Data\calendar.png")
clouds_icon = get_base64_image(r"Data\clouds.png")

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
        return get_base64_image(rf"Data\condition\{filename}")
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
        return res['list'][0]['main']['aqi']
    except:
        return None

# ---------------- STATE ----------------
if "city" not in st.session_state:
    st.session_state.city = "Bhubaneswar"

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

/* MAIN CARDS CSS FIX */
div[data-testid="column"]:has(.card-marker) {
    background: white;
    padding: 25px 40px !important;
    border-radius: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
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
    margin-bottom: 0px;
">
    <img src="data:image/png;base64,{clouds_icon}" width="50" style="filter: drop-shadow(0px 4px 8px rgba(0,0,0,0.15));">
    <div style="
        font-size:48px;
        font-weight:800;
        color:white;
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

col1, col2 = st.columns([15, 1])

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
        <img src="data:image/png;base64,{gps_icon}" width="26" style="margin:0; padding:0; display:block;">
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
        if st.button("", key="toggle_search_on"):
            st.session_state.search = True
            st.rerun()
    else:
        st.markdown(f"""
        <style>
        /* Absolute position the active search input container to flush right */
        div[data-testid="stHorizontalBlock"]:has(.header-marker) > div[data-testid="column"]:last-child div[data-testid="stElementContainer"]:has(input) {{
            position: absolute !important;
            right: 0 !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
            width: 680px !important;
            z-index: 100;
            margin: 0 !important;
            padding: 0 !important;
        }}
        /* Ensure the inner Streamlit wrappers stretch fully and have no padding */
        div[data-testid="stHorizontalBlock"]:has(.header-marker) > div[data-testid="column"]:last-child div.stTextInput div {{
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }}
        /* Style the input box itself */
        div[data-testid="stHorizontalBlock"]:has(.header-marker) > div[data-testid="column"]:last-child div.stTextInput input {{
            border-radius: 20px !important;
            border: 1px solid #ccc !important;
            padding: 0 15px !important;
            background-color: white !important;
            color: #333 !important;
            width: 100% !important;
            min-height: 32px !important;
            height: 32px !important;
            margin: 0 !important;
            box-sizing: border-box !important;
        }}
        /* Hide labels and instructions to prevent extra layout padding */
        div[data-testid="stHorizontalBlock"]:has(.header-marker) > div[data-testid="column"]:last-child label,
        div[data-testid="stHorizontalBlock"]:has(.header-marker) > div[data-testid="column"]:last-child div[data-testid="InputInstructions"] {{
            display: none !important;
            margin: 0 !important;
            height: 0 !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        st.text_input("", placeholder="Search here...", key="search_input", on_change=submit_search, label_visibility="collapsed")


city = st.session_state.city

# ---------------- FETCH ----------------
data = get_weather(city)
forecast = get_forecast(city)

if str(data.get("cod")) != "200":
    st.error("Error fetching weather")
else:

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
        <div style="background: #89c2d9; padding: 25px 40px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; height: 230px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <div style="font-size: 50px; font-weight: bold; line-height: 1.1; color: #111;">{temp}°<span style="font-size: 20px;">C</span></div>
                    <div style="font-size: 16px; margin-top: 1px; color: #111; font-weight: 600;"><span style="color: #dc3545;">▲</span> H: {temp_max}° &nbsp; <span style="color: #0d6efd;">▼</span> L: {temp_min}°</div>
                    <div style="font-size: 18px; margin-top: 1px; color: #555;">{desc}</div>
                </div>
                <div>
                    <img src="data:image/png;base64,{icon_b64}" width="120" style="margin-top: -5px;">
                </div>
            </div>
            <div style="display: flex; gap: 8px; margin-top: 10px;">
                <div style="flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 6px 4px; text-align: center; height: 62px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 14px; color: #666; white-space: nowrap;">Pressure</div>
                    <div style="font-size: 15px; color: #0d6efd; font-weight: 800;">{pressure} mb</div>
                </div>
                <div style="flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 6px 4px; text-align: center; height: 62px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 14px; color: #666; white-space: nowrap;">Visibility</div>
                    <div style="font-size: 15px; color: #0d6efd; font-weight: 800;">{visibility} km</div>
                </div>
                <div style="flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 6px 4px; text-align: center; height: 62px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 14px; color: #666; white-space: nowrap;">Humidity</div>
                    <div style="font-size: 15px; color: #0d6efd; font-weight: 800;">{humidity}%</div>
                </div>
                <div style="flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 6px 4px; text-align: center; height: 62px; display: flex; flex-direction: column; justify-content: center;">
                    <div style="font-size: 14px; color: #666; white-space: nowrap;">Precipitation</div>
                    <div style="font-size: 15px; color: #0d6efd; font-weight: 800;">{precip_prob}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    # WIND CARD
    with col2:
        speed = data['wind']['speed']
        pct = min(int(speed * 10), 100)
        st.markdown(f"""
        <div style="background: #89c2d9; padding: 25px 40px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; height: 230px; display: flex; flex-direction: column;">
            <div style="font-weight: 600; font-size: 18px; margin-bottom: 10px; color: #111; display: flex; align-items: center; gap: 8px;"><img src="data:image/png;base64,{wind_icon}" width="20"> Wind Info</div>
            <div style="font-size: 34px; margin-top: 10px; font-weight: bold; color: #0d6efd; line-height: 1;">{speed} <span style="font-size: 18px; font-weight: 500;">m/s</span></div>
            <div style="font-size: 16px; margin-top: 20px; margin-bottom: 4px; color: #555;">Wind Speed</div>
            <div style="width: 100%; margin-top: 5px; background-color: #e9ecef; border-radius: 4px; height: 10px; margin-bottom: 6px;">
                <div style="width: {pct}%; background-color: #0d6efd; height: 10px; border-radius: 4px;"></div>
            </div>
            <div style="font-size: 16px; margin-top: 5px; font-weight: 600; color: #111;">{pct}%</div>
        </div>
        """, unsafe_allow_html=True)
 
    # SUN CARD
    with col3:
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
         
        st.markdown(f"""
        <div style="background: #89c2d9; padding: 25px 40px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; height: 230px; display: flex; flex-direction: column; justify-content: center;">
            <div>
                <div style="font-size: 18px; margin-bottom: 4px; font-weight: 500; color: #111; display: flex; align-items: center; gap: 8px;"><img src="data:image/png;base64,{sunrise_icon}" width="20"> Sunrise:</div>
                <div style="font-size: 26px; font-weight: bold; padding-left: 28px; color: #111;">{sunrise}</div>
            </div>
            <hr style="margin: 10px 0; border: none; border-top: 1px solid #eee;">
            <div>
                <div style="font-size: 18px; margin-bottom: 4px; font-weight: 500; color: #111; display: flex; align-items: center; gap: 8px;"><img src="data:image/png;base64,{sunset_icon}" width="20"> Sunset:</div>
                <div style="font-size: 26px; font-weight: bold; padding-left: 28px; color: #111;">{sunset}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- GRAPH & FORECAST ROW ----------------
    st.markdown("<div style='height:5px;'></div>", unsafe_allow_html=True)
    
    t1, t2 = st.columns([1, 1.6], gap="large")
    with t1:
        st.markdown(f"<div style='display:flex; align-items:center; gap:8px; font-weight: 600; font-size: 20px; color: #111; margin-bottom: -20px;'><img src='data:image/png;base64,{bar_graph_icon}' width='20' height='20'><span>Temperature Trend (Next 24 Hours)</span></div>", unsafe_allow_html=True)
    with t2:
        st.markdown(f"<div style='display:flex; align-items:center; gap:8px; font-weight: 600; font-size: 20px; color: #111; margin-bottom: -20px;'><img src='data:image/png;base64,{calendar_icon}' width='20' height='20'><span>7-Day Forecast</span></div>", unsafe_allow_html=True)
        
    st.markdown("<div style='height:5px;'></div>", unsafe_allow_html=True)

    r2c1, r2c2 = st.columns([1, 1.6], gap="large")
    
    with r2c1:
        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
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
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        ax.grid(axis='y', linestyle='-', alpha=0.3)
        ax.grid(axis='x', linestyle='-', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#ddd')
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, fontsize=11, color='black')
        ax.tick_params(axis='x', length=0, pad=2, colors='black', labelsize=11)
        ax.yaxis.set_major_locator(plt.MaxNLocator(nbins=6))
        plt.yticks(fontsize=11, color='black')
        ax.tick_params(axis='y', length=0, pad=3, colors='black', labelsize=11)
        ax.set_ylabel('°C', color='black', fontsize=12, rotation=0, labelpad=15)
        fig.tight_layout(pad=1.5)
        st.pyplot(fig)
    with r2c2:
        st.markdown("<div style='margin-top:-10px;'></div>", unsafe_allow_html=True)
        html_boxes = "<div style='display:flex; gap:8px; justify-content:space-between;'>"
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
            html_boxes += f"""<div style="flex:1; height:130px; display:flex; flex-direction:column; justify-content:space-between; background:#89c2d9; padding:8px 5px; border-radius:12px; text-align:center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; box-sizing:border-box;">
                            <div style="font-size:14px; color:#111; font-weight:600;">{date_str}</div>
                            <div><img src="data:image/png;base64,{icon_b64}" width="30"></div>
                            <div style="font-weight:bold; color:#dc3545; font-size:16px;">{temp}°C</div>
                            <div style="font-size:12px; color:#333; font-weight:500;">{desc}</div>
                        </div>"""
        html_boxes += "</div>"
        st.markdown(html_boxes, unsafe_allow_html=True)

        # ---------------- EXTRA ----------------
        st.markdown("<div style='height:5px;'></div>", unsafe_allow_html=True)
        st.markdown("<div style='font-weight: 600; font-size: 20px; margin-bottom: 10px;'>🌍 Additional Details</div>", unsafe_allow_html=True)
        
        warm_alert = ""
        if data['main']['temp'] > 30:
            warm_alert = "<div style='background: #fff9e6; border: 1px solid #ffeeba; border-radius: 12px; padding: 12px 15px; color: #856404; font-size: 14px; font-weight: 600; display: flex; align-items: center; gap: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.02); width: 260px; box-sizing: border-box; height: 44px;'><svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' fill='#ff9800' class='bi bi-exclamation-triangle-fill' viewBox='0 0 16 16'><path d='M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5m.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2'/></svg><span>Warm Alert: Stay hydrated!</span></div>"
        else:
            warm_alert = "<div style='width: 260px; height: 44px; visibility: hidden;'></div>"
            
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        aqi_val = get_aqi(lat, lon)
        aqi_labels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        aqi_desc = aqi_labels.get(aqi_val, "N/A")
        aqi_display = f"{aqi_val} ({aqi_desc})" if aqi_val is not None else "N/A"

        st.markdown(f"""<div style="background: white; border-radius: 15px; padding: 10px 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; border: 1px solid #f0f0f0;"><div style="display: flex; gap: 20px; align-items: center;"><div style="display: flex; align-items: center; gap: 6px;"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#0d6efd" class="bi bi-thermometer-half" viewBox="0 0 16 16"><path d="M9.5 12.5a1.5 1.5 0 1 1-2-1.415V9.5a.5.5 0 1 1 1 0v1.585c.67.143 1.185.66 1.185 1.415z"/><path d="M5.5 2.5a2.5 2.5 0 0 1 5 0v7.55a3.5 3.5 0 1 1-5 0zM8 1a1.5 1.5 0 0 0-1.5 1.5v7.987l-.167.15a2.5 2.5 0 1 0 3.333 0l-.166-.15V2.5A1.5 1.5 0 0 0 8 1z"/></svg><span style="font-size: 16px; color: #333; white-space: nowrap;">Feels Like: <b>{int(data['main']['feels_like'])} °C</b></span></div><div style="border-left: 1px solid #eef2f6; height: 30px;"></div><div style="display: flex; align-items: center; gap: 6px;"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#0d6efd" class="bi bi-cloud-fill" viewBox="0 0 16 16"><path d="M4.406 3.342A5.53 5.53 0 0 1 8 2c2.69 0 4.923 2 5.166 4.579C14.758 6.804 16 8.137 16 9.773 16 11.569 14.502 13 12.687 13H3.781C1.708 13 0 11.366 0 9.318c0-1.763 1.266-3.223 2.942-3.593.143-.863.698-1.723 1.464-2.383zm.653.757c-.757.653-1.153 1.44-1.153 2.056v.448l-.445.049C2.064 6.805 1 7.952 1 9.318 1 10.74 2.242 12 3.781 12h8.906C13.98 12 15 10.988 15 9.773c0-1.216-1.02-2.228-2.313-2.228h-.5v-.5C12.188 4.5 10.303 3 8 3a4.53 4.53 0 0 0-2.941 1.1z"/></svg><span style="font-size: 16px; color: #333; white-space: nowrap;">Cloud Cover: <b>{data['clouds']['all']}%</b></span></div><div style="border-left: 1px solid #eef2f6; height: 30px;"></div><div style="display: flex; align-items: center; gap: 6px;"><svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="#0d6efd" class="bi bi-wind" viewBox="0 0 16 16"><path d="M12.5 2A2.5 2.5 0 0 0 10 4.5a.5.5 0 0 1-1 0A3.5 3.5 0 1 1 12.5 8H.5a.5.5 0 0 1 0-1h12a2.5 2.5 0 0 0 0-5zm-7 1a1 1 0 0 0-1 1 .5.5 0 0 1-1 0 2 2 0 1 1 2 2h-5a.5.5 0 0 1 0-1h5a1 1 0 0 0 0-2zM0 11.5a.5.5 0 0 1 .5-.5h11.75A2.75 2.75 0 1 1 9.5 13.75a.5.5 0 0 1 1 0 1.75 1.75 0 1 0 1.75-1.75H.5a.5.5 0 0 1-.5-.5z"/></svg><span style="font-size: 16px; color: #333; white-space: nowrap;">AQI: <b>{aqi_display}</b></span></div></div>{warm_alert}</div>""", unsafe_allow_html=True)