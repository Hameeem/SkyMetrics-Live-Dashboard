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
<div style="background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%); padding: 16px 24px; border-radius: 12px; border-left: 6px solid #38bdf8; margin-bottom: 20px; color:white; display:flex; justify-content:space-between; align-items:center;">
    <div>
        <h3 style="margin:0; color:#ffffff; font-weight:800;">🛰️ Live SkyMetrics Airplane Tracking Radar</h3>
        <span style="color:#e0f2fe; font-size:0.95rem;">Sharp vector tiles, rotated plane icons (✈️), and real-time operational status.</span>
    </div>
    <div style="background: #ffffff; color: #0284c7; font-weight: 800; padding: 6px 14px; border-radius: 20px; font-size: 0.82rem;">
        ● HIGH DEFINITION VECTOR RADAR
    </div>
</div>
""", unsafe_allow_html=True)

# Flight Status Color Legend Expander Card
with st.expander("🎨 Flight Status Color Legend & Map Guide (Click to expand)", expanded=True):
    col_l1, col_l2, col_l3, col_l4 = st.columns(4)
    with col_l1:
        st.markdown("""
            <div style="background:#ffffff; border:2px solid #86efac; padding:12px; border-radius:8px; text-align:center;">
                <span style="font-size:1.4rem;">✈️</span><br/>
                <b style="color:#15803d; font-size:0.95rem;">🟢 GREEN PLANE</b><br/>
                <span style="color:#475569; font-size:0.8rem;">On-Time (En Route)</span>
            </div>
        """, unsafe_allow_html=True)
    with col_l2:
        st.markdown("""
            <div style="background:#ffffff; border:2px solid #fde047; padding:12px; border-radius:8px; text-align:center;">
                <span style="font-size:1.4rem;">✈️</span><br/>
                <b style="color:#b45309; font-size:0.95rem;">🟡 YELLOW PLANE</b><br/>
                <span style="color:#475569; font-size:0.8rem;">On Approach / Holding</span>
            </div>
        """, unsafe_allow_html=True)
    with col_l3:
        st.markdown("""
            <div style="background:#ffffff; border:2px solid #fca5a5; padding:12px; border-radius:8px; text-align:center;">
                <span style="font-size:1.4rem;">✈️</span><br/>
                <b style="color:#b91c1c; font-size:0.95rem;">🔴 RED PLANE</b><br/>
                <span style="color:#475569; font-size:0.8rem;">Delayed (>15 mins)</span>
            </div>
        """, unsafe_allow_html=True)
    with col_l4:
        st.markdown("""
            <div style="background:#ffffff; border:2px solid #bae6fd; padding:12px; border-radius:8px; text-align:center;">
                <span style="font-size:1.4rem;">🔵</span><br/>
                <b style="color:#0369a1; font-size:0.95rem;">BLUE BADGES</b><br/>
                <span style="color:#475569; font-size:0.8rem;">Airports (DEL, BOM, etc.)</span>
            </div>
        """, unsafe_allow_html=True)

st.markdown("<br/>", unsafe_allow_html=True)

# Filter Bar
col1, col2, col3, col4 = st.columns(4)
with col1:
    origin_filter = st.text_input("Origin IATA", placeholder="e.g. DEL").upper()
with col2:
    dest_filter = st.text_input("Destination IATA", placeholder="e.g. BOM").upper()
with col3:
    status_filter = st.selectbox("Filter Status Category", ["ALL", "EN_ROUTE (🟢 On-Time)", "ON_APPROACH (🟡 Holding)", "DELAYED (🔴 Delayed)"])
with col4:
    map_engine = st.selectbox("Map Engine Mode", ["Vector Radar (Airplane Icons ✈️)", "PyDeck 3D Globe"])

params = {}
if origin_filter:
    params["origin"] = origin_filter
if dest_filter:
    params["destination"] = dest_filter

if "DELAYED" in status_filter:
    params["status"] = "DELAYED"
elif "ON_APPROACH" in status_filter:
    params["status"] = "ON_APPROACH"
elif "EN_ROUTE" in status_filter:
    params["status"] = "EN_ROUTE"

flights = api_client.get_live_flights(params)
airports = api_client.get_airports()

st.markdown(f"**Tracking {len(flights)} Active Flights in Airspace**")

# Render Map
if map_engine == "PyDeck 3D Globe":
    st.pydeck_chart(render_pydeck_flight_map(flights, airports), use_container_width=True)
else:
    folium_map = create_folium_flight_map(flights, airports)
    st_folium(folium_map, width=1200, height=540)

st.markdown("<br/>", unsafe_allow_html=True)

# Telemetry Data Table
st.subheader("Live Aircraft Telemetry Feed")
if flights:
    df_table = pd.DataFrame(flights)[["callsign", "origin_country", "origin_iata", "destination_iata", "latitude", "longitude", "altitude_m", "velocity_mps", "status"]]
    st.dataframe(df_table, use_container_width=True, hide_index=True)
else:
    st.info("No active flights matching selected filter criteria.")
