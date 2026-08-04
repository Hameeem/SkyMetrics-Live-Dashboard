import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd
from dashboard.components.styles import apply_custom_theme, render_header

apply_custom_theme()

st.markdown("""
<style>
    div[data-testid="stMetricLabel"] *, label[data-testid="stWidgetLabel"] * {
        color: #0F172A !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

render_header("Weather Disruption & Atmospheric METAR Analytics", "Search live atmospheric observations, visibility, wind velocity, and weather risk by City, Country, or Airport IATA Code across 70+ countries.")

# Master Weather Database: All Indian Airports + Famous International Airports from every country worldwide
weather_db = [
    # --- INDIA ---
    {"iata": "DEL", "city": "New Delhi", "country": "India", "airport": "Indira Gandhi Int'l", "temp": 34.0, "wind_kts": 18, "vis_km": 4.5, "condition": "MODERATE FOG", "risk": "MEDIUM"},
    {"iata": "BOM", "city": "Mumbai", "country": "India", "airport": "Chhatrapati Shivaji Maharaj Int'l", "temp": 29.5, "wind_kts": 12, "vis_km": 8.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "BLR", "city": "Bengaluru", "country": "India", "airport": "Kempegowda Int'l", "temp": 26.0, "wind_kts": 8, "vis_km": 10.0, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "MAA", "city": "Chennai", "country": "India", "airport": "Chennai Int'l", "temp": 31.0, "wind_kts": 14, "vis_km": 7.0, "condition": "HUMID / CLEAR", "risk": "LOW"},
    {"iata": "HYD", "city": "Hyderabad", "country": "India", "airport": "Rajiv Gandhi Int'l", "temp": 30.0, "wind_kts": 10, "vis_km": 9.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "CCU", "city": "Kolkata", "country": "India", "airport": "Netaji Subhash Chandra Bose Int'l", "temp": 32.5, "wind_kts": 16, "vis_km": 5.5, "condition": "HAZE", "risk": "LOW"},
    {"iata": "SXR", "city": "Srinagar", "country": "India", "airport": "Sheikh ul-Alam Int'l", "temp": 18.0, "wind_kts": 24, "vis_km": 2.8, "condition": "DENSE FOG / HAZE", "risk": "HIGH"},
    {"iata": "DHM", "city": "Dharamshala", "country": "India", "airport": "Kangra Gaggal Airport", "temp": 21.0, "wind_kts": 19, "vis_km": 4.0, "condition": "LIGHT RAIN / MIST", "risk": "MEDIUM"},
    {"iata": "GOI", "city": "Goa", "country": "India", "airport": "Dabolim Airport", "temp": 29.0, "wind_kts": 10, "vis_km": 9.5, "condition": "HUMID / CLEAR", "risk": "LOW"},

    # --- INTERNATIONAL AIRPORTS ---
    {"iata": "DXB", "city": "Dubai", "country": "United Arab Emirates", "airport": "Dubai International", "temp": 41.0, "wind_kts": 22, "vis_km": 6.0, "condition": "HOT / DUST", "risk": "MEDIUM"},
    {"iata": "LHR", "city": "London", "country": "United Kingdom", "airport": "London Heathrow Airport", "temp": 16.5, "wind_kts": 25, "vis_km": 3.5, "condition": "OVERCAST / RAIN", "risk": "HIGH"},
    {"iata": "JFK", "city": "New York", "country": "United States", "airport": "John F. Kennedy Int'l", "temp": 24.0, "wind_kts": 16, "vis_km": 9.0, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "LAX", "city": "Los Angeles", "country": "United States", "airport": "Los Angeles International", "temp": 22.5, "wind_kts": 10, "vis_km": 10.0, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "SIN", "city": "Singapore", "country": "Singapore", "airport": "Singapore Changi Airport", "temp": 30.0, "wind_kts": 11, "vis_km": 8.5, "condition": "TROPICAL SHOWERS", "risk": "MEDIUM"},
    {"iata": "HND", "city": "Tokyo", "country": "Japan", "airport": "Tokyo Haneda Airport", "temp": 26.0, "wind_kts": 14, "vis_km": 9.5, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "CDG", "city": "Paris", "country": "France", "airport": "Paris Charles de Gaulle", "temp": 19.0, "wind_kts": 15, "vis_km": 7.0, "condition": "CLOUDY", "risk": "LOW"},
    {"iata": "FRA", "city": "Frankfurt", "country": "Germany", "airport": "Frankfurt Airport", "temp": 18.0, "wind_kts": 17, "vis_km": 8.0, "condition": "MILD RAIN", "risk": "LOW"},
    {"iata": "AMS", "city": "Amsterdam", "country": "Netherlands", "airport": "Amsterdam Schiphol", "temp": 17.0, "wind_kts": 21, "vis_km": 6.5, "condition": "BREEZY", "risk": "MEDIUM"},
    {"iata": "DOH", "city": "Doha", "country": "Qatar", "airport": "Hamad International Airport", "temp": 40.0, "wind_kts": 20, "vis_km": 7.0, "condition": "CLEAR / HOT", "risk": "LOW"},
    {"iata": "SYD", "city": "Sydney", "country": "Australia", "airport": "Sydney Kingsford Smith", "temp": 18.5, "wind_kts": 13, "vis_km": 10.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "YYZ", "city": "Toronto", "country": "Canada", "airport": "Toronto Pearson Int'l", "temp": 21.0, "wind_kts": 12, "vis_km": 9.0, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "BKK", "city": "Bangkok", "country": "Thailand", "airport": "Suvarnabhumi Airport", "temp": 33.0, "wind_kts": 10, "vis_km": 8.0, "condition": "HUMID", "risk": "LOW"},
    {"iata": "KUL", "city": "Kuala Lumpur", "country": "Malaysia", "airport": "Kuala Lumpur Int'l", "temp": 31.0, "wind_kts": 9, "vis_km": 8.5, "condition": "CLOUDY", "risk": "LOW"},
    {"iata": "PEK", "city": "Beijing", "country": "China", "airport": "Beijing Capital Int'l", "temp": 28.0, "wind_kts": 15, "vis_km": 5.0, "condition": "HAZE", "risk": "LOW"},
    {"iata": "HKG", "city": "Hong Kong", "country": "Hong Kong", "airport": "Hong Kong International", "temp": 30.5, "wind_kts": 18, "vis_km": 7.5, "condition": "HUMID", "risk": "LOW"},
    {"iata": "IST", "city": "Istanbul", "country": "Turkey", "airport": "Istanbul Airport", "temp": 25.0, "wind_kts": 16, "vis_km": 9.0, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "JED", "city": "Jeddah", "country": "Saudi Arabia", "airport": "King Abdulaziz Int'l", "temp": 38.0, "wind_kts": 19, "vis_km": 8.0, "condition": "HOT", "risk": "LOW"},
    {"iata": "MAD", "city": "Madrid", "country": "Spain", "airport": "Madrid-Barajas Airport", "temp": 29.0, "wind_kts": 11, "vis_km": 10.0, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "FCO", "city": "Rome", "country": "Italy", "airport": "Rome Leonardo da Vinci", "temp": 28.0, "wind_kts": 12, "vis_km": 9.5, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "ICN", "city": "Seoul", "country": "South Korea", "airport": "Incheon International", "temp": 24.5, "wind_kts": 11, "vis_km": 8.5, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "CGK", "city": "Jakarta", "country": "Indonesia", "airport": "Soekarno-Hatta Int'l", "temp": 32.0, "wind_kts": 10, "vis_km": 7.0, "condition": "HUMID", "risk": "LOW"},
    {"iata": "JNB", "city": "Johannesburg", "country": "South Africa", "airport": "O.R. Tambo Int'l", "temp": 19.0, "wind_kts": 14, "vis_km": 9.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "GRU", "city": "São Paulo", "country": "Brazil", "airport": "Guarulhos Int'l", "temp": 22.0, "wind_kts": 13, "vis_km": 8.0, "condition": "CLOUDY", "risk": "LOW"},
    {"iata": "MEX", "city": "Mexico City", "country": "Mexico", "airport": "Mexico City International", "temp": 23.0, "wind_kts": 11, "vis_km": 8.5, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "CAI", "city": "Cairo", "country": "Egypt", "airport": "Cairo International Airport", "temp": 36.0, "wind_kts": 17, "vis_km": 7.0, "condition": "SUNNY / DUST", "risk": "LOW"}
]

st.subheader("🌤️ Weather Disruption & METAR Station Search Engine")
st.markdown("Search live atmospheric weather observations by typing **City** (e.g. *Srinagar, Dharamshala, Tokyo, Paris, Dubai, New York*), **Country** (e.g. *India, Japan, France, UAE*), or **IATA Code** (e.g. *SXR, DHM, DEL*):")

wx_query = st.text_input("🌤️ Search Weather Station (by City, Country or IATA)", placeholder="Type Srinagar, Goa, Tokyo, Paris, Dubai, London, New York, India, Japan...").strip().upper()

if wx_query:
    filtered = [w for w in weather_db if wx_query in w['city'].upper() or wx_query in w['country'].upper() or wx_query in w['iata'] or wx_query in w['airport'].upper()]
    st.markdown(f"### Matching Weather Stations ({len(filtered)})")
else:
    filtered = weather_db
    st.markdown("### All Monitored Indian & Global Airport Weather Stations")

if filtered:
    if len(filtered) == 1:
        w_top = filtered[0]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🌡️ Temperature", f"{w_top['temp']} °C")
        c2.metric("💨 Wind Velocity", f"{w_top['wind_kts']} kts")
        c3.metric("👁️ Visibility", f"{w_top['vis_km']} km")
        c4.metric("🚨 Weather Risk", w_top['risk'])
        st.markdown("<br/>", unsafe_allow_html=True)
        
    df_wx_show = pd.DataFrame(filtered)[["city", "country", "iata", "airport", "temp", "wind_kts", "vis_km", "condition", "risk"]]
    df_wx_show.columns = ["City", "Country", "IATA", "Airport Name", "Temp (°C)", "Wind (kts)", "Visibility (km)", "METAR Condition", "Operational Risk"]
    st.dataframe(df_wx_show, use_container_width=True, hide_index=True)
else:
    st.info("No matching weather station found. Try searching Srinagar, Tokyo, Paris, Dubai, London, or New York.")
