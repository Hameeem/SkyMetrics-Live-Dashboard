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

render_header("Weather Disruption & Atmospheric METAR Analytics", "Search real-time atmospheric observations, METAR phenomena, visibility, wind velocity, and operational weather risk for any airport hub worldwide.")

# Master Weather Database: All Indian Airports + Famous International Airports per Country
weather_db = [
    # --- INDIA ---
    {"iata": "DEL", "airport": "Indira Gandhi Int'l", "city": "New Delhi", "country": "India", "temp": 34.0, "wind_kts": 18, "vis_km": 4.5, "condition": "MODERATE FOG", "risk": "MEDIUM"},
    {"iata": "BOM", "airport": "Chhatrapati Shivaji Maharaj Int'l", "city": "Mumbai", "country": "India", "temp": 29.5, "wind_kts": 12, "vis_km": 8.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "BLR", "airport": "Kempegowda Int'l", "city": "Bengaluru", "country": "India", "temp": 26.0, "wind_kts": 8, "vis_km": 10.0, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "MAA", "airport": "Chennai Int'l", "city": "Chennai", "country": "India", "temp": 31.0, "wind_kts": 14, "vis_km": 7.0, "condition": "HUMID / CLEAR", "risk": "LOW"},
    {"iata": "HYD", "airport": "Rajiv Gandhi Int'l", "city": "Hyderabad", "country": "India", "temp": 30.0, "wind_kts": 10, "vis_km": 9.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "CCU", "airport": "Netaji Subhash Chandra Bose Int'l", "city": "Kolkata", "country": "India", "temp": 32.5, "wind_kts": 16, "vis_km": 5.5, "condition": "HAZE", "risk": "LOW"},
    {"iata": "SXR", "airport": "Sheikh ul-Alam Int'l", "city": "Srinagar", "country": "India", "temp": 18.0, "wind_kts": 24, "vis_km": 2.8, "condition": "DENSE FOG / HAZE", "risk": "HIGH"},
    {"iata": "DHM", "airport": "Kangra Gaggal Airport", "city": "Dharamshala", "country": "India", "temp": 21.0, "wind_kts": 19, "vis_km": 4.0, "condition": "LIGHT RAIN / MIST", "risk": "MEDIUM"},
    {"iata": "ATQ", "airport": "Sri Guru Ram Dass Jee Int'l", "city": "Amritsar", "country": "India", "temp": 33.0, "wind_kts": 15, "vis_km": 5.0, "condition": "DUST HAZE", "risk": "MEDIUM"},
    {"iata": "IXC", "airport": "Shaheed Bhagat Singh Int'l", "city": "Chandigarh", "country": "India", "temp": 32.0, "wind_kts": 11, "vis_km": 7.5, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "TRZ", "airport": "Tiruchirappalli Int'l", "city": "Trichy", "country": "India", "temp": 33.5, "wind_kts": 13, "vis_km": 8.5, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "CJB", "airport": "Coimbatore Int'l", "city": "Coimbatore", "country": "India", "temp": 28.0, "wind_kts": 9, "vis_km": 10.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "IXM", "airport": "Madurai Airport", "city": "Madurai", "country": "India", "temp": 34.0, "wind_kts": 12, "vis_km": 9.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "AMD", "airport": "Sardar Vallabhbhai Patel Int'l", "city": "Ahmedabad", "country": "India", "temp": 36.0, "wind_kts": 14, "vis_km": 6.0, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "GOI", "airport": "Dabolim Airport", "city": "Goa", "country": "India", "temp": 29.0, "wind_kts": 10, "vis_km": 9.5, "condition": "HUMID / CLEAR", "risk": "LOW"},
    {"iata": "GOX", "airport": "Manohar Int'l", "city": "Mopa Goa", "country": "India", "temp": 29.2, "wind_kts": 11, "vis_km": 9.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "PNQ", "airport": "Pune Airport", "city": "Pune", "country": "India", "temp": 28.5, "wind_kts": 9, "vis_km": 8.5, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "COK", "airport": "Cochin Int'l", "city": "Kochi", "country": "India", "temp": 30.0, "wind_kts": 13, "vis_km": 7.0, "condition": "LIGHT SHOWERS", "risk": "LOW"},
    {"iata": "TRV", "airport": "Trivandrum Int'l", "city": "Thiruvananthapuram", "country": "India", "temp": 30.5, "wind_kts": 12, "vis_km": 8.0, "condition": "HUMID", "risk": "LOW"},
    {"iata": "GAU", "airport": "Lokpriya Gopinath Bordoloi Int'l", "city": "Guwahati", "country": "India", "temp": 27.5, "wind_kts": 8, "vis_km": 6.5, "condition": "MIST", "risk": "LOW"},
    {"iata": "PAT", "airport": "Jayprakash Narayan Airport", "city": "Patna", "country": "India", "temp": 33.0, "wind_kts": 10, "vis_km": 5.0, "condition": "HAZE", "risk": "LOW"},
    {"iata": "JAI", "airport": "Jaipur Int'l", "city": "Jaipur", "country": "India", "temp": 35.0, "wind_kts": 16, "vis_km": 6.0, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "VTZ", "airport": "Visakhapatnam Int'l", "city": "Visakhapatnam", "country": "India", "temp": 31.5, "wind_kts": 15, "vis_km": 7.5, "condition": "BREEZY", "risk": "LOW"},
    {"iata": "BBI", "airport": "Biju Patnaik Int'l", "city": "Bhubaneswar", "country": "India", "temp": 32.0, "wind_kts": 11, "vis_km": 8.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "LKO", "airport": "Chaudhary Charan Singh Int'l", "city": "Lucknow", "country": "India", "temp": 33.5, "wind_kts": 12, "vis_km": 5.5, "condition": "HAZE", "risk": "LOW"},
    {"iata": "VNS", "airport": "Lal Bahadur Shastri Int'l", "city": "Varanasi", "country": "India", "temp": 34.0, "wind_kts": 9, "vis_km": 5.0, "condition": "HAZE", "risk": "LOW"},
    {"iata": "IXB", "airport": "Bagdogra Airport", "city": "Bagdogra", "country": "India", "temp": 25.0, "wind_kts": 7, "vis_km": 4.5, "condition": "LIGHT FOG", "risk": "MEDIUM"},
    {"iata": "IDR", "airport": "Devi Ahilya Bai Holkar Airport", "city": "Indore", "country": "India", "temp": 31.0, "wind_kts": 10, "vis_km": 8.5, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "LEH", "airport": "Kushok Bakula Rimpochee Airport", "city": "Leh", "country": "India", "temp": 12.0, "wind_kts": 26, "vis_km": 3.0, "condition": "HIGH WIND / FREEZING", "risk": "HIGH"},

    # --- FAMOUS INTERNATIONAL AIRPORTS ---
    {"iata": "DXB", "airport": "Dubai International Airport", "city": "Dubai", "country": "UAE", "temp": 41.0, "wind_kts": 22, "vis_km": 6.0, "condition": "HOT / DUST", "risk": "MEDIUM"},
    {"iata": "LHR", "airport": "London Heathrow Airport", "city": "London", "country": "UK", "temp": 16.5, "wind_kts": 25, "vis_km": 3.5, "condition": "OVERCAST / RAIN", "risk": "HIGH"},
    {"iata": "JFK", "airport": "John F. Kennedy Int'l", "city": "New York", "country": "USA", "temp": 24.0, "wind_kts": 16, "vis_km": 9.0, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "LAX", "airport": "Los Angeles International", "city": "Los Angeles", "country": "USA", "temp": 22.5, "wind_kts": 10, "vis_km": 10.0, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "SIN", "airport": "Singapore Changi Airport", "city": "Singapore", "country": "Singapore", "temp": 30.0, "wind_kts": 11, "vis_km": 8.5, "condition": "TROPICAL SHOWERS", "risk": "MEDIUM"},
    {"iata": "HND", "airport": "Tokyo Haneda Airport", "city": "Tokyo", "country": "Japan", "temp": 26.0, "wind_kts": 14, "vis_km": 9.5, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "CDG", "airport": "Paris Charles de Gaulle", "city": "Paris", "country": "France", "temp": 19.0, "wind_kts": 15, "vis_km": 7.0, "condition": "CLOUDY", "risk": "LOW"},
    {"iata": "FRA", "airport": "Frankfurt Airport", "city": "Frankfurt", "country": "Germany", "temp": 18.0, "wind_kts": 17, "vis_km": 8.0, "condition": "MILD RAIN", "risk": "LOW"},
    {"iata": "AMS", "airport": "Amsterdam Schiphol", "city": "Amsterdam", "country": "Netherlands", "temp": 17.0, "wind_kts": 21, "vis_km": 6.5, "condition": "BREEZY", "risk": "MEDIUM"},
    {"iata": "DOH", "airport": "Hamad International Airport", "city": "Doha", "country": "Qatar", "temp": 40.0, "wind_kts": 20, "vis_km": 7.0, "condition": "CLEAR / HOT", "risk": "LOW"},
    {"iata": "SYD", "airport": "Sydney Kingsford Smith", "city": "Sydney", "country": "Australia", "temp": 18.5, "wind_kts": 13, "vis_km": 10.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "YYZ", "airport": "Toronto Pearson Int'l", "city": "Toronto", "country": "Canada", "temp": 21.0, "wind_kts": 12, "vis_km": 9.0, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "BKK", "airport": "Suvarnabhumi Airport", "city": "Bangkok", "country": "Thailand", "temp": 33.0, "wind_kts": 10, "vis_km": 8.0, "condition": "HUMID", "risk": "LOW"},
    {"iata": "KUL", "airport": "Kuala Lumpur Int'l", "city": "Kuala Lumpur", "country": "Malaysia", "temp": 31.0, "wind_kts": 9, "vis_km": 8.5, "condition": "CLOUDY", "risk": "LOW"},
    {"iata": "PEK", "airport": "Beijing Capital Int'l", "city": "Beijing", "country": "China", "temp": 28.0, "wind_kts": 15, "vis_km": 5.0, "condition": "HAZE", "risk": "LOW"},
    {"iata": "HKG", "airport": "Hong Kong International", "city": "Hong Kong", "country": "Hong Kong", "temp": 30.5, "wind_kts": 18, "vis_km": 7.5, "condition": "HUMID", "risk": "LOW"},
    {"iata": "IST", "airport": "Istanbul Airport", "city": "Istanbul", "country": "Turkey", "temp": 25.0, "wind_kts": 16, "vis_km": 9.0, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "JED", "airport": "King Abdulaziz Int'l", "city": "Jeddah", "country": "Saudi Arabia", "temp": 38.0, "wind_kts": 19, "vis_km": 8.0, "condition": "HOT", "risk": "LOW"},
    {"iata": "MAD", "airport": "Madrid-Barajas Airport", "city": "Madrid", "country": "Spain", "temp": 29.0, "wind_kts": 11, "vis_km": 10.0, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "FCO", "airport": "Rome Leonardo da Vinci", "city": "Rome", "country": "Italy", "temp": 28.0, "wind_kts": 12, "vis_km": 9.5, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "ICN", "airport": "Incheon International", "city": "Seoul", "country": "South Korea", "temp": 24.5, "wind_kts": 11, "vis_km": 8.5, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "CGK", "airport": "Soekarno-Hatta Int'l", "city": "Jakarta", "country": "Indonesia", "temp": 32.0, "wind_kts": 10, "vis_km": 7.0, "condition": "HUMID", "risk": "LOW"},
    {"iata": "JNB", "airport": "O.R. Tambo Int'l", "city": "Johannesburg", "country": "South Africa", "temp": 19.0, "wind_kts": 14, "vis_km": 9.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "GRU", "airport": "São Paulo/Guarulhos Int'l", "city": "São Paulo", "country": "Brazil", "temp": 22.0, "wind_kts": 13, "vis_km": 8.0, "condition": "CLOUDY", "risk": "LOW"},
    {"iata": "MEX", "airport": "Mexico City International", "city": "Mexico City", "country": "Mexico", "temp": 23.0, "wind_kts": 11, "vis_km": 8.5, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "CAI", "airport": "Cairo International Airport", "city": "Cairo", "country": "Egypt", "temp": 36.0, "wind_kts": 17, "vis_km": 7.0, "condition": "SUNNY / DUST", "risk": "LOW"}
]

st.subheader("🌤️ Airport Weather Telemetry & METAR Search Engine")
st.markdown("Search live atmospheric weather observations, visibility, wind velocity, and operational risk for all Indian airports and famous international hubs.")

wx_q = st.text_input("🌤️ Search Weather Station (IATA Code, City, or Country)", placeholder="Type SXR, DHM, DEL, BOM, Srinagar, Goa, Tokyo, Dubai, London, New York...").strip().upper()

if wx_q:
    filtered = [w for w in weather_db if wx_q in w['iata'] or wx_q in w['airport'].upper() or wx_q in w['city'].upper() or wx_q in w['country'].upper()]
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
        
    df_wx_show = pd.DataFrame(filtered)[["iata", "city", "country", "airport", "temp", "wind_kts", "vis_km", "condition", "risk"]]
    df_wx_show.columns = ["IATA", "City", "Country", "Airport Name", "Temp (°C)", "Wind (kts)", "Visibility (km)", "METAR Condition", "Operational Risk"]
    st.dataframe(df_wx_show, use_container_width=True, hide_index=True)
else:
    st.info("No matching weather station found. Try searching SXR, DHM, DEL, BOM, BLR, MAA, GOI, or DXB.")
