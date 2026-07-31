import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd


from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client
from dashboard.components.charts import create_airport_delays_bar

apply_custom_theme()

render_header("Airport Hub Performance & Congestion Analytics", "Comprehensive operational performance metrics, runway capacities, and hub traffic rankings.")

airports = api_client.get_airports()

st.subheader("Global Airport Metadata Warehouse")
if airports:
    df_ap = pd.DataFrame(airports)[["iata", "icao", "name", "city", "country", "latitude", "longitude", "altitude_ft", "runways_count"]]
    st.dataframe(df_ap, use_container_width=True, hide_index=True)

st.markdown("<br/>", unsafe_allow_html=True)

st.subheader("Airport Departure Traffic Ranking")
st.plotly_chart(create_airport_delays_bar([]), use_container_width=True)
