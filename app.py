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
    background-color: #f5f7fb;
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
    padding:20px 20px;  /* reduce side padding */
    border-radius:25px;
    box-shadow:10px 14px 6px rgba(0,0,0,0.09);
    margin-top:30px;
    margin-bottom:10px;
}

/* REMOVE COLUMN PADDING (important) */
div[data-testid="column"] {
    padding: 5 !important;
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
    ">
        <img src="data:image/jpeg;base64,{loc_icon}" width="18">
        {st.session_state.city.title()}
    </div>
    """, unsafe_allow_html=True)

with col2:
    clicked = st.markdown(f"""
    <div style="display:flex; justify-content:flex-end;">
        <button style="
            border:none;
            background:transparent;
            cursor:pointer;
        " onclick="window.location.reload()">
            <img src="data:image/png;base64,{search_icon}" width="20">
        </button>
    </div>
    """, unsafe_allow_html=True)
# ---------------- SEARCH ----------------
if st.session_state.search:
    new_city = st.text_input("Search city")
    if new_city:
        st.session_state.city = new_city


city = st.session_state.city

# ---------------- FETCH ----------------
data = get_weather(city)
forecast = get_forecast(city)

if str(data.get("cod")) != "200":
    st.error("Error fetching weather")
else:

    # ---------------- MAIN CARDS ----------------
    st.markdown("<div style='height:70px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2,2,1], gap="large")

    # WEATHER CARD
    with col1:
        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
        st.markdown(f"### 📍 {city}")
        st.markdown(f"<h1 style='margin:0'>{data['main']['temp']}°C</h1>", unsafe_allow_html=True)
        st.write(data['weather'][0]['description'])

        icon = data['weather'][0]['icon']
        st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png", width=100)

        c1, c2, c3 = st.columns(3)
        c1.metric("Pressure", f"{data['main']['pressure']} mb")
        c2.metric("Visibility", f"{data['visibility']/1000} km")
        c3.metric("Humidity", f"{data['main']['humidity']}%")


    # WIND CARD
    with col2:
        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
        st.markdown("### 🌬️ Wind Info")
        st.markdown(f"<h1>{data['wind']['speed']} m/s</h1>", unsafe_allow_html=True)

        st.write("Wind Speed")
        st.progress(min(int(data['wind']['speed'] * 10), 100))


    # SUN CARD
    with col3:
        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        st.write("🌅 Sunrise:", sunrise.strftime('%H:%M'))
        st.write("🌇 Sunset:", sunset.strftime('%H:%M'))

    # ---------------- GRAPH ----------------
    temps = []
    times = []

    for i in range(min(8, len(forecast['list']))):
        item = forecast['list'][i]
        temps.append(item['main']['temp'])
        times.append(item['dt_txt'][11:16])
        
    graph_col, = st.columns(1)
    with graph_col:
        st.markdown('<div class="card-marker"></div>', unsafe_allow_html=True)
        st.markdown("### 📈 Temperature Trend (Next 24 Hours)")

        plt.figure(figsize=(8,4))
        plt.plot(times, temps, marker='o')
        plt.xticks(rotation=45)
        plt.grid()

        st.pyplot(plt)

    # ---------------- FORECAST ----------------
    st.markdown("### 📅 5-Day Forecast")

    cols = st.columns(5)

    for i in range(min(5, len(forecast['list']) // 8)):
        d = forecast['list'][i*8]
        with cols[i]:
            st.markdown(f"""
            <div style="
                background:white;
                padding:15px;
                border-radius:12px;
                text-align:center;
                box-shadow:0 3px 8px rgba(0,0,0,0.08);
            ">
                <b>{d['dt_txt'][:10]}</b><br><br>
                🌡️ {d['main']['temp']}°C<br>
                {d['weather'][0]['main']}
            </div>
            """, unsafe_allow_html=True)

    # ---------------- EXTRA ----------------
    st.markdown("### 🌍 Additional Details")

    colA, colB, colC = st.columns([2,2,2])

    with colA:
        st.write(f"🌡️ Feels Like: {data['main']['feels_like']} °C")
        st.write(f"👁️ Visibility: {data['visibility']} m")

    with colB:
        st.write(f"☁️ Cloud Cover: {data['clouds']['all']}%")

    with colC:
        if data['main']['temp'] > 30:
            st.markdown("""
            <div style="
                background:#fff4e5;
                padding:15px;
                border-radius:10px;
                color:#a85b00;
                font-weight:500;
            ">
            ⚠️ Warm Alert: Stay hydrated!
            </div>
            """, unsafe_allow_html=True)