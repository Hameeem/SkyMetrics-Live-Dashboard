import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd
import requests

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client

apply_custom_theme()

render_header("Global Aviation Flight & Airport Search", "Lookup live and historical flights by Callsign, Airport IATA (e.g. SXR, DEL, BOM), Flight Number, or City.")

search_query = st.text_input("🔍 Search Query", placeholder="Enter callsign (e.g. IGO505), airport (SXR, DEL, BOM, DHM, MAA), or city (Srinagar)...")

if search_query:
    q_str = search_query.strip().upper()
    
    # 1. Search Live Flights
    live_flights = api_client.get_live_flights({"query": q_str})
    if not live_flights:
        # Fallback local list match
        all_live = api_client.get_live_flights()
        live_flights = [
            f for f in all_live 
            if q_str in f.get("callsign", "").upper() 
            or q_str in (f.get("origin_iata") or "").upper() 
            or q_str in (f.get("destination_iata") or "").upper()
            or q_str in (f.get("origin_country") or "").upper()
        ]

    # 2. Search Airports
    matching_airports = api_client.get_airports(q_str)

    st.markdown(f"### Results for `{search_query}`")

    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader(f"Active Live Flights ({len(live_flights)})")
        if live_flights:
            df_live = pd.DataFrame(live_flights)[["callsign", "origin_country", "origin_iata", "destination_iata", "altitude_m", "velocity_mps", "status"]]
            st.dataframe(df_live, use_container_width=True, hide_index=True)
        else:
            st.info(f"No active live flights matched '{search_query}'.")

    with col_b:
        st.subheader(f"Matching Airport Hubs ({len(matching_airports)})")
        if matching_airports:
            df_ap = pd.DataFrame(matching_airports)[["iata", "name", "city", "country", "latitude", "longitude"]]
            st.dataframe(df_ap, use_container_width=True, hide_index=True)
        else:
            st.info(f"No airport hubs matched '{search_query}'.")
else:
    st.info("Type a callsign (e.g. IGO505), airport IATA (e.g. SXR, DEL, BOM, DHM, ATQ, TRZ), or city above to initiate search.")
