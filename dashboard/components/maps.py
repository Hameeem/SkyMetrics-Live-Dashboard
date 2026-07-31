import pydeck as pdk
import folium
import pandas as pd
from typing import List, Dict, Any

def render_pydeck_flight_map(flights: List[Dict[str, Any]], airports: List[Dict[str, Any]] = None):
    df_flights = pd.DataFrame(flights)

    if df_flights.empty:
        df_flights = pd.DataFrame([{
            "callsign": "BAW117", "latitude": 51.4700, "longitude": -0.4543,
            "altitude_m": 10000, "velocity_mps": 240, "origin_country": "United Kingdom",
            "status": "EN_ROUTE"
        }])

    # Color mapping based on flight status
    def get_color(status):
        if status == "DELAYED":
            return [239, 68, 68, 200]
        elif status == "ON_APPROACH":
            return [245, 158, 11, 200]
        return [56, 189, 248, 200]

    df_flights["color"] = df_flights["status"].apply(get_color)

    view_state = pdk.ViewState(
        latitude=20.0,
        longitude=10.0,
        zoom=1.5,
        pitch=40,
        bearing=0
    )

    layer_flights = pdk.Layer(
        "ScatterplotLayer",
        data=df_flights,
        get_position=["longitude", "latitude"],
        get_color="color",
        get_radius=120000,
        pickable=True,
        auto_highlight=True
    )

    deck = pdk.Deck(
        layers=[layer_flights],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={
            "html": "<b>Callsign:</b> {callsign}<br/>"
                    "<b>Country:</b> {origin_country}<br/>"
                    "<b>Altitude:</b> {altitude_m} m<br/>"
                    "<b>Speed:</b> {velocity_mps} m/s<br/>"
                    "<b>Status:</b> {status}",
            "style": {"backgroundColor": "#1e293b", "color": "white", "fontSize": "13px"}
        }
    )

    return deck

def create_folium_flight_map(flights: List[Dict[str, Any]], airports: List[Dict[str, Any]] = None):
    m = folium.Map(location=[25.0, 10.0], zoom_start=2, tiles="CartoDB dark_matter")

    # Add airports as blue circle markers
    if airports:
        for ap in airports[:20]:
            folium.CircleMarker(
                location=[ap["latitude"], ap["longitude"]],
                radius=5,
                popup=f"<b>Airport:</b> {ap['name']} ({ap['iata']})<br/><b>Country:</b> {ap['country']}",
                color="#3b82f6",
                fill=True,
                fill_color="#60a5fa",
                fill_opacity=0.8
            ).add_to(m)

    # Add aircraft markers
    for f in flights[:50]:
        color = "#10b981"
        if f.get("status") == "DELAYED":
            color = "#ef4444"
        elif f.get("status") == "ON_APPROACH":
            color = "#f59e0b"

        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 180px;">
            <h4 style="margin: 0 0 6px 0; color: #1e3a8a;">✈️ {f.get('callsign', 'N/A')}</h4>
            <b>Origin Country:</b> {f.get('origin_country', 'N/A')}<br/>
            <b>Route:</b> {f.get('origin_iata', '?')} ➔ {f.get('destination_iata', '?')}<br/>
            <b>Altitude:</b> {f.get('altitude_m', 0):,.0f} m<br/>
            <b>Velocity:</b> {f.get('velocity_mps', 0)} m/s<br/>
            <b>Status:</b> <span style="color:{color}; font-weight:bold;">{f.get('status', 'EN_ROUTE')}</span>
        </div>
        """

        folium.CircleMarker(
            location=[f["latitude"], f["longitude"]],
            radius=7,
            popup=popup_html,
            tooltip=f.get("callsign", "Aircraft"),
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9
        ).add_to(m)

    return m
