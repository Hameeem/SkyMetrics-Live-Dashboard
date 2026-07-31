import streamlit as st
import pandas as pd

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.charts import create_weather_delay_heatmap

apply_custom_theme()

render_header("Weather Disruption & Atmospheric Impact Analysis", "Real-time METAR weather telemetry, wind shears, visibility restrictions, and correlation heatmaps.")

st.subheader("Atmospheric Risk Correlation")
st.plotly_chart(create_weather_delay_heatmap(), use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)
st.subheader("Severe Weather Advisory Monitor")

st.markdown("""
<div class="glass-card">
    <h4 style="color: #ef4444; margin-top:0;">⚠️ High Wind & Low Visibility Warnings</h4>
    <table style="width:100%; text-align:left; color:#d1d5db;">
        <tr style="border-bottom:1px solid rgba(255,255,255,0.1);">
            <th>Airport</th><th>Condition</th><th>Wind (kts)</th><th>Visibility</th><th>Delay Impact</th>
        </tr>
        <tr>
            <td><b>DEL</b> (Indira Gandhi Int'l)</td><td>Heavy Fog & Haze</td><td>24.5 kts</td><td>1.2 km</td><td><span class="badge-delayed">+35 min avg delay</span></td>
        </tr>
        <tr>
            <td><b>LHR</b> (London Heathrow)</td><td>Crosswind Gusts</td><td>28.0 kts</td><td>8.5 km</td><td><span class="badge-approach">+18 min avg delay</span></td>
        </tr>
        <tr>
            <td><b>ORD</b> (Chicago O'Hare)</td><td>Thunderstorm Cell</td><td>32.1 kts</td><td>2.5 km</td><td><span class="badge-delayed">+42 min avg delay</span></td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)
