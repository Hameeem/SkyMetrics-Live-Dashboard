import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd

import requests
import os

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client

apply_custom_theme()

render_header("Global Aviation Flight Search", "Lookup live and historical flights by Callsign, Flight Number, ICAO24, IATA, or Airport.")

search_query = st.text_input("🔍 Search Query", placeholder="Enter callsign (e.g., BAW117), IATA (LHR), or airline (Emirates)...")

if search_query:
    base_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")
    try:
        resp = requests.get(f"{base_url}/api/v1/flights/search", params={"query": search_query}, timeout=4)
        if resp.status_code == 200:
            data = resp.json()
            live_list = data.get("live_flights", [])
            hist_list = data.get("historical_flights", [])

            st.markdown(f"### Results for `{search_query}`")

            col_a, col_b = st.columns(2)

            with col_a:
                st.subheader(f"Active Live Flights ({len(live_list)})")
                if live_list:
                    df_live = pd.DataFrame(live_list)[["callsign", "origin_country", "origin_iata", "destination_iata", "altitude_m", "status"]]
                    st.dataframe(df_live, use_container_width=True, hide_index=True)
                else:
                    st.info("No active live flights matched query.")

            with col_b:
                st.subheader(f"Historical Flight Records ({len(hist_list)})")
                if hist_list:
                    df_hist = pd.DataFrame(hist_list)[["flight_number", "airline", "origin_iata", "destination_iata", "delay_minutes", "is_delayed"]]
                    st.dataframe(df_hist, use_container_width=True, hide_index=True)
                else:
                    st.info("No historical records matched query.")
        else:
            st.error("Error executing search API query.")
    except Exception as e:
        st.warning("Offline search mode active.")
        flights = api_client.get_live_flights()
        filtered = [f for f in flights if search_query.upper() in f.get("callsign", "") or search_query.upper() in (f.get("origin_iata") or "")]
        st.dataframe(pd.DataFrame(filtered), use_container_width=True)
else:
    st.info("Type a callsign (e.g. BAW117), airport IATA (e.g. LHR, DEL, JFK), or flight number above to initiate search.")
