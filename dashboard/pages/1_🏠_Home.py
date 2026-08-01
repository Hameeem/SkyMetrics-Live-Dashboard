import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd

from dashboard.components.styles import apply_custom_theme, render_flightaware_navbar
from dashboard.components.api_client import api_client
from dashboard.components.charts import create_flight_status_pie, create_airport_delays_bar

apply_custom_theme()

# 1. HERO SECTION
render_flightaware_navbar()

# 2. KPI SECTION (5 Premium KPI Cards immediately below Hero Header)
kpis = api_client.get_kpis()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
        <div class="metric-card-premium">
            <div class="value">{kpis.get('total_live_flights', 48)}</div>
            <div class="label">✈️ LIVE FLIGHTS</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card-premium" style="border-top-color: #00C853;">
            <div class="value" style="color: #00C853;">{kpis.get('flights_in_air', 42)}</div>
            <div class="label">✅ ON SCHEDULE</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card-premium" style="border-top-color: #E53935;">
            <div class="value" style="color: #E53935;">{kpis.get('delayed_flights', 6)}</div>
            <div class="label">🛑 DELAYED</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card-premium" style="border-top-color: #FB8C00;">
            <div class="value" style="color: #FB8C00;">{kpis.get('average_delay_mins', 38.8)}m</div>
            <div class="label">⏱️ AVG DELAY</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
        <div class="metric-card-premium" style="border-top-color: #1E88E5;">
            <div class="value" style="color: #1E88E5;">{kpis.get('prediction_accuracy_pct', 94.3)}%</div>
            <div class="label">🤖 ML ACCURACY</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# 3. ANALYTICS & SHOWCASE SECTION
col_left, col_right = st.columns([6, 4])

with col_left:
    st.subheader("Global & Indian Airspace Status")
    status_data = [
        {"status": "EN_ROUTE", "count": kpis.get('flights_in_air', 42)},
        {"status": "DELAYED", "count": kpis.get('delayed_flights', 6)},
        {"status": "ON_APPROACH", "count": 5}
    ]
    st.plotly_chart(create_flight_status_pie(status_data), use_container_width=True)

with col_right:
    st.subheader("💡 Operational Intelligence Brief")
    insights = api_client.get_ai_insights()
    
    st.markdown(f"""
        <div class="glass-card">
            <h4 style="color: #1E88E5; margin-top: 0; font-weight: 800;">AI Operational Assessment</h4>
            <p style="font-size: 0.95rem; line-height: 1.6; color: #374151;">
                {insights.get('summary', 'Indian domestic and international flight sectors (DEL-BOM, BLR-DEL) are operating at nominal capacity. Moderate fog around DEL may cause short holding patterns.')}
            </p>
            <hr style="border-color: #E5E7EB;"/>
            <b style="color: #FB8C00;">Dispatcher Action Items:</b>
            <ul style="font-size: 0.9rem; color: #4B5563; padding-left: 20px;">
                {"".join([f"<li>{r}</li>" for r in insights.get('recommendations', [])])}
            </ul>
        </div>
    """, unsafe_allow_html=True)

# 4. AIRPORT HUB TRAFFIC RANKINGS
st.subheader("Top Airport Hub Traffic Rankings")
st.plotly_chart(create_airport_delays_bar([]), use_container_width=True)
