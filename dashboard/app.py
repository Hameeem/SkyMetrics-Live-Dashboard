import streamlit as st
import os

st.set_page_config(
    page_title="FlightAware | SkyMetrics Aviation Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from dashboard.components.styles import apply_custom_theme, render_flightaware_navbar
from dashboard.components.api_client import api_client

apply_custom_theme()

# Render Top FlightAware Navigation Bar
render_flightaware_navbar()

# FlightAware Search Bar Header
st.markdown("""
<div style="background: #001e44; padding: 14px 20px; border-radius: 8px; border: 1px solid #0284c7; margin-bottom: 20px; text-align: center;">
    <h3 style="margin:0 0 8px 0; color:#ffffff; font-weight:700;">Global Flight & Airport Intelligence Tracking</h3>
    <span style="color:#94a3b8; font-size:0.9rem;">Track live aircraft telemetry, weather METAR reports, and AI delay predictions across India and global airspace.</span>
</div>
""", unsafe_allow_html=True)

# Sidebar Navigation Header
st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <h2 style="color: #38bdf8; margin: 0; font-weight: 800; letter-spacing: 1px;">✈️ SKYMETRICS</h2>
        <span style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">FlightAware Style Edition</span>
    </div>
""", unsafe_allow_html=True)

# System Health Check Badge in Sidebar
health = api_client.check_health()
backend_status = health.get("status", "OFFLINE")
status_color = "#22c55e" if backend_status == "HEALTHY" else "#f59e0b"

st.sidebar.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(56, 189, 248, 0.2); padding: 10px 14px; border-radius: 8px; margin-bottom: 20px; font-size: 0.85rem;">
        <div><b>Backend API:</b> <span style="color:{status_color}; font-weight:bold;">{backend_status}</span></div>
        <div><b>ML Predictor:</b> <span style="color:#22c55e;">ACTIVE</span></div>
        <div><b>Data Warehouse:</b> <span style="color:#22c55e;">CONNECTED</span></div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
### Explore SkyMetrics Modules:

Select a module from the sidebar navigation:

- 🏠 **Home**: Live operational overview, top hub metrics, and FlightAware tracking stats.
- ✈️ **Live Tracking**: FlightAware-style 3D world tracking map with yellow airport badges & tan aircraft icons.
- 🔍 **Flight Search**: Search by Flight Number, Callsign (e.g., `AIC101`, `IGO505`), or Airport (`DEL`, `BOM`).
- 🤖 **Delay Prediction**: Interactive ML delay risk prediction engine with SHAP feature breakdowns.
- 🏬 **Airport Analytics**: Busiest hub traffic, runway distribution, and delay rankings.
- 🌤️ **Weather Impact**: Airport weather METAR monitoring and correlation heatmaps.
- 💡 **AI Insights**: Automated operational diagnostics & dispatcher recommendations.
- ⚙️ **Admin Operations**: User accounts, ETL pipeline execution logs, and ML model retraining.
""")
