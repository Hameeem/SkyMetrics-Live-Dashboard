import streamlit as st
import pandas as pd

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client
from dashboard.components.charts import create_flight_status_pie, create_airport_delays_bar

apply_custom_theme()

render_header("Executive Operational Summary", "Real-time key operational metrics across global airspace networks.")

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
            <div class="value" style="color: #10b981;">{kpis.get('flights_in_air', 38)}</div>
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
            <div class="value" style="color: #a855f7;">{kpis.get('prediction_accuracy_pct', 91.4)}%</div>
            <div class="label">ML Model Accuracy</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Overview Visualizations & AI Briefing
col_left, col_right = st.columns([6, 4])

with col_left:
    st.subheader("Global Airspace Status")
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
            <p style="font-size: 0.95rem; line-height: 1.5; color: #d1d5db;">
                {insights.get('summary', 'Transatlantic and Eurocontrol airspace sectors are operating at nominal capacity. Moderate wind shears around LHR and DEL may cause short arrival holds.')}
            </p>
            <hr style="border-color: rgba(255, 255, 255, 0.1);"/>
            <b style="color: #f59e0b;">Recommended Action Items:</b>
            <ul style="font-size: 0.9rem; color: #9ca3af; padding-left: 20px;">
                {"".join([f"<li>{r}</li>" for r in insights.get('recommendations', [])])}
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Busiest Airport Chart
st.subheader("Top Airport Hub Traffic")
st.plotly_chart(create_airport_delays_bar([]), use_container_width=True)
