import streamlit as st
import pandas as pd
from streamlit_folium import st_folium

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client
from dashboard.components.maps import create_folium_flight_map, render_pydeck_flight_map

apply_custom_theme()

render_header("Live Flight Tracking & Airspace Map", "Real-time aircraft positions, velocity vectors, altitude layers, and flight telematics.")

# Filter Bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    origin_filter = st.text_input("Origin IATA", placeholder="e.g. LHR").upper()
with col2:
    dest_filter = st.text_input("Destination IATA", placeholder="e.g. JFK").upper()
with col3:
    status_filter = st.selectbox("Flight Status", ["ALL", "EN_ROUTE", "ON_APPROACH", "DELAYED"])
with col4:
    map_engine = st.selectbox("Map Engine", ["PyDeck 3D", "Folium Interactive"])

params = {}
if origin_filter:
    params["origin"] = origin_filter
if dest_filter:
    params["destination"] = dest_filter
if status_filter != "ALL":
    params["status"] = status_filter

flights = api_client.get_live_flights(params)
airports = api_client.get_airports()

st.markdown(f"**Tracking {len(flights)} Active Aircraft in Airspace**")

# Render Map
if map_engine == "PyDeck 3D":
    st.pydeck_chart(render_pydeck_flight_map(flights, airports), use_container_width=True)
else:
    folium_map = create_folium_flight_map(flights, airports)
    st_folium(folium_map, width=1200, height=500)

st.markdown("<br/>", unsafe_allow_html=True)

# Telemetry Data Table
st.subheader("Live Telemetry Data Feed")
if flights:
    df_table = pd.DataFrame(flights)[["callsign", "origin_country", "origin_iata", "destination_iata", "latitude", "longitude", "altitude_m", "velocity_mps", "status"]]
    st.dataframe(df_table, use_container_width=True, hide_index=True)
else:
    st.info("No active flights matching selected filter criteria.")
