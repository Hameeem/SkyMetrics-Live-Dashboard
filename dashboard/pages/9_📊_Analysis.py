import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client

apply_custom_theme()

st.markdown("""
<style>
    div[data-testid="stMetricLabel"] *, label[data-testid="stWidgetLabel"] * {
        color: #0F172A !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

render_header("Airport & Airline Operations Analysis Dashboard", "Filter live operational analytics by Airport Hub, Time Horizon (Today, Week, Month, Year), Airline On-Time %, Takeoffs/Landings, and Side-by-Side Airport Comparison.")

# Complete Master Airport Database for Search & Comparison
all_airports_master = [
    {"iata": "ALL", "name": "ALL - All Indian Airspace Hubs", "city": "All Cities", "takeoffs": 420},
    {"iata": "DEL", "name": "DEL - Indira Gandhi Int'l (Delhi)", "city": "New Delhi", "takeoffs": 142},
    {"iata": "BOM", "name": "BOM - Chhatrapati Shivaji Maharaj Int'l (Mumbai)", "city": "Mumbai", "takeoffs": 98},
    {"iata": "BLR", "name": "BLR - Kempegowda Int'l (Bengaluru)", "city": "Bengaluru", "takeoffs": 75},
    {"iata": "MAA", "name": "MAA - Chennai Int'l (Chennai)", "city": "Chennai", "takeoffs": 62},
    {"iata": "HYD", "name": "HYD - Rajiv Gandhi Int'l (Hyderabad)", "city": "Hyderabad", "takeoffs": 54},
    {"iata": "CCU", "name": "CCU - Netaji Subhash Chandra Bose Int'l (Kolkata)", "city": "Kolkata", "takeoffs": 48},
    {"iata": "SXR", "name": "SXR - Sheikh ul-Alam Int'l (Srinagar)", "city": "Srinagar", "takeoffs": 28},
    {"iata": "DHM", "name": "DHM - Kangra Gaggal Airport (Dharamshala)", "city": "Dharamshala", "takeoffs": 14},
    {"iata": "ATQ", "name": "ATQ - Sri Guru Ram Dass Jee Int'l (Amritsar)", "city": "Amritsar", "takeoffs": 22},
    {"iata": "IXC", "name": "IXC - Shaheed Bhagat Singh Int'l (Chandigarh)", "city": "Chandigarh", "takeoffs": 25},
    {"iata": "TRZ", "name": "TRZ - Tiruchirappalli Int'l (Trichy)", "city": "Trichy", "takeoffs": 18},
    {"iata": "CJB", "name": "CJB - Coimbatore Int'l", "city": "Coimbatore", "takeoffs": 19},
    {"iata": "IXM", "name": "IXM - Madurai Airport", "city": "Madurai", "takeoffs": 16},
    {"iata": "AMD", "name": "AMD - Sardar Vallabhbhai Patel Int'l", "city": "Ahmedabad", "takeoffs": 42},
    {"iata": "GOI", "name": "GOI - Dabolim Airport", "city": "Goa", "takeoffs": 38},
    {"iata": "PNQ", "name": "PNQ - Pune Airport", "city": "Pune", "takeoffs": 35},
    {"iata": "COK", "name": "COK - Cochin Int'l", "city": "Kochi", "takeoffs": 40},
    {"iata": "GAU", "name": "GAU - Lokpriya Gopinath Bordoloi Int'l", "city": "Guwahati", "takeoffs": 26},
    {"iata": "PAT", "name": "PAT - Jayprakash Narayan Airport", "city": "Patna", "takeoffs": 24},
    {"iata": "JAI", "name": "JAI - Jaipur Int'l", "city": "Jaipur", "takeoffs": 30},
    {"iata": "VTZ", "name": "VTZ - Visakhapatnam Int'l", "city": "Visakhapatnam", "takeoffs": 21},
    {"iata": "BBI", "name": "BBI - Biju Patnaik Int'l", "city": "Bhubaneswar", "takeoffs": 23},
    {"iata": "LKO", "name": "LKO - Chaudhary Charan Singh Int'l", "city": "Lucknow", "takeoffs": 32},
    {"iata": "DXB", "name": "DXB - Dubai International Airport", "city": "Dubai", "takeoffs": 185},
    {"iata": "LHR", "name": "LHR - London Heathrow Airport", "city": "London", "takeoffs": 160},
    {"iata": "SIN", "name": "SIN - Singapore Changi Airport", "city": "Singapore", "takeoffs": 150},
    {"iata": "JFK", "name": "JFK - John F. Kennedy Int'l", "city": "New York", "takeoffs": 175}
]

# Airport Search Box & Filter System
st.markdown("### 🔍 Search & Filter Airport Analytics")
c_srch1, c_srch2, c_srch3 = st.columns([5, 4, 3])

with c_srch1:
    search_term = st.text_input("🔍 Search Airport (by Code, City, or Name)", placeholder="Type SXR, DHM, Delhi, Srinagar, Dubai, London...").strip().upper()

matching_airports = [ap["name"] for ap in all_airports_master if not search_term or search_term in ap["iata"] or search_term in ap["name"].upper() or search_term in ap["city"].upper()]

if not matching_airports:
    matching_airports = [ap["name"] for ap in all_airports_master]

with c_srch2:
    selected_primary = st.selectbox("📍 Select Primary Airport Hub", matching_airports, index=0)

with c_srch3:
    timeframe = st.selectbox("📅 Timeframe Horizon", ["Today (24 Hours)", "Past 7 Days (Week)", "Past 30 Days (Month)", "Past 365 Days (Year)"])

# Optional Side-by-Side Airport Comparison Toggle
st.markdown("---")
enable_compare = st.checkbox("⚔️ Enable Side-by-Side Airport Comparison")

if enable_compare:
    c_cmp1, c_cmp2 = st.columns(2)
    with c_cmp1:
        st.info(f"**Primary Target:** {selected_primary}")
    with c_cmp2:
        selected_secondary = st.selectbox("📍 Select Comparison Airport", [ap["name"] for ap in all_airports_master if ap["name"] != selected_primary], index=1)

st.markdown("<br/>", unsafe_allow_html=True)

# Helper function to get stats for an airport name
def get_ap_stats(ap_fullname, tf_name):
    mult = 1 if "Today" in tf_name else (7 if "Week" in tf_name else (30 if "Month" in tf_name else 365))
    ap_entry = next((ap for ap in all_airports_master if ap["name"] == ap_fullname), all_airports_master[0])
    code = ap_entry["iata"]
    base_t = ap_entry["takeoffs"]
    
    takeoffs = base_t * mult
    landings = int(base_t * 0.96) * mult
    delayed = int(base_t * 0.12) * mult
    ontime_rate = 88.5 if code == "BLR" else (87.2 if code == "DEL" else (84.1 if code == "SXR" else 86.4))
    
    return {
        "code": code,
        "name": ap_fullname,
        "takeoffs": takeoffs,
        "landings": landings,
        "delayed": delayed,
        "ontime_rate": ontime_rate,
        "base_t": base_t,
        "mult": mult
    }

p_stats = get_ap_stats(selected_primary, timeframe)

if not enable_compare:
    # Single Airport Analytics Overview
    k1, k2, k3, k4 = st.columns(4)
    dates = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    b_t = p_stats["base_t"]

    with k1:
        st.metric("🛫 Takeoffs / Departures", f"{p_stats['takeoffs']:,}", f"+{int(p_stats['mult']*4.2)} vs prev")
        fig_k1 = go.Figure(data=go.Scatter(x=dates, y=[b_t - 5, b_t + 8, b_t - 2, b_t + 12, b_t - 4, b_t + 6, b_t], mode='lines', line=dict(color="#1E88E5", width=3)))
        fig_k1.update_layout(margin=dict(l=5, r=5, t=5, b=5), paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig_k1, use_container_width=True)

    with k2:
        st.metric("🛬 Landings / Arrivals", f"{p_stats['landings']:,}", f"+{int(p_stats['mult']*3.8)} vs prev")
        fig_k2 = go.Figure(data=go.Scatter(x=dates, y=[b_t - 6, b_t + 5, b_t - 4, b_t + 10, b_t - 2, b_t + 4, b_t - 2], mode='lines', line=dict(color="#0284C7", width=3)))
        fig_k2.update_layout(margin=dict(l=5, r=5, t=5, b=5), paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig_k2, use_container_width=True)

    with k3:
        st.metric("🛑 Delayed Flights (>15m)", f"{p_stats['delayed']:,}", f"-{int(p_stats['mult']*1.1)} vs prev", delta_color="inverse")
        fig_k3 = go.Figure(data=go.Scatter(x=dates, y=[int(b_t*0.18), int(b_t*0.14), int(b_t*0.15), int(b_t*0.11), int(b_t*0.13), int(b_t*0.10), int(b_t*0.12)], mode='lines', line=dict(color="#0F172A", width=3)))
        fig_k3.update_layout(margin=dict(l=5, r=5, t=5, b=5), paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig_k3, use_container_width=True)

    with k4:
        st.metric("🎯 On-Time Arrival Rate", f"{p_stats['ontime_rate']:.1f}%", "+1.4% Target")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=p_stats['ontime_rate'],
            gauge={'axis': {'range': [0, 100], 'tickcolor': "#0F172A"}, 'bar': {'color': "#1E88E5"}, 'steps': [{'range': [0, 75], 'color': "#F8FAFC"}, {'range': [75, 85], 'color': "#E2E8F0"}, {'range': [85, 100], 'color': "#BAE6FD"}]}
        ))
        fig_gauge.update_layout(height=130, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor="#FFFFFF", font=dict(color="#0F172A"))
        st.plotly_chart(fig_gauge, use_container_width=True)

else:
    # Side-by-Side Comparison Layout
    s_stats = get_ap_stats(selected_secondary, timeframe)
    st.subheader(f"⚔️ Operational Comparison: {p_stats['code']} vs {s_stats['code']}")
    
    col_ap1, col_ap2 = st.columns(2)
    with col_ap1:
        st.markdown(f"### 📍 {p_stats['name']}")
        m1, m2 = st.columns(2)
        m1.metric("Departures", f"{p_stats['takeoffs']:,}")
        m2.metric("On-Time Rate", f"{p_stats['ontime_rate']:.1f}%")
        st.metric("Delays (>15m)", f"{p_stats['delayed']:,}")

    with col_ap2:
        st.markdown(f"### 📍 {s_stats['name']}")
        m3, m4 = st.columns(2)
        m3.metric("Departures", f"{s_stats['takeoffs']:,}")
        m4.metric("On-Time Rate", f"{s_stats['ontime_rate']:.1f}%")
        st.metric("Delays (>15m)", f"{s_stats['delayed']:,}")

    st.markdown("<br/>", unsafe_allow_html=True)
    st.subheader("📊 Comparative Departure Volume Bar Chart")
    fig_cmp_bar = go.Figure(data=[
        go.Bar(name=p_stats['code'], x=["Takeoffs", "Landings", "Delays"], y=[p_stats['takeoffs'], p_stats['landings'], p_stats['delayed']], marker_color="#1E88E5"),
        go.Bar(name=s_stats['code'], x=["Takeoffs", "Landings", "Delays"], y=[s_stats['takeoffs'], s_stats['landings'], s_stats['delayed']], marker_color="#0F172A")
    ])
    fig_cmp_bar.update_layout(barmode='group', paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color="#0F172A"))
    st.plotly_chart(fig_cmp_bar, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)
col_left, col_mid = st.columns([5, 5])

with col_left:
    st.subheader("✈️ Airline On-Time Performance & Delays")
    df_airlines = pd.DataFrame([
        {"Airline": "IndiGo", "Total Flights": int(p_stats['takeoffs']*0.48), "On-Time %": "91.4%", "Avg Delay": "11.2 min", "Status": "OPTIMAL"},
        {"Airline": "Air India", "Total Flights": int(p_stats['takeoffs']*0.26), "On-Time %": "84.8%", "Avg Delay": "22.5 min", "Status": "NOMINAL"},
        {"Airline": "Vistara", "Total Flights": int(p_stats['takeoffs']*0.14), "On-Time %": "89.2%", "Avg Delay": "14.1 min", "Status": "GOOD"},
        {"Airline": "Akasa Air", "Total Flights": int(p_stats['takeoffs']*0.07), "On-Time %": "88.6%", "Avg Delay": "15.0 min", "Status": "GOOD"},
        {"Airline": "SpiceJet", "Total Flights": int(p_stats['takeoffs']*0.05), "On-Time %": "81.2%", "Avg Delay": "26.8 min", "Status": "ATTENTION"}
    ])
    st.dataframe(df_airlines, use_container_width=True, hide_index=True)

with col_mid:
    st.subheader("📍 Top Route Flight Traffic Share")
    df_routes = pd.DataFrame([
        {"Route Corridor": f"{p_stats['code']} ➔ BOM (Mumbai)", "Daily Flights": int(p_stats['takeoffs']*0.22), "Share %": "22.0%"},
        {"Route Corridor": f"{p_stats['code']} ➔ BLR (Bengaluru)", "Daily Flights": int(p_stats['takeoffs']*0.18), "Share %": "18.0%"},
        {"Route Corridor": f"{p_stats['code']} ➔ SXR (Srinagar)", "Daily Flights": int(p_stats['takeoffs']*0.12), "Share %": "12.0%"},
        {"Route Corridor": f"{p_stats['code']} ➔ MAA (Chennai)", "Daily Flights": int(p_stats['takeoffs']*0.10), "Share %": "10.0%"},
        {"Route Corridor": f"{p_stats['code']} ➔ DHM (Dharamshala)", "Daily Flights": int(p_stats['takeoffs']*0.06), "Share %": "6.0%"}
    ])
    st.dataframe(df_routes, use_container_width=True, hide_index=True)
