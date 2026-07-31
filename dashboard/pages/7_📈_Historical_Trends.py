import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd


from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.charts import create_airline_treemap, create_altitude_speed_scatter
from dashboard.components.api_client import api_client

apply_custom_theme()

render_header("Historical Operational Analytics & Fleet Trends", "Multi-dimensional historical delay distributions, airline rankings, treemaps, and telematics scatter analysis.")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Global Airline Fleet Distribution")
    st.plotly_chart(create_airline_treemap(), use_container_width=True)

with c2:
    st.subheader("Velocity vs Altitude Telemetry Distribution")
    flights = api_client.get_live_flights()
    st.plotly_chart(create_altitude_speed_scatter(flights), use_container_width=True)
