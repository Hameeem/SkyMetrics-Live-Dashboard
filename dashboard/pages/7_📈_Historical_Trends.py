import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client

apply_custom_theme()

render_header("Historical Operational Analytics & Fleet Trends", "Multi-dimensional historical delay distributions, airline market share, operational timelines, and telemetry scatter analysis.")

# Fallback Historical Fleet & Traffic Datasets
fleet_data = pd.DataFrame([
    {"Airline": "IndiGo", "Fleet Size": 340, "Share %": 61.2, "Region": "Domestic India"},
    {"Airline": "Air India Group", "Fleet Size": 140, "Share %": 24.5, "Region": "Domestic & Int'l"},
    {"Airline": "Vistara", "Fleet Size": 70, "Share %": 8.8, "Region": "Full Service"},
    {"Airline": "Akasa Air", "Fleet Size": 24, "Share %": 4.1, "Region": "Low Cost"},
    {"Airline": "SpiceJet", "Fleet Size": 38, "Share %": 1.4, "Region": "Regional"}
])

monthly_traffic = pd.DataFrame([
    {"Month": "Jan", "Flights (Thousands)": 142.5, "On-Time %": 88.2},
    {"Month": "Feb", "Flights (Thousands)": 138.2, "On-Time %": 89.5},
    {"Month": "Mar", "Flights (Thousands)": 150.1, "On-Time %": 87.1},
    {"Month": "Apr", "Flights (Thousands)": 154.8, "On-Time %": 86.4},
    {"Month": "May", "Flights (Thousands)": 162.3, "On-Time %": 84.8},
    {"Month": "Jun", "Flights (Thousands)": 168.0, "On-Time %": 83.2},
    {"Month": "Jul", "Flights (Thousands)": 164.5, "On-Time %": 85.9}
])

telemetry_data = pd.DataFrame([
    {"Callsign": "AIC101", "Airline": "Air India", "Altitude_m": 10500, "Velocity_mps": 240, "Status": "ON-TIME"},
    {"Callsign": "IGO505", "Airline": "IndiGo", "Altitude_m": 9800, "Velocity_mps": 220, "Status": "ON-TIME"},
    {"Callsign": "VTI811", "Airline": "Vistara", "Altitude_m": 11200, "Velocity_mps": 250, "Status": "ON-TIME"},
    {"Callsign": "SEJ404", "Airline": "SpiceJet", "Altitude_m": 6500, "Velocity_mps": 180, "Status": "ON-TIME"},
    {"Callsign": "AKJ202", "Airline": "Akasa Air", "Altitude_m": 7500, "Velocity_mps": 210, "Status": "ON-TIME"},
    {"Callsign": "IGO612", "Airline": "IndiGo", "Altitude_m": 5500, "Velocity_mps": 190, "Status": "ON-TIME"},
    {"Callsign": "AIC441", "Airline": "Air India", "Altitude_m": 4800, "Velocity_mps": 175, "Status": "ON APPROACH"},
    {"Callsign": "AIC121", "Airline": "Air India", "Altitude_m": 11500, "Velocity_mps": 260, "Status": "DELAYED"}
])

# Attempt live data fetch with safe fallback
try:
    live_flights = api_client.get_live_flights()
    if live_flights and len(live_flights) > 0:
        df_live = pd.DataFrame(live_flights)
        if "altitude_m" in df_live.columns and "velocity_mps" in df_live.columns:
            telemetry_data = df_live
except Exception:
    pass

c1, c2 = st.columns(2)

with c1:
    st.subheader("✈️ Indian Aviation Airline Market Share")
    fig_tree = px.treemap(
        fleet_data, 
        path=["Region", "Airline"], 
        values="Fleet Size", 
        color="Share %",
        color_continuous_scale="Blues",
        title="Fleet Market Share Distribution by Airline Carrier"
    )
    fig_tree.update_layout(margin=dict(t=30, l=10, r=10, b=10))
    st.plotly_chart(fig_tree, use_container_width=True)

with c2:
    st.subheader("⚡ Velocity vs Altitude Telemetry Distribution")
    fig_scat = px.scatter(
        telemetry_data,
        x="Altitude_m" if "Altitude_m" in telemetry_data.columns else "altitude_m",
        y="Velocity_mps" if "Velocity_mps" in telemetry_data.columns else "velocity_mps",
        color="Status" if "Status" in telemetry_data.columns else "status",
        hover_name="Callsign" if "Callsign" in telemetry_data.columns else "callsign",
        size_max=15,
        color_discrete_map={"ON-TIME": "#00C853", "ON APPROACH": "#FB8C00", "DELAYED": "#E53935", "EN_ROUTE": "#00C853"},
        title="Airspeed (m/s) vs Cruising Altitude (m)"
    )
    fig_scat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_scat, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)
c3, c4 = st.columns(2)

with c3:
    st.subheader("📈 Monthly Flight Volume Timeline")
    fig_line = px.bar(
        monthly_traffic,
        x="Month",
        y="Flights (Thousands)",
        text="Flights (Thousands)",
        color="On-Time %",
        color_continuous_scale="Viridis",
        title="Monthly Operations (Thousands of Flights)"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with c4:
    st.subheader("📊 Historical Delay Duration Breakdown")
    delay_dist = pd.DataFrame([
        {"Category": "On-Time (<15m)", "Count": 38400, "Color": "#00C853"},
        {"Category": "Minor Delay (15-30m)", "Count": 4200, "Color": "#FB8C00"},
        {"Category": "Moderate Delay (30-60m)", "Count": 1850, "Color": "#FF7043"},
        {"Category": "Severe Delay (>60m)", "Count": 620, "Color": "#E53935"}
    ])
    fig_bar = px.bar(
        delay_dist,
        x="Category",
        y="Count",
        color="Category",
        color_discrete_sequence=["#00C853", "#FB8C00", "#FF7043", "#E53935"],
        title="Annual Delay Severity Count"
    )
    fig_bar.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_bar, use_container_width=True)
