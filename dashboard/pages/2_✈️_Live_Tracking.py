import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd

from streamlit_folium import st_folium

from dashboard.components.styles import apply_custom_theme, render_flightaware_navbar
from dashboard.components.api_client import api_client
from dashboard.components.maps import create_folium_flight_map, render_pydeck_flight_map

apply_custom_theme()
render_flightaware_navbar()

st.markdown("""
<div style="background: #001e44; padding: 12px 20px; border-radius: 8px; border-left: 4px solid #0284c7; margin-bottom: 15px; display:flex; justify-content:space-between; align-items:center;">
    <h3 style="margin:0; color:#ffffff;">🛰️ Live FlightAware World Tracking Radar</h3>
    <span style="color:#f59e0b; font-weight:bold; font-size:0.9rem;">● LIVE ADS-B TELEMETRY FEED</span>
</div>
""", unsafe_allow_html=True)

# Filter Bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    origin_filter = st.text_input("Origin IATA", placeholder="e.g. DEL").upper()
with col2:
    dest_filter = st.text_input("Destination IATA", placeholder="e.g. BOM").upper()
with col3:
    status_filter = st.selectbox("Flight Status", ["ALL", "EN_ROUTE", "ON_APPROACH", "DELAYED"])
with col4:
    map_engine = st.selectbox("Map Theme Engine", ["FlightAware Folium (Yellow Badges)", "PyDeck 3D Radar"])

params = {}
if origin_filter:
    params["origin"] = origin_filter
if dest_filter:
    params["destination"] = dest_filter
if status_filter != "ALL":
    params["status"] = status_filter

flights = api_client.get_live_flights(params)
airports = api_client.get_airports()

st.markdown(f"**Tracking {len(flights)} Active Flights in Airspace**")

# Render Map
if map_engine == "PyDeck 3D Radar":
    st.pydeck_chart(render_pydeck_flight_map(flights, airports), use_container_width=True)
else:
    folium_map = create_folium_flight_map(flights, airports)
    st_folium(folium_map, width=1200, height=520)

st.markdown("<br/>", unsafe_allow_html=True)

# Telemetry Data Table
st.subheader("Live Telemetry Stream")
if flights:
    df_table = pd.DataFrame(flights)[["callsign", "origin_country", "origin_iata", "destination_iata", "latitude", "longitude", "altitude_m", "velocity_mps", "status"]]
    st.dataframe(df_table, use_container_width=True, hide_index=True)
else:
    st.info("No active flights matching selected filter criteria.")
