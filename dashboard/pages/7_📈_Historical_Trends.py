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

st.markdown("""
<style>
    div[data-testid="stMetricLabel"] *, label[data-testid="stWidgetLabel"] * {
        color: #0F172A !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

render_header("Historical Trends & Operational Analytics", "Multi-dimensional historical operational analytics, fleet distribution, scatter telemetry, and delay severity histograms.")

# Sample historical flight telemetry
flights_hist = pd.DataFrame([
    {"callsign": "AIC101", "airline": "Air India", "origin_iata": "DEL", "destination_iata": "BOM", "altitude_m": 10500, "velocity_mps": 240, "status": "EN_ROUTE"},
    {"callsign": "IGO505", "airline": "IndiGo", "origin_iata": "DEL", "destination_iata": "SXR", "altitude_m": 9800, "velocity_mps": 220, "status": "EN_ROUTE"},
    {"callsign": "VTI811", "airline": "Vistara", "origin_iata": "BOM", "destination_iata": "ATQ", "altitude_m": 11200, "velocity_mps": 250, "status": "EN_ROUTE"},
    {"callsign": "SEJ404", "airline": "SpiceJet", "origin_iata": "DEL", "destination_iata": "DHM", "altitude_m": 6500, "velocity_mps": 180, "status": "EN_ROUTE"},
    {"callsign": "AKJ202", "airline": "Akasa Air", "origin_iata": "BLR", "destination_iata": "MAA", "altitude_m": 7500, "velocity_mps": 210, "status": "EN_ROUTE"},
    {"callsign": "IGO612", "airline": "IndiGo", "origin_iata": "MAA", "destination_iata": "TRZ", "altitude_m": 5500, "velocity_mps": 190, "status": "EN_ROUTE"},
    {"callsign": "AIC441", "airline": "Air India", "origin_iata": "DEL", "destination_iata": "IXC", "altitude_m": 4800, "velocity_mps": 175, "status": "ON_APPROACH"},
    {"callsign": "SEJ711", "airline": "SpiceJet", "origin_iata": "MAA", "destination_iata": "CJB", "altitude_m": 6200, "velocity_mps": 195, "status": "EN_ROUTE"},
    {"callsign": "IGO309", "airline": "IndiGo", "origin_iata": "MAA", "destination_iata": "IXM", "altitude_m": 5800, "velocity_mps": 185, "status": "EN_ROUTE"},
    {"callsign": "AIC121", "airline": "Air India", "origin_iata": "DEL", "destination_iata": "LHR", "altitude_m": 11500, "velocity_mps": 260, "status": "DELAYED"}
])

c_h1, c_h2 = st.columns(2)

with c_h1:
    st.subheader("✈️ Indian Aviation Airline Market Share")
    fig_tree = go.Figure(go.Treemap(
        labels=["Domestic India", "Domestic & Int'l", "Full Service", "Low Cost", "Regional", "IndiGo", "Air India", "Vistara", "Akasa Air", "SpiceJet"],
        parents=["", "", "", "", "", "Domestic India", "Domestic & Int'l", "Full Service", "Low Cost", "Regional"],
        values=[340, 140, 70, 24, 38, 340, 140, 70, 24, 38],
        marker_colors=["#1E88E5", "#0284C7", "#38BDF8", "#0F172A", "#64748B"]
    ))
    fig_tree.update_layout(margin=dict(t=20, l=10, r=10, b=10), paper_bgcolor="#FFFFFF")
    st.plotly_chart(fig_tree, use_container_width=True)

with c_h2:
    st.subheader("⚡ Velocity vs Altitude Telemetry Distribution")
    fig_scat = go.Figure(data=go.Scatter(
        x=flights_hist["altitude_m"].tolist(),
        y=flights_hist["velocity_mps"].tolist(),
        mode='markers+text',
        text=flights_hist["callsign"].tolist(),
        textposition="top center",
        marker=dict(size=14, color='#1E88E5')
    ))
    fig_scat.update_layout(
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        xaxis=dict(title="Cruising Altitude (meters)", color="#0F172A"),
        yaxis=dict(title="Airspeed Velocity (m/s)", color="#0F172A"),
        font=dict(color="#0F172A")
    )
    st.plotly_chart(fig_scat, use_container_width=True)

st.markdown("<br/>", unsafe_allow_html=True)
c_h3, c_h4 = st.columns(2)

with c_h3:
    st.subheader("📈 Monthly Flight Operations Volume")
    fig_line = go.Figure(data=go.Bar(
        x=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
        y=[142.5, 138.2, 150.1, 154.8, 162.3, 168.0, 164.5],
        marker_color="#1E88E5"
    ))
    fig_line.update_layout(
        paper_bgcolor="#FFFFFF", 
        plot_bgcolor="#FFFFFF", 
        yaxis=dict(title="Flights (Thousands)", color="#0F172A"),
        xaxis=dict(color="#0F172A"),
        font=dict(color="#0F172A")
    )
    st.plotly_chart(fig_line, use_container_width=True)

with c_h4:
    st.subheader("📊 Annual Delay Severity Distribution")
    fig_bar = go.Figure(data=go.Bar(
        x=["On-Time (<15m)", "Minor (15-30m)", "Moderate (30-60m)", "Severe (>60m)"],
        y=[38400, 4200, 1850, 620],
        marker_color=["#1E88E5", "#0284C7", "#38BDF8", "#0F172A"]
    ))
    fig_bar.update_layout(
        showlegend=False, 
        paper_bgcolor="#FFFFFF", 
        plot_bgcolor="#FFFFFF", 
        yaxis=dict(title="Flight Count", color="#0F172A"),
        xaxis=dict(color="#0F172A"),
        font=dict(color="#0F172A")
    )
    st.plotly_chart(fig_bar, use_container_width=True)
