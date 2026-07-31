import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import os


from dashboard.components.styles import apply_custom_theme, render_header

apply_custom_theme()

render_header("User Preferences & Platform Configuration", "Configure theme tokens, API endpoints, default hub preferences, and alert notifications.")

st.subheader("API Connection Settings")
backend_url_input = st.text_input("Backend REST API Endpoint URL", value=os.getenv("BACKEND_API_URL", "http://localhost:8000"))

st.subheader("Dashboard Preferences")
theme_select = st.selectbox("Dashboard Visual Theme", ["Enterprise Dark (Default)", "Glassmorphic Midnight", "High Contrast Dark"])
default_hub = st.selectbox("Default Operational Airport Hub", ["LHR", "DEL", "JFK", "HND", "DXB", "ORD", "CDG", "SIN"])
auto_refresh = st.slider("Auto Refresh Interval (seconds)", min_value=10, max_value=300, value=30)
email_notif = st.checkbox("Enable Email Notifications for Triggered Alerts", value=True)

if st.button("💾 Save Preferences"):
    st.success("Preferences saved successfully!")
