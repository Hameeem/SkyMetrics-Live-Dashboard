import pydeck as pdk
import folium
import pandas as pd
from typing import List, Dict, Any

def render_pydeck_flight_map(flights: List[Dict[str, Any]], airports: List[Dict[str, Any]] = None):
    df_flights = pd.DataFrame(flights)

    if df_flights.empty:
        df_flights = pd.DataFrame([{
            "callsign": "AIC101", "latitude": 28.5562, "longitude": 77.1000,
            "altitude_m": 10500, "velocity_mps": 240, "origin_country": "India",
            "status": "EN_ROUTE", "heading_deg": 190
        }])

    def get_color(status):
        if status == "DELAYED":
            return [239, 68, 68, 240] # Red
        elif status == "ON_APPROACH":
            return [245, 158, 11, 240] # Yellow
        return [16, 185, 129, 240] # Green (On-Time)

    df_flights["color"] = df_flights["status"].apply(get_color)

    view_state = pdk.ViewState(
        latitude=22.0,
        longitude=78.0,
        zoom=4.0,
        pitch=0,
        bearing=0
    )

    layer_flights = pdk.Layer(
        "ScatterplotLayer",
        data=df_flights,
        get_position=["longitude", "latitude"],
        get_color="color",
        get_radius=60000,
        pickable=True,
        auto_highlight=True,
        stroked=True,
        get_line_color=[255, 255, 255, 255],
        get_line_width=2000
    )

    deck = pdk.Deck(
        layers=[layer_flights],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/light-v10",
        tooltip={
            "html": "<div style='font-family: Arial, sans-serif; padding: 8px; background: #ffffff; color: #0f172a; border-radius: 6px; border: 2px solid #0284c7; box-shadow: 0 4px 12px rgba(0,0,0,0.15);'>"
                    "<b style='color:#0284c7; font-size:1.05rem;'>✈️ Callsign:</b> {callsign}<br/>"
                    "<b>Country:</b> {origin_country}<br/>"
                    "<b>Altitude:</b> {altitude_m} m | <b>Speed:</b> {velocity_mps} m/s<br/>"
                    "<b>Operational Status:</b> {status}</div>",
            "style": {"fontSize": "13px"}
        }
    )

    return deck

def create_folium_flight_map(flights: List[Dict[str, Any]], airports: List[Dict[str, Any]] = None):
    # Crisp high-contrast vector tiles
    m = folium.Map(location=[22.0, 78.0], zoom_start=4, tiles="CartoDB positron")

    # Add green circle markers with yellow IATA labels for airports
    if airports:
        for ap in airports[:30]:
            folium.CircleMarker(
                location=[ap["latitude"], ap["longitude"]],
                radius=5,
                popup=f"<b>Airport Hub:</b> {ap['name']} ({ap['iata']})<br/><b>Country:</b> {ap['country']}",
                color="#0284c7",
                fill=True,
                fill_color="#38bdf8",
                fill_opacity=0.95
            ).add_to(m)

            # High-resolution IATA Text Badge
            folium.map.Marker(
                [ap["latitude"] + 0.35, ap["longitude"] + 0.35],
                icon=folium.DivIcon(
                    html=f'<div style="font-size: 9pt; font-weight: 800; color: #0369a1; background: #ffffff; padding: 1px 5px; border-radius: 4px; border: 1px solid #38bdf8; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">{ap["iata"]}</div>'
                )
            ).add_to(m)

    # Add Airplane Icons (✈️) for aircraft markers with color coding
    for f in flights[:60]:
        status = f.get("status", "EN_ROUTE")
        
        # Color Legend Logic
        if status == "DELAYED":
            color = "#ef4444" # Red for Delayed
            status_text = "🔴 DELAYED (>15 mins)"
        elif status == "ON_APPROACH":
            color = "#f59e0b" # Yellow for Holding / Approach
            status_text = "🟡 ON APPROACH / HOLDING"
        else:
            color = "#10b981" # Green for On-Time En-Route
            status_text = "🟢 ON-TIME (EN ROUTE)"

        heading = f.get("heading_deg", 0)

        # Custom Airplane Icon Div (✈️)
        plane_html = f"""
        <div style="font-size: 16pt; color: {color}; transform: rotate({heading}deg); text-shadow: 0 0 4px #ffffff, 0 0 2px #000000; cursor: pointer;">
            ✈️
        </div>
        """

        popup_html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 200px; background:#ffffff; color:#0f172a; padding:10px; border-radius:8px; border: 2px solid #0284c7; box-shadow:0 4px 15px rgba(0,0,0,0.15);">
            <h4 style="margin: 0 0 6px 0; color: #0284c7;">✈️ {f.get('callsign', 'N/A')}</h4>
            <b>Country:</b> {f.get('origin_country', 'India')}<br/>
            <b>Route:</b> {f.get('origin_iata', 'DEL')} ➔ {f.get('destination_iata', 'BOM')}<br/>
            <b>Altitude:</b> {f.get('altitude_m', 0):,.0f} meters<br/>
            <b>Speed:</b> {f.get('velocity_mps', 0)} m/s<br/>
            <b>Status:</b> <span style="color:{color}; font-weight:800;">{status_text}</span>
        </div>
        """

        folium.map.Marker(
            [f["latitude"], f["longitude"]],
            icon=folium.DivIcon(html=plane_html),
            popup=popup_html,
            tooltip=f"{f.get('callsign', 'Aircraft')} ({status_text})"
        ).add_to(m)

    return m
