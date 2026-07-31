import pydeck as pdk
import folium
import pandas as pd
from typing import List, Dict, Any

def render_pydeck_flight_map(flights: List[Dict[str, Any]], airports: List[Dict[str, Any]] = None):
    df_flights = pd.DataFrame(flights)

    if df_flights.empty:
        df_flights = pd.DataFrame([{
            "callsign": "AIC101", "latitude": 28.5562, "longitude": 77.1000,
            "altitude_m": 10000, "velocity_mps": 240, "origin_country": "India",
            "status": "EN_ROUTE"
        }])

    # FlightAware icon tan/orange color: [249, 115, 22, 230]
    def get_color(status):
        if status == "DELAYED":
            return [239, 68, 68, 230] # Red
        elif status == "ON_APPROACH":
            return [234, 179, 8, 230] # Yellow
        return [249, 115, 22, 230] # FlightAware Orange

    df_flights["color"] = df_flights["status"].apply(get_color)

    view_state = pdk.ViewState(
        latitude=22.0,
        longitude=78.0, # Center around South Asia / India
        zoom=3.8,
        pitch=30,
        bearing=0
    )

    layer_flights = pdk.Layer(
        "ScatterplotLayer",
        data=df_flights,
        get_position=["longitude", "latitude"],
        get_color="color",
        get_radius=80000,
        pickable=True,
        auto_highlight=True
    )

    deck = pdk.Deck(
        layers=[layer_flights],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip={
            "html": "<div style='font-family: Arial; padding: 6px;'>"
                    "<b style='color:#38bdf8;'>✈️ Callsign:</b> {callsign}<br/>"
                    "<b>Country:</b> {origin_country}<br/>"
                    "<b>Altitude:</b> {altitude_m} m | <b>Speed:</b> {velocity_mps} m/s<br/>"
                    "<b>Status:</b> {status}</div>",
            "style": {"backgroundColor": "#001430", "color": "white", "fontSize": "13px", "border": "1px solid #0284c7"}
        }
    )

    return deck

def create_folium_flight_map(flights: List[Dict[str, Any]], airports: List[Dict[str, Any]] = None):
    m = folium.Map(location=[22.0, 78.0], zoom_start=4, tiles="CartoDB dark_matter")

    # Add airports as green nodes with yellow IATA badge labels (FlightAware style!)
    if airports:
        for ap in airports[:25]:
            # Add airport green circle
            folium.CircleMarker(
                location=[ap["latitude"], ap["longitude"]],
                radius=6,
                popup=f"<b>Airport:</b> {ap['name']} ({ap['iata']})<br/><b>Country:</b> {ap['country']}",
                color="#22c55e",
                fill=True,
                fill_color="#4ade80",
                fill_opacity=0.9
            ).add_to(m)

            # Add yellow text label for IATA code
            folium.map.Marker(
                [ap["latitude"] + 0.3, ap["longitude"] + 0.3],
                icon=folium.DivIcon(
                    html=f'<div style="font-size: 10pt; font-weight: bold; color: #facc15; text-shadow: 1px 1px 2px black;">{ap["iata"]}</div>'
                )
            ).add_to(m)

    # Add FlightAware tan/orange aircraft markers
    for f in flights[:60]:
        color = "#f97316" # FlightAware orange/tan
        if f.get("status") == "DELAYED":
            color = "#ef4444"
        elif f.get("status") == "ON_APPROACH":
            color = "#eab308"

        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 190px; background:#001430; color:white; padding:8px; border-radius:6px;">
            <h4 style="margin: 0 0 6px 0; color: #38bdf8;">✈️ {f.get('callsign', 'N/A')}</h4>
            <b>Country:</b> {f.get('origin_country', 'India')}<br/>
            <b>Route:</b> {f.get('origin_iata', 'DEL')} ➔ {f.get('destination_iata', 'BOM')}<br/>
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
            fill_opacity=0.95
        ).add_to(m)

    return m
