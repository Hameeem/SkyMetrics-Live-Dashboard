import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client

apply_custom_theme()

# Explicit CSS label fix for Analysis page
st.markdown("""
<style>
    div[data-testid="stMetricLabel"] *, label[data-testid="stWidgetLabel"] * {
        color: #0F172A !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

render_header("Airport & Airline Operations Analysis Dashboard", "Filter live and historical operational analytics by Airport Hub, Time Horizon (Today, Week, Month, Year), Airline On-Time %, Takeoffs/Landings, and Route Density.")

# Top Controls: Airport Selector & Timeframe Filter
c_ctrl1, c_ctrl2 = st.columns([6, 4])

with c_ctrl1:
    selected_airport = st.selectbox(
        "📍 Select Airport Hub",
        [
            "ALL - All Indian Airspace Hubs",
            "DEL - Indira Gandhi Int'l (Delhi)",
            "BOM - Chhatrapati Shivaji Maharaj Int'l (Mumbai)",
            "BLR - Kempegowda Int'l (Bengaluru)",
            "MAA - Chennai Int'l (Chennai)",
            "HYD - Rajiv Gandhi Int'l (Hyderabad)",
            "CCU - Netaji Subhash Chandra Bose Int'l (Kolkata)",
            "SXR - Sheikh ul-Alam Int'l (Srinagar)",
            "DHM - Kangra Gaggal Airport (Dharamshala)",
            "ATQ - Sri Guru Ram Dass Jee Int'l (Amritsar)",
            "IXC - Shaheed Bhagat Singh Int'l (Chandigarh)",
            "TRZ - Tiruchirappalli Int'l (Trichy)"
        ]
    )

with c_ctrl2:
    timeframe = st.selectbox(
        "📅 Timeframe Horizon",
        ["Today (24 Hours)", "Past 7 Days (Week)", "Past 30 Days (Month)", "Past 365 Days (Year)"]
    )

st.markdown("<br/>", unsafe_allow_html=True)

# Dynamic Data Calculations based on Airport & Timeframe
mult = 1 if "Today" in timeframe else (7 if "Week" in timeframe else (30 if "Month" in timeframe else 365))
code = selected_airport.split(" - ")[0]

base_takeoffs = 142 if code == "DEL" else (98 if code == "BOM" else (75 if code == "BLR" else (28 if code == "SXR" else (14 if code == "DHM" else 420))))
takeoffs = base_takeoffs * mult
landings = int(base_takeoffs * 0.96) * mult
delayed = int(base_takeoffs * 0.12) * mult
ontime_rate = 88.5 if code == "BLR" else (87.2 if code == "DEL" else (84.1 if code == "SXR" else 86.4))

# Executive KPI Dashboard Row (Sky Blue, White & Black Theme)
k1, k2, k3, k4 = st.columns(4)

dates = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]

with k1:
    st.metric("🛫 Takeoffs / Departures", f"{takeoffs:,}", f"+{int(mult*4.2)} vs prev {timeframe.split()[1]}")
    fig_k1 = go.Figure(data=go.Scatter(x=dates, y=[base_takeoffs - 5, base_takeoffs + 8, base_takeoffs - 2, base_takeoffs + 12, base_takeoffs - 4, base_takeoffs + 6, base_takeoffs], mode='lines', line=dict(color="#1E88E5", width=3)))
    fig_k1.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    st.plotly_chart(fig_k1, use_container_width=True)

with k2:
    st.metric("🛬 Landings / Arrivals", f"{landings:,}", f"+{int(mult*3.8)} vs prev {timeframe.split()[1]}")
    fig_k2 = go.Figure(data=go.Scatter(x=dates, y=[base_takeoffs - 6, base_takeoffs + 5, base_takeoffs - 4, base_takeoffs + 10, base_takeoffs - 2, base_takeoffs + 4, base_takeoffs - 2], mode='lines', line=dict(color="#0284C7", width=3)))
    fig_k2.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    st.plotly_chart(fig_k2, use_container_width=True)

with k3:
    st.metric("🛑 Delayed Flights (>15m)", f"{delayed:,}", f"-{int(mult*1.1)} vs prev", delta_color="inverse")
    fig_k3 = go.Figure(data=go.Scatter(x=dates, y=[int(base_takeoffs*0.18), int(base_takeoffs*0.14), int(base_takeoffs*0.15), int(base_takeoffs*0.11), int(base_takeoffs*0.13), int(base_takeoffs*0.10), int(base_takeoffs*0.12)], mode='lines', line=dict(color="#0F172A", width=3)))
    fig_k3.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    st.plotly_chart(fig_k3, use_container_width=True)

with k4:
    st.metric("🎯 On-Time Arrival Rate", f"{ontime_rate:.1f}%", "+1.4% Target")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ontime_rate,
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "#0F172A"},
            'bar': {'color': "#1E88E5"},
            'steps': [
                {'range': [0, 75], 'color': "#F8FAFC"},
                {'range': [75, 85], 'color': "#E2E8F0"},
                {'range': [85, 100], 'color': "#BAE6FD"}
            ]
        }
    ))
    fig_gauge.update_layout(
        height=130, 
        margin=dict(l=10, r=10, t=10, b=10), 
        paper_bgcolor="#FFFFFF",
        font=dict(color="#0F172A", family="Plus Jakarta Sans")
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Row 2: Analytical Breakdown Tables & Geographic Sector Map
col_left, col_mid, col_right = st.columns([4, 3, 3])

with col_left:
    st.subheader("✈️ Airline On-Time Performance & Delays")
    st.markdown("On-time arrival rate % and average delay duration grouped by carrier:")
    
    df_airlines = pd.DataFrame([
        {"Airline": "IndiGo", "Total Flights": int(takeoffs*0.48), "On-Time %": "91.4%", "Avg Delay": "11.2 min", "Status": "OPTIMAL"},
        {"Airline": "Air India", "Total Flights": int(takeoffs*0.26), "On-Time %": "84.8%", "Avg Delay": "22.5 min", "Status": "NOMINAL"},
        {"Airline": "Vistara", "Total Flights": int(takeoffs*0.14), "On-Time %": "89.2%", "Avg Delay": "14.1 min", "Status": "GOOD"},
        {"Airline": "Akasa Air", "Total Flights": int(takeoffs*0.07), "On-Time %": "88.6%", "Avg Delay": "15.0 min", "Status": "GOOD"},
        {"Airline": "SpiceJet", "Total Flights": int(takeoffs*0.05), "On-Time %": "81.2%", "Avg Delay": "26.8 min", "Status": "ATTENTION"}
    ])
    st.dataframe(df_airlines, use_container_width=True, hide_index=True)

with col_mid:
    st.subheader("📍 Top Route Flight Traffic Share")
    st.markdown("Highest volume flight corridors from selected hub:")
    
    df_routes = pd.DataFrame([
        {"Route Corridor": f"{code if code != 'ALL' else 'DEL'} ➔ BOM (Mumbai)", "Daily Flights": int(takeoffs*0.22), "Share %": "22.0%"},
        {"Route Corridor": f"{code if code != 'ALL' else 'DEL'} ➔ BLR (Bengaluru)", "Daily Flights": int(takeoffs*0.18), "Share %": "18.0%"},
        {"Route Corridor": f"{code if code != 'ALL' else 'DEL'} ➔ SXR (Srinagar)", "Daily Flights": int(takeoffs*0.12), "Share %": "12.0%"},
        {"Route Corridor": f"{code if code != 'ALL' else 'DEL'} ➔ MAA (Chennai)", "Daily Flights": int(takeoffs*0.10), "Share %": "10.0%"},
        {"Route Corridor": f"{code if code != 'ALL' else 'DEL'} ➔ DHM (Dharamshala)", "Daily Flights": int(takeoffs*0.06), "Share %": "6.0%"}
    ])
    st.dataframe(df_routes, use_container_width=True, hide_index=True)

with col_right:
    st.subheader("🛰️ Hub Sector Airspace Map")
    m_hub = folium.Map(location=[22.0, 78.0], zoom_start=4, tiles="CartoDB positron")
    
    folium.Marker([28.5562, 77.1000], popup="Delhi DEL Hub", icon=folium.Icon(color="blue", icon="plane")).add_to(m_hub)
    folium.CircleMarker([33.9872, 74.7741], radius=7, color="#0F172A", fill=True, fill_color="#1E88E5", popup="Srinagar SXR Hub").add_to(m_hub)
    folium.CircleMarker([19.0896, 72.8656], radius=7, color="#0F172A", fill=True, fill_color="#0284C7", popup="Mumbai BOM Hub").add_to(m_hub)
    folium.CircleMarker([13.1986, 77.7066], radius=7, color="#0F172A", fill=True, fill_color="#38BDF8", popup="Bengaluru BLR Hub").add_to(m_hub)
    
    st_folium(m_hub, width=320, height=280)
