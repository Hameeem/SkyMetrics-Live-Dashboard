import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.getcwd())

import streamlit as st

st.set_page_config(
    page_title="SkyMetrics | Enterprise Flight Intelligence",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

from dashboard.components.styles import apply_custom_theme, render_flightaware_navbar
from dashboard.components.api_client import api_client

apply_custom_theme()

# Top Sky Blue Navigation Bar
render_flightaware_navbar()

# Sky Blue & White Hero Banner
st.markdown("""
<div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 24px 30px; border-radius: 12px; border: 2px solid #38bdf8; margin-bottom: 24px; color: white;">
    <h2 style="margin: 0 0 8px 0; color: #ffffff; font-weight: 800; font-size: 2rem;">Global Aviation Intelligence & Real-Time Tracking</h2>
    <span style="color: #e0f2fe; font-size: 1.05rem;">Live flight telemetry, weather METAR impact analysis, and machine learning delay risk predictions across India and global airspace.</span>
</div>
""", unsafe_allow_html=True)

# Hero Graphic Airplane Showcase Images
img_col1, img_col2 = st.columns(2)

takeoff_path = os.path.join(os.path.dirname(__file__), "assets", "airplane_takeoff.jpg")
landing_path = os.path.join(os.path.dirname(__file__), "assets", "airplane_landing.jpg")

with img_col1:
    if os.path.exists(takeoff_path):
        st.image(takeoff_path, caption="✈️ Live Telemetry: Jet Aircraft Takeoff at Golden Hour", use_container_width=True)

with img_col2:
    if os.path.exists(landing_path):
        st.image(landing_path, caption="🛬 Runway Operations: Airliner Final Approach & Touchdown", use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Sidebar Navigation Header
st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <h2 style="color: #ffffff; margin: 0; font-weight: 800; letter-spacing: 1px;">✈️ SKYMETRICS</h2>
        <span style="color: #bae6fd; font-size: 0.85rem; text-transform: uppercase; font-weight: 700; letter-spacing: 1px;">Sky Blue Edition</span>
    </div>
""", unsafe_allow_html=True)

# System Health Check Badge in Sidebar
health = api_client.check_health()
backend_status = health.get("status", "OFFLINE")
status_color = "#4ade80" if backend_status == "HEALTHY" else "#fde047"

st.sidebar.markdown(f"""
    <div style="background: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.3); padding: 12px 16px; border-radius: 8px; margin-bottom: 20px; font-size: 0.85rem; color: #ffffff;">
        <div><b>Backend API:</b> <span style="color:{status_color}; font-weight:bold;">{backend_status}</span></div>
        <div><b>ML Predictor:</b> <span style="color:#4ade80;">ACTIVE</span></div>
        <div><b>Data Warehouse:</b> <span style="color:#4ade80;">CONNECTED</span></div>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
### Explore SkyMetrics Modules:

Select a module from the sidebar navigation:

- 🏠 **Home**: Live operational summary, top hub rankings, and graphic flight showcases.
- ✈️ **Live Tracking**: 3D world tracking map with yellow airport badges & aircraft telemetry.
- 🔍 **Flight Search**: Search by Flight Number, Callsign (`AIC101`, `IGO505`), or Airport (`DEL`, `BOM`).
- 🤖 **Delay Prediction**: Interactive ML delay risk prediction engine with SHAP feature breakdowns.
- 🏬 **Airport Analytics**: Busiest hub traffic, runway distribution, and delay rankings.
- 🌤️ **Weather Impact**: Airport weather METAR monitoring and correlation heatmaps.
- 💡 **AI Insights**: Automated operational diagnostics & dispatcher recommendations.
- ⚙️ **Admin Operations**: User accounts, ETL pipeline execution logs, and ML model retraining.
""")
