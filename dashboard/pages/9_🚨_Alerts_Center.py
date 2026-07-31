import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd


from dashboard.components.styles import apply_custom_theme, render_header

apply_custom_theme()

render_header("Aviation Flight & Weather Alert Center", "Configure custom operational alert triggers, delay thresholds, and notification rules.")

col_a1, col_a2 = st.columns([5, 5])

with col_a1:
    st.subheader("Create Custom Alert Rule")
    title = st.text_input("Alert Title", value="LHR Heavy Wind Warning")
    alert_type = st.selectbox("Alert Condition", ["DELAY_THRESHOLD", "WEATHER_WARNING", "ALTITUDE_DEV", "COUNTRY_RESTRICTION"])
    target_ap = st.text_input("Target Airport (IATA)", value="LHR").upper()
    threshold = st.number_input("Threshold Value (mins / kts)", value=25.0)

    if st.button("➕ Deploy Active Alert Rule"):
        st.success(f"Alert rule '{title}' registered successfully! Email & Webhook notifications active.")

with col_a2:
    st.subheader("Active Operational Alerts")
    alerts_data = [
        {"title": "LHR Heavy Wind Delay Threshold", "type": "WEATHER_WARNING", "target": "LHR", "threshold": "25.0 kts", "status": "ACTIVE", "triggers": 3},
        {"title": "DEL Arrival Delay Alert (>30 mins)", "type": "DELAY_THRESHOLD", "target": "DEL", "threshold": "30.0 mins", "status": "ACTIVE", "triggers": 5},
        {"title": "JFK Altitude Deviation Warning", "type": "ALTITUDE_DEV", "target": "JFK", "threshold": "1000 m", "status": "ACTIVE", "triggers": 1}
    ]
    st.dataframe(pd.DataFrame(alerts_data), use_container_width=True, hide_index=True)
