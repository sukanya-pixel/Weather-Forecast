import streamlit as st
import requests
import datetime
import matplotlib.pyplot as plt
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(layout="wide")

# ---------------- CSS (MAIN MAGIC) ----------------
st.markdown("""
<style>

body {
    background-color: #013a63;
}

.stApp {
    background-color: #013a63;
}

.block-container {
    padding-top: 1rem !important;
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
.block-container {
    padding-top: 1rem !important;
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
API_KEY = "e389a52b0df383a9027789a81046f191"

def get_base64_image(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()

loc_icon = get_base64_image(r"D:\Pinnacle\Weather\location.png")
search_icon = get_base64_image(r"D:\Pinnacle\Weather\search.png")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_forecast(city):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

# ---------------- STATE ----------------
if "city" not in st.session_state:
    st.session_state.city = "Bhubaneswar"

if "search" not in st.session_state:
    st.session_state.search = False

# ---------------- HEADER & CARD CSS FIXES ----------------
st.markdown("""
<style>

/* HEADER CARD */
div[data-testid="stHorizontalBlock"]:has(.header-marker) {
    background:white;
    padding:12px 20px;  /* reduce side padding */
    border-radius:25px;
    box-shadow:10px 14px 6px rgba(0,0,0,0.09);
    margin-top:30px;
    margin-bottom:10px;
}

/* REMOVE COLUMN PADDING (important) */
div[data-testid="column"] {
    padding: 0 !important;
}

/* LEFT TEXT */
div[data-testid="stHorizontalBlock"]:has(.header-marker) 
div[data-testid="column"]:nth-child(1) {
    display:flex;
    align-items:center;
}

/* RIGHT BUTTON COLUMN */
div[data-testid="stHorizontalBlock"]:has(.header-marker) 
div[data-testid="column"]:nth-child(2) {
    display:flex;
    justify-content:flex-end;
    align-items:center;
}

/* FORCE BUTTON TO EXTREME RIGHT */
div.stButton {
    width:100%;
    display:flex;
    justify-content:flex-end;
}

div.stButton > button {
    margin-right:0;
}

/* MAIN CARDS CSS FIX */
div[data-testid="column"]:has(.card-marker) {
    background: white;
    padding: 20px !important;
    border-radius: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# HEADER BLOCK

col1, col2 = st.columns([10,1])

with col1:
    st.markdown(f"""
    <div class="header-marker" style="
        display:flex;
        align-items:center;
        gap:8px;
        font-size:18px;
        font-weight:500;
        padding-bottom:15px
    ">
        <img src="data:image/jpeg;base64,{loc_icon}" width="18">
        {st.session_state.city.title()}
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <style>
    /* Anchor to the entire header card so we can perfectly right-align */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) {{
        position: relative !important;
    }}
    /* Position the button relative to the header card itself */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        width: 30px !important;
        height: 30px !important;
        padding: 0 !important;
        position: absolute !important;
        right: 20px !important; /* Matches the card's 20px side padding exactly */
        top: 50% !important;
        transform: translateY(-50%) !important;
        margin: 0 !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button:hover {{
        background: transparent !important;
        border: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button:focus {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button:active {{
        background: transparent !important;
        border: none !important;
    }}
    /* Render image OVER the transparent button */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button::after {{
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 20px;
        height: 20px;
        background-image: url("data:image/png;base64,{search_icon}");
        background-size: contain;
        background-repeat: no-repeat;
        background-position: center;
        pointer-events: none;
    }}
    /* Hide button text */
    div[data-testid="stHorizontalBlock"]:has(.header-marker) button p {{
        display: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)
    if st.button("\u200B", key="search_btn"):
        st.session_state.search = not st.session_state.search

# ---------------- SEARCH ----------------
def submit_search():
    new_city = st.session_state.search_input.strip()
    if new_city:
        st.session_state.city = new_city
        st.session_state.search = False

if st.session_state.search:
    st.text_input("Search city and press Enter", key="search_input", on_change=submit_search)


city = st.session_state.city

# ---------------- FETCH ----------------
data = get_weather(city)
forecast = get_forecast(city)

if str(data.get("cod")) != "200":
    st.error("Error fetching weather")
else:

    # ---------------- MAIN CARDS ----------------
    col1, col2, col3 = st.columns([1.8, 1.4, 1.2], gap="large")

    # WEATHER CARD
    with col1:
        icon = data['weather'][0]['icon']
        desc = data['weather'][0]['description'].title()
        temp = int(data['main']['temp'])
        pressure = data['main']['pressure']
        visibility = data['visibility'] // 1000
        humidity = data['main']['humidity']
        st.markdown(f"""
        <div style="background: #89c2d9; padding: 25px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; height: 260px; display: flex; flex-direction: column; justify-content: space-between;">
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <div style="font-weight: 600; font-size: 16px; margin-bottom: 5px; color: #111;">📍 {city}</div>
                    <div style="font-size: 48px; font-weight: bold; line-height: 1.2; color: #111;">{temp}°<span style="font-size: 24px;">C</span></div>
                    <div style="font-size: 14px; margin-top: 5px; color: #555;">{desc}</div>
                </div>
                <div>
                    <img src="http://openweathermap.org/img/wn/{icon}@4x.png" width="120" style="margin-top: -10px;">
                </div>
            </div>
            <div style="display: flex; gap: 10px; margin-top: 25px;">
                <div style="flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 18px; color: #666;">Pressure</div>
                    <div style="font-size: 18px; color: #0d6efd; font-weight: 800; margin-top: 5px;">{pressure} mb</div>
                </div>
                <div style="flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 18px; color: #666;">Visibility</div>
                    <div style="font-size: 18px; color: #0d6efd; font-weight: 800; margin-top: 5px;">{visibility} km</div>
                </div>
                <div style="flex: 1; border: 1px solid #eee; border-radius: 8px; padding: 10px; text-align: center;">
                    <div style="font-size: 18px; color: #666;">Humidity</div>
                    <div style="font-size: 18px; color: #0d6efd; font-weight: 800; margin-top: 5px;">{humidity}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # WIND CARD
    with col2:
        speed = data['wind']['speed']
        pct = min(int(speed * 10), 100)
        st.markdown(f"""
        <div style="background: #89c2d9; padding: 25px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; height: 260px; display: flex; flex-direction: column;">
            <div style="font-weight: 600; font-size: 16px; margin-bottom: 20px; color: #111;">💨 Wind Info</div>
            <div style="font-size: 42px; font-weight: bold; color: #0d6efd; line-height: 1;">{speed} <span style="font-size: 24px; font-weight: 500;">m/s</span></div>
            <div style="font-size: 14px; margin-top: auto; margin-bottom: 8px; color: #555;">Wind Speed</div>
            <div style="width: 100%; background-color: #e9ecef; border-radius: 4px; height: 10px; margin-bottom: 10px;">
                <div style="width: {pct}%; background-color: #0d6efd; height: 10px; border-radius: 4px;"></div>
            </div>
            <div style="font-size: 14px; font-weight: 600; color: #111;">{pct}%</div>
        </div>
        """, unsafe_allow_html=True)

    # SUN CARD
    with col3:
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        
        st.markdown(f"""
        <div style="background: #89c2d9; padding: 25px; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0; height: 260px; display: flex; flex-direction: column; justify-content: center;">
            <div>
                <div style="font-size: 15px; margin-bottom: 8px; font-weight: 500; color: #111;">🌅 Sunrise:</div>
                <div style="font-size: 28px; font-weight: bold; padding-left: 28px; color: #111;">{sunrise}</div>
            </div>
            <hr style="margin: 20px 0; border: none; border-top: 1px solid #eee;">
            <div>
                <div style="font-size: 15px; margin-bottom: 8px; font-weight: 500; color: #111;">🌇 Sunset:</div>
                <div style="font-size: 28px; font-weight: bold; padding-left: 28px; color: #111;">{sunset}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ---------------- GRAPH & FORECAST ROW ----------------
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    
    t1, t2 = st.columns([1.5, 1], gap="large")
    with t1:
        st.markdown("<div style='font-weight: 600; font-size: 16px; color: #111; margin-bottom: -10px;'>📈 Temperature Trend (Next 24 Hours)</div>", unsafe_allow_html=True)
    with t2:
        st.markdown("<div style='font-weight: 600; font-size: 16px; color: #111; margin-bottom: -10px;'>📅 5-Day Forecast</div>", unsafe_allow_html=True)
        
    st.markdown("<div style='height:15px;'></div>", unsafe_allow_html=True)

    r2c1, r2c2 = st.columns([1.5, 1], gap="large")
    
    with r2c1:
        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
        temps = []
        times = []
        for i in range(min(8, len(forecast['list']))):
            item = forecast['list'][i]
            temps.append(item['main']['temp'])
            times.append(item['dt_txt'][11:16])
            
        fig, ax = plt.subplots(figsize=(8,3.5))
        ax.plot(times, temps, marker='o', color='#0d6efd', linewidth=2)
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        ax.grid(axis='y', linestyle='-', alpha=0.3)
        ax.grid(axis='x', linestyle='-', alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#ddd')
        plt.xticks(fontsize=9, color='#666')
        plt.yticks(fontsize=9, color='#666')
        ax.set_ylabel('°C', color='#666', rotation=0, labelpad=15)
        st.pyplot(fig)
        
    with r2c2:
        html_boxes = "<div style='display:flex; gap:10px; justify-content:space-between;'>"
        for i in range(min(5, len(forecast['list']) // 8)):
            d = forecast['list'][i*8]
            dt_obj = datetime.datetime.strptime(d['dt_txt'], '%Y-%m-%d %H:%M:%S')
            date_str = dt_obj.strftime('%d %b')
            icon = d['weather'][0]['icon']
            temp = int(d['main']['temp'])
            desc = d['weather'][0]['main']
            html_boxes += f"""
            <div style="flex:1; background:#89c2d9; padding:15px 5px; border-radius:12px; text-align:center; box-shadow: 0 4px 12px rgba(0,0,0,0.05); border: 1px solid #f0f0f0;">
                <div style="font-size:12px; color:#333; margin-bottom:8px; font-weight:500;">{date_str}</div>
                <img src="http://openweathermap.org/img/wn/{icon}@2x.png" width="40" style="margin-bottom:8px;">
                <div style="font-weight:bold; color:#dc3545; font-size:16px;">{temp}°C</div>
                <div style="font-size:11px; color:#666; margin-top:5px;">{desc}</div>
            </div>
            """
        html_boxes += "</div>"
        st.markdown(html_boxes, unsafe_allow_html=True)

    # ---------------- EXTRA ----------------
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-weight: 600; font-size: 16px; margin-bottom: 10px;'>🌍 Additional Details</div>", unsafe_allow_html=True)
    
    warm_alert = ""
    if data['main']['temp'] > 30:
        warm_alert = """
        <div>
            <div style="background: rgba(255, 165, 0, 0.15); padding:10px 20px; border-radius:8px; color:#ff9800; font-size:14px; font-weight:600; display:flex; align-items:center; gap:8px;">
                ⚠️ Warm Alert: Stay hydrated!
            </div>
        </div>
        """
        
    st.markdown(f"""
    <div style="background:#89c2d9; border-radius:12px; padding:20px 30px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); display:flex; justify-content:space-between; align-items:center; border: 1px solid #f0f0f0;">
        <div style="display: flex; gap: 40px; align-items:center;">
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:24px;">🌡️</span> 
                <span style="font-size:14px; color:#333;">Feels Like: <b>{data['main']['feels_like']} °C</b></span>
            </div>
            <div style="display:flex; align-items:center; gap:10px;">
                <span style="font-size:24px; color:#0d6efd;">👁️</span> 
                <span style="font-size:14px; color:#333;">Visibility: <b>{data['visibility']} m</b></span>
            </div>
        </div>
        
        <div style="display:flex; align-items:center; gap:10px; border-left: 1px solid #eee; padding-left: 40px; margin-right: auto; margin-left: 40px;">
            <span style="font-size:24px;">☁️</span> 
            <span style="font-size:14px; color:#333;">Cloud Cover: <b>{data['clouds']['all']}%</b></span>
        </div>
        
        {warm_alert}
    </div>
    """, unsafe_allow_html=True)