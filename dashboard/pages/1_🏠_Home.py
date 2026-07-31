import streamlit as st
import pandas as pd

from dashboard.components.styles import apply_custom_theme, render_flightaware_navbar
from dashboard.components.api_client import api_client
from dashboard.components.charts import create_flight_status_pie, create_airport_delays_bar

apply_custom_theme()
render_flightaware_navbar()

st.markdown("""
<div style="background: linear-gradient(90deg, #001f44 0%, #003366 100%); padding: 18px 24px; border-radius: 8px; border-left: 5px solid #f59e0b; margin-bottom: 20px;">
    <h2 style="margin: 0; color: #ffffff; font-weight: 800;">FlightAware Operations Command Center</h2>
    <span style="color: #cbd5e1;">Real-time tracking metrics across Indian and global airspace sectors.</span>
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
            <div class="value" style="color: #22c55e;">{kpis.get('flights_in_air', 38)}</div>
            <div class="label">On-Schedule (Air)</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: #ef4444;">{kpis.get('delayed_flights', 7)}</div>
            <div class="label">Delayed Flights</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: #f59e0b;">{kpis.get('average_delay_mins', 24.5)}m</div>
            <div class="label">Avg Delay Mins</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="metric-card">
            <div class="value" style="color: #38bdf8;">{kpis.get('prediction_accuracy_pct', 94.3)}%</div>
            <div class="label">ML Model Accuracy</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Overview Visualizations & AI Briefing
col_left, col_right = st.columns([6, 4])

with col_left:
    st.subheader("Global & Indian Airspace Status")
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
            <h4 style="color: #38bdf8; margin-top: 0;">AI Operational Assessment</h4>
            <p style="font-size: 0.95rem; line-height: 1.5; color: #cbd5e1;">
                {insights.get('summary', 'Indian domestic and international flight corridors (DEL-BOM, BLR-DEL) are operating at nominal capacity. Fog and haze around DEL may cause short holding patterns.')}
            </p>
            <hr style="border-color: rgba(255, 255, 255, 0.1);"/>
            <b style="color: #f59e0b;">Dispatcher Action Items:</b>
            <ul style="font-size: 0.9rem; color: #94a3b8; padding-left: 20px;">
                {"".join([f"<li>{r}</li>" for r in insights.get('recommendations', [])])}
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Busiest Airport Chart
st.subheader("Top Airport Hub Traffic Rankings")
st.plotly_chart(create_airport_delays_bar([]), use_container_width=True)
