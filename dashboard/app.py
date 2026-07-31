import streamlit as st
import os

st.set_page_config(
    page_title="SkyMetrics | Enterprise Flight Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client

apply_custom_theme()

# Sidebar Navigation Header
st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <h2 style="color: #38bdf8; margin: 0; font-weight: 800; letter-spacing: 1px;">✈️ SKYMETRICS</h2>
        <span style="color: #9ca3af; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Enterprise Flight Intelligence</span>
    </div>
""", unsafe_allow_html=True)

# System Health Check Badge in Sidebar
health = api_client.check_health()
backend_status = health.get("status", "OFFLINE")
status_color = "#10b981" if backend_status == "HEALTHY" else "#f59e0b"

st.sidebar.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255, 255, 255, 0.1); padding: 10px 14px; border-radius: 8px; margin-bottom: 20px; font-size: 0.85rem;">
        <div><b>Backend API:</b> <span style="color:{status_color}; font-weight:bold;">{backend_status}</span></div>
        <div><b>ML Predictor:</b> <span style="color:#10b981;">ACTIVE</span></div>
        <div><b>Warehouse DB:</b> <span style="color:#10b981;">CONNECTED</span></div>
    </div>
""", unsafe_allow_html=True)

# Main Welcome Landing if executed directly
render_header(
    "SkyMetrics Enterprise Aviation Intelligence",
    "Real-time flight tracking, weather impact modeling, machine learning delay predictions, and automated ETL analytics."
)

st.markdown("""
### Welcome to SkyMetrics ✈️

Select a workspace module from the sidebar navigation:

- 🏠 **Home**: Executive KPIs, operational alert highlights, and platform overview.
- ✈️ **Live Tracking**: Real-time 3D world tracking map and live flight telemetry grid.
- 🔍 **Flight Search**: Search by callsign, flight number, ICAO, IATA, or airline.
- 🤖 **Delay Prediction**: Interactive ML delay risk prediction engine with SHAP feature breakdowns.
- 🏬 **Airport Analytics**: Congestion ranking, arrival/departure distribution, and hub analytics.
- 🌤️ **Weather Impact**: Airport weather METAR monitoring and delay correlation heatmaps.
- 📈 **Historical Trends**: Time-series delay trends, treemaps, and speed/altitude analytics.
- 💡 **AI Operational Insights**: Natural language operational summaries and risk assessments.
- 🚨 **Alerts Center**: Custom flight alert rule builder and trigger history.
- ⚙️ **Admin Operations**: User management, system health metrics, and ETL pipeline execution logs.
- 👤 **Settings**: Preference customization and API connection management.
""")
