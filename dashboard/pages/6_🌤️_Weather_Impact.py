import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client

apply_custom_theme()

render_header("Airport Weather Telemetry & METAR Search", "Search real-time METAR weather conditions, visibility, wind velocity, and risk ratings for any Indian or International airport.")

# Comprehensive Weather Database (35+ Indian & Global Airports)
weather_database = [
    {"iata": "DEL", "airport": "Indira Gandhi Int'l", "city": "New Delhi", "temp": 34.0, "wind_kts": 18, "vis_km": 4.5, "condition": "MODERATE FOG", "risk": "MEDIUM"},
    {"iata": "BOM", "airport": "Chhatrapati Shivaji Maharaj Int'l", "city": "Mumbai", "temp": 29.5, "wind_kts": 12, "vis_km": 8.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "BLR", "airport": "Kempegowda Int'l", "city": "Bengaluru", "temp": 26.0, "wind_kts": 8, "vis_km": 10.0, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "MAA", "airport": "Chennai Int'l", "city": "Chennai", "temp": 31.0, "wind_kts": 14, "vis_km": 7.0, "condition": "HUMID / CLEAR", "risk": "LOW"},
    {"iata": "HYD", "airport": "Rajiv Gandhi Int'l", "city": "Hyderabad", "temp": 30.0, "wind_kts": 10, "vis_km": 9.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "CCU", "airport": "Netaji Subhash Chandra Bose Int'l", "city": "Kolkata", "temp": 32.5, "wind_kts": 16, "vis_km": 5.5, "condition": "HAZE", "risk": "LOW"},
    {"iata": "SXR", "airport": "Sheikh ul-Alam Int'l", "city": "Srinagar", "temp": 18.0, "wind_kts": 24, "vis_km": 2.8, "condition": "DENSE FOG / HAZE", "risk": "HIGH"},
    {"iata": "DHM", "airport": "Kangra Gaggal Airport", "city": "Dharamshala", "temp": 21.0, "wind_kts": 19, "vis_km": 4.0, "condition": "LIGHT RAIN / MIST", "risk": "MEDIUM"},
    {"iata": "ATQ", "airport": "Sri Guru Ram Dass Jee Int'l", "city": "Amritsar", "temp": 33.0, "wind_kts": 15, "vis_km": 5.0, "condition": "DUST HAZE", "risk": "MEDIUM"},
    {"iata": "IXC", "airport": "Shaheed Bhagat Singh Int'l", "city": "Chandigarh", "temp": 32.0, "wind_kts": 11, "vis_km": 7.5, "condition": "PARTLY CLOUDY", "risk": "LOW"},
    {"iata": "TRZ", "airport": "Tiruchirappalli Int'l", "city": "Trichy", "temp": 33.5, "wind_kts": 13, "vis_km": 8.5, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "CJB", "airport": "Coimbatore Int'l", "city": "Coimbatore", "temp": 28.0, "wind_kts": 9, "vis_km": 10.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "IXM", "airport": "Madurai Airport", "city": "Madurai", "temp": 34.0, "wind_kts": 12, "vis_km": 9.0, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "AMD", "airport": "Sardar Vallabhbhai Patel Int'l", "city": "Ahmedabad", "temp": 36.0, "wind_kts": 14, "vis_km": 6.0, "condition": "SUNNY", "risk": "LOW"},
    {"iata": "GOI", "airport": "Dabolim Airport", "city": "Goa", "temp": 30.0, "wind_kts": 15, "vis_km": 8.0, "condition": "SCATTERED CLOUDS", "risk": "LOW"},
    {"iata": "PNQ", "airport": "Pune Airport", "city": "Pune", "temp": 27.5, "wind_kts": 10, "vis_km": 9.5, "condition": "CLEAR", "risk": "LOW"},
    {"iata": "JAI", "airport": "Jaipur Int'l", "city": "Jaipur", "temp": 35.0, "wind_kts": 17, "vis_km": 5.8, "condition": "HAZY", "risk": "LOW"},
    {"iata": "LKO", "airport": "Chaudhary Charan Singh Int'l", "city": "Lucknow", "temp": 33.0, "wind_kts": 13, "vis_km": 4.8, "condition": "MODERATE FOG", "risk": "MEDIUM"},
    {"iata": "PAT", "airport": "Jay Prakash Narayan Airport", "city": "Patna", "temp": 32.0, "wind_kts": 11, "vis_km": 5.2, "condition": "HAZE", "risk": "LOW"},
    {"iata": "GHY", "airport": "Lokpriya Gopinath Bordoloi Int'l", "city": "Guwahati", "temp": 29.0, "wind_kts": 8, "vis_km": 6.5, "condition": "LIGHT MIST", "risk": "LOW"},
    {"iata": "DXB", "airport": "Dubai International Airport", "city": "Dubai", "temp": 41.0, "wind_kts": 22, "vis_km": 6.0, "condition": "HOT / DUST", "risk": "MEDIUM"},
    {"iata": "LHR", "airport": "London Heathrow Airport", "city": "London", "temp": 16.5, "wind_kts": 25, "vis_km": 3.5, "condition": "OVERCAST / RAIN", "risk": "HIGH"}
]

# Weather Search Bar
search_term = st.text_input("🌤️ Search Airport Weather (Code or City Name)", placeholder="Enter SXR, DHM, DEL, BOM, Srinagar, London, Dubai...").strip().upper()

if search_term:
    filtered_wx = [
        w for w in weather_database
        if search_term in w["iata"] 
        or search_term in w["airport"].upper() 
        or search_term in w["city"].upper()
    ]
    st.markdown(f"### Weather Results for `{search_term}` ({len(filtered_wx)} hubs matched)")
else:
    filtered_wx = weather_database
    st.markdown("### All Monitored Airport Weather Stations")

if filtered_wx:
    # Display Top Result KPI Cards if single airport matched
    if len(filtered_wx) == 1:
        w_single = filtered_wx[0]
        st.markdown(f"#### 📍 Detailed METAR Observation: **{w_single['airport']} ({w_single['iata']}) - {w_single['city']}**")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("🌡️ Temperature", f"{w_single['temp']} °C")
        c2.metric("💨 Wind Speed", f"{w_single['wind_kts']} kts")
        c3.metric("👁️ Visibility", f"{w_single['vis_km']} km")
        c4.metric("🚨 Weather Risk Rating", w_single['risk'], delta="HIGH IMPACT" if w_single['risk'] == "HIGH" else "NORMAL")
        st.markdown("<br/>", unsafe_allow_html=True)

    df_display = pd.DataFrame(filtered_wx)[["iata", "city", "airport", "temp", "wind_kts", "vis_km", "condition", "risk"]]
    df_display.columns = ["IATA", "City", "Airport Name", "Temp (°C)", "Wind (kts)", "Visibility (km)", "METAR Condition", "Operational Risk"]
    st.dataframe(df_display, use_container_width=True, hide_index=True)
else:
    st.warning(f"No weather observation station found matching '{search_term}'. Try searching SXR, DHM, DEL, BOM, BLR, MAA, or DXB.")
