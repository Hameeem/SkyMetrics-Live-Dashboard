import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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

render_header("Airport Hub & Runway Infrastructure Analytics", "Real-time runway capacity utilization, taxi times, terminal congestion metrics, peak hourly traffic flow, and airfield operational status across Indian and Global hubs.")

# Comprehensive Hub Infrastructure Database
hub_db = [
    {
        "iata": "DEL", "city": "New Delhi", "country": "India", "name": "Indira Gandhi Int'l", "display": "New Delhi, India - Indira Gandhi Int'l (DEL)",
        "runways": 4, "terminals": 3, "gates": 128, "apron_bays": 185, "ils_rating": "CAT III-B (All-Weather)",
        "daily_movements": 1420, "peak_hourly": 92, "taxi_out_min": 14.5, "taxi_in_min": 8.2, "sec_wait_min": 9.5, "baggage_min": 12.0, "utilization": 88.5
    },
    {
        "iata": "BOM", "city": "Mumbai", "country": "India", "name": "Chhatrapati Shivaji Maharaj Int'l", "display": "Mumbai, India - Chhatrapati Shivaji Maharaj Int'l (BOM)",
        "runways": 2, "terminals": 2, "gates": 84, "apron_bays": 120, "ils_rating": "CAT II",
        "daily_movements": 980, "peak_hourly": 52, "taxi_out_min": 18.2, "taxi_in_min": 11.0, "sec_wait_min": 14.0, "baggage_min": 16.5, "utilization": 94.2
    },
    {
        "iata": "BLR", "city": "Bengaluru", "country": "India", "name": "Kempegowda Int'l", "display": "Bengaluru, India - Kempegowda Int'l (BLR)",
        "runways": 2, "terminals": 2, "gates": 72, "apron_bays": 105, "ils_rating": "CAT III-B",
        "daily_movements": 750, "peak_hourly": 44, "taxi_out_min": 11.0, "taxi_in_min": 6.8, "sec_wait_min": 7.5, "baggage_min": 10.5, "utilization": 78.4
    },
    {
        "iata": "MAA", "city": "Chennai", "country": "India", "name": "Chennai Int'l", "display": "Chennai, India - Chennai Int'l (MAA)",
        "runways": 2, "terminals": 2, "gates": 48, "apron_bays": 78, "ils_rating": "CAT II",
        "daily_movements": 620, "peak_hourly": 38, "taxi_out_min": 13.0, "taxi_in_min": 7.5, "sec_wait_min": 11.0, "baggage_min": 14.0, "utilization": 82.1
    },
    {
        "iata": "HYD", "city": "Hyderabad", "country": "India", "name": "Rajiv Gandhi Int'l", "display": "Hyderabad, India - Rajiv Gandhi Int'l (HYD)",
        "runways": 2, "terminals": 1, "gates": 42, "apron_bays": 68, "ils_rating": "CAT I",
        "daily_movements": 540, "peak_hourly": 34, "taxi_out_min": 10.5, "taxi_in_min": 6.0, "sec_wait_min": 8.0, "baggage_min": 11.0, "utilization": 74.0
    },
    {
        "iata": "CCU", "city": "Kolkata", "country": "India", "name": "Netaji Subhash Chandra Bose Int'l", "display": "Kolkata, India - Netaji Subhash Chandra Bose Int'l (CCU)",
        "runways": 2, "terminals": 1, "gates": 38, "apron_bays": 62, "ils_rating": "CAT II",
        "daily_movements": 480, "peak_hourly": 30, "taxi_out_min": 12.5, "taxi_in_min": 7.2, "sec_wait_min": 10.0, "baggage_min": 13.5, "utilization": 76.5
    },
    {
        "iata": "SXR", "city": "Srinagar", "country": "India", "name": "Sheikh ul-Alam Int'l", "display": "Srinagar, India - Sheikh ul-Alam Int'l (SXR)",
        "runways": 1, "terminals": 1, "gates": 12, "apron_bays": 24, "ils_rating": "CAT I",
        "daily_movements": 280, "peak_hourly": 18, "taxi_out_min": 8.5, "taxi_in_min": 5.0, "sec_wait_min": 15.5, "baggage_min": 18.0, "utilization": 91.0
    },
    {
        "iata": "DHM", "city": "Dharamshala", "country": "India", "name": "Kangra Gaggal Airport", "display": "Dharamshala, India - Kangra Gaggal Airport (DHM)",
        "runways": 1, "terminals": 1, "gates": 4, "apron_bays": 8, "ils_rating": "Visual Approach Only",
        "daily_movements": 140, "peak_hourly": 10, "taxi_out_min": 6.0, "taxi_in_min": 4.0, "sec_wait_min": 6.5, "baggage_min": 9.0, "utilization": 65.0
    },
    {
        "iata": "DXB", "city": "Dubai", "country": "UAE", "name": "Dubai International", "display": "Dubai, UAE - Dubai International (DXB)",
        "runways": 2, "terminals": 3, "gates": 160, "apron_bays": 230, "ils_rating": "CAT III-B",
        "daily_movements": 1850, "peak_hourly": 110, "taxi_out_min": 16.0, "taxi_in_min": 9.5, "sec_wait_min": 6.0, "baggage_min": 9.5, "utilization": 96.5
    },
    {
        "iata": "LHR", "city": "London", "country": "UK", "name": "London Heathrow Airport", "display": "London, UK - London Heathrow (LHR)",
        "runways": 2, "terminals": 4, "gates": 135, "apron_bays": 210, "ils_rating": "CAT III-B",
        "daily_movements": 1600, "peak_hourly": 98, "taxi_out_min": 19.5, "taxi_in_min": 12.0, "sec_wait_min": 12.5, "baggage_min": 15.0, "utilization": 98.0
    }
]

# Search & Select Engine
st.markdown("### 🔍 Select Airport Hub for Infrastructure & Capacity Breakdown")
c1, c2 = st.columns([6, 4])

with c1:
    q_search = st.text_input("🔍 Search Airport Hub by City, Country, or Code", placeholder="Type Srinagar, Dharamshala, Delhi, Mumbai, Dubai, London...").strip().upper()

matching_hubs = [h["display"] for h in hub_db if not q_search or q_search in h["city"].upper() or q_search in h["country"].upper() or q_search in h["iata"] or q_search in h["name"].upper()]
if not matching_hubs:
    matching_hubs = [h["display"] for h in hub_db]

with c2:
    selected_hub_disp = st.selectbox("📍 Target Airport Hub", matching_hubs, index=0)

hub_obj = next((h for h in hub_db if h["display"] == selected_hub_disp), hub_db[0])

st.markdown("<br/>", unsafe_allow_html=True)

# Top KPI Metric Row
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🛤️ Active Runways", f"{hub_obj['runways']} Runways", f"{hub_obj['ils_rating']}")
k2.metric("🛫 Daily Movements", f"{hub_obj['daily_movements']:,}", f"Peak {hub_obj['peak_hourly']}/hr")
k3.metric("🛞 Avg Taxi-Out Time", f"{hub_obj['taxi_out_min']} mins", "-1.2 mins vs benchmark")
k4.metric("🛂 Security Wait Time", f"{hub_obj['sec_wait_min']} mins", "Optimal Flow")
k5.metric("⚡ Runway Utilization", f"{hub_obj['utilization']}%", "HIGH DENSITY" if hub_obj['utilization']>85 else "NOMINAL")

st.markdown("<br/>", unsafe_allow_html=True)
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("⏱️ Hourly Traffic Flight Movement Profile (UTC)")
    hours = [f"{h:02d}:00" for h in range(24)]
    base_m = hub_obj["peak_hourly"]
    movements_curve = [
        int(base_m*0.3), int(base_m*0.25), int(base_m*0.2), int(base_m*0.35), int(base_m*0.65), int(base_m*0.9),
        int(base_m*1.0), int(base_m*0.95), int(base_m*0.85), int(base_m*0.75), int(base_m*0.7), int(base_m*0.65),
        int(base_m*0.7), int(base_m*0.75), int(base_m*0.8), int(base_m*0.85), int(base_m*0.95), int(base_m*0.98),
        int(base_m*0.88), int(base_m*0.75), int(base_m*0.6), int(base_m*0.5), int(base_m*0.45), int(base_m*0.35)
    ]
    fig_hourly = go.Figure(data=[
        go.Bar(name="Departures", x=hours, y=[int(v*0.52) for v in movements_curve], marker_color="#1E88E5"),
        go.Bar(name="Arrivals", x=hours, y=[int(v*0.48) for v in movements_curve], marker_color="#0F172A")
    ])
    fig_hourly.update_layout(barmode='stack', paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color="#0F172A"), yaxis_title="Hourly Movements")
    st.plotly_chart(fig_hourly, use_container_width=True)

with col_chart2:
    st.subheader("📊 Terminal Ground Efficiency Benchmark (Minutes)")
    categories = ["Taxi-Out Time", "Taxi-In Time", "Security Queue", "Baggage First Belt"]
    values = [hub_obj["taxi_out_min"], hub_obj["taxi_in_min"], hub_obj["sec_wait_min"], hub_obj["baggage_min"]]
    fig_eff = go.Figure(data=[
        go.Bar(x=categories, y=values, marker_color=["#1E88E5", "#0284C7", "#38BDF8", "#0F172A"], text=[f"{v} min" for v in values], textposition="auto")
    ])
    fig_eff.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF", font=dict(color="#0F172A"), yaxis_title="Minutes")
    st.plotly_chart(fig_eff, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)
st.subheader("🛤️ Airfield & Runway Operational Status Board")

df_runways = pd.DataFrame([
    {"Runway ID": "RWY 28/10", "Heading": "280° / 100°", "Length": "4,430 meters", "Surface": "Asphalt", "ILS Rating": hub_obj['ils_rating'], "Status": "OPERATIONAL", "Wind Component": "12 kts Headwind"},
    {"Runway ID": "RWY 29L/11R", "Heading": "290° / 110°", "Length": "3,810 meters", "Surface": "Concrete", "ILS Rating": "CAT II", "Status": "OPERATIONAL", "Wind Component": "10 kts Headwind"},
    {"Runway ID": "RWY 27/09", "Heading": "270° / 090°", "Length": "3,800 meters", "Surface": "Asphalt", "ILS Rating": "CAT I", "Status": "STANDBY / ACTIVE", "Wind Component": "8 kts Crosswind"}
])
st.dataframe(df_runways, use_container_width=True, hide_index=True)
