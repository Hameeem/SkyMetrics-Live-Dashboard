import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd

from dashboard.components.styles import apply_custom_theme, render_flightaware_navbar
from dashboard.components.api_client import api_client
from dashboard.components.charts import create_flight_status_pie, create_airport_delays_bar

apply_custom_theme()
render_flightaware_navbar()

st.markdown("""
<div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 20px 26px; border-radius: 12px; border-left: 6px solid #38bdf8; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.25);">
    <h2 style="margin: 0; color: #ffffff; font-weight: 800;">Flight Operations Command Center</h2>
    <span style="color: #e0f2fe; font-size: 1rem;">Real-time tracking metrics across Indian and global airspace sectors.</span>
</div>
""", unsafe_allow_html=True)

# Key Metric Cards Row
kpis = api_client.get_kpis()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="value">{kpis.get('total_live_flights', 45)}</div>
            <div class="label">Total Live Flights</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: #16a34a;">{kpis.get('flights_in_air', 38)}</div>
            <div class="label">On-Schedule (Air)</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: #dc2626;">{kpis.get('delayed_flights', 7)}</div>
            <div class="label">Delayed Flights</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: #d97706;">{kpis.get('average_delay_mins', 24.5)}m</div>
            <div class="label">Avg Delay Mins</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: #0284c7;">{kpis.get('prediction_accuracy_pct', 94.3)}%</div>
            <div class="label">ML Model Accuracy</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Embedded Airplane Showcase Image Banner
takeoff_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "airplane_takeoff.jpg")
if os.path.exists(takeoff_path):
    st.image(takeoff_path, caption="✈️ Live Telemetry Stream: Jet Departure at Indira Gandhi Int'l (DEL)", use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Overview Visualizations & AI Briefing
col_left, col_right = st.columns([6, 4])

with col_left:
    st.subheader("Global & Indian Airspace Operational Status")
    status_data = [
        {"status": "EN_ROUTE", "count": kpis.get('flights_in_air', 38)},
        {"status": "DELAYED", "count": kpis.get('delayed_flights', 7)},
        {"status": "ON_APPROACH", "count": 5}
    ]
    st.plotly_chart(create_flight_status_pie(status_data), use_container_width=True)

with col_right:
    st.subheader("💡 Operational Intelligence Brief")
    insights = api_client.get_ai_insights()
    
    st.markdown(f"""
        <div class="glass-card">
            <h4 style="color: #0284c7; margin-top: 0; font-weight: 800;">AI Operational Assessment</h4>
            <p style="font-size: 0.95rem; line-height: 1.6; color: #334155;">
                {insights.get('summary', 'Indian domestic and international flight corridors (DEL-BOM, BLR-DEL) are operating at nominal capacity. Fog and haze around DEL may cause short holding patterns.')}
            </p>
            <hr style="border-color: #e2e8f0;"/>
            <b style="color: #d97706;">Dispatcher Action Items:</b>
            <ul style="font-size: 0.9rem; color: #475569; padding-left: 20px;">
                {"".join([f"<li>{r}</li>" for r in insights.get('recommendations', [])])}
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Busiest Airport Chart
st.subheader("Top Airport Hub Traffic Rankings")
st.plotly_chart(create_airport_delays_bar([]), use_container_width=True)
