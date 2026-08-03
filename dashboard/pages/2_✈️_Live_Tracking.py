import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.getcwd())

import streamlit as st
import pandas as pd
import json
import folium
import streamlit.components.v1 as components
from dashboard.components.styles import apply_custom_theme, render_header

apply_custom_theme()

st.markdown("""
<style>
    div[data-testid="stMetricLabel"] *, label[data-testid="stWidgetLabel"] * {
        color: #0F172A !important;
        font-weight: 800 !important;
    }
</style>
""", unsafe_allow_html=True)

render_header("Live Airspace Vector Tracking Radar", "Real-time animated flight tracking map with smooth airplane motion vectors across all-India airspace control sectors.")

st.subheader("🛰️ Animated Live Airplane Radar Map")
st.markdown("Planes actively fly across the screen in real-time along their flight vector heading. Hover cursor over any moving airplane (✈️) to inspect telemetry.")

# Sample Flights Data with Headings & Coordinates
flights_data = [
    {"callsign": "AIC101", "airline": "Air India", "origin_iata": "DEL", "destination_iata": "BOM", "lat": 24.50, "lon": 75.20, "altitude": 10500, "speed": 240, "status": "EN_ROUTE", "heading": 190},
    {"callsign": "IGO505", "airline": "IndiGo", "origin_iata": "DEL", "destination_iata": "SXR", "lat": 31.20, "lon": 75.80, "altitude": 9800, "speed": 220, "status": "EN_ROUTE", "heading": 340},
    {"callsign": "VTI811", "airline": "Vistara", "origin_iata": "BOM", "destination_iata": "ATQ", "lat": 24.50, "lon": 73.80, "altitude": 11200, "speed": 250, "status": "EN_ROUTE", "heading": 15},
    {"callsign": "SEJ404", "airline": "SpiceJet", "origin_iata": "DEL", "destination_iata": "DHM", "lat": 30.50, "lon": 76.50, "altitude": 6500, "speed": 180, "status": "EN_ROUTE", "heading": 20},
    {"callsign": "AKJ202", "airline": "Akasa Air", "origin_iata": "BLR", "destination_iata": "MAA", "lat": 13.00, "lon": 78.50, "altitude": 7500, "speed": 210, "status": "EN_ROUTE", "heading": 85},
    {"callsign": "IGO612", "airline": "IndiGo", "origin_iata": "MAA", "destination_iata": "TRZ", "lat": 11.80, "lon": 79.40, "altitude": 5500, "speed": 190, "status": "EN_ROUTE", "heading": 210},
    {"callsign": "AIC441", "airline": "Air India", "origin_iata": "DEL", "destination_iata": "IXC", "lat": 29.80, "lon": 76.90, "altitude": 4800, "speed": 175, "status": "ON_APPROACH", "heading": 350},
    {"callsign": "SEJ711", "airline": "SpiceJet", "origin_iata": "MAA", "destination_iata": "CJB", "lat": 12.00, "lon": 78.60, "altitude": 6200, "speed": 195, "status": "EN_ROUTE", "heading": 250},
    {"callsign": "IGO309", "airline": "IndiGo", "origin_iata": "MAA", "destination_iata": "IXM", "lat": 11.00, "lon": 79.00, "altitude": 5800, "speed": 185, "status": "EN_ROUTE", "heading": 200},
    {"callsign": "AIC121", "airline": "Air India", "origin_iata": "DEL", "destination_iata": "LHR", "lat": 35.00, "lon": 65.00, "altitude": 11500, "speed": 260, "status": "DELAYED", "heading": 290}
]

flights_json = json.dumps(flights_data)

# Generate Animated Leaflet Map HTML
map_html = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        #map {{ width: 100%; height: 560px; border-radius: 16px; border: 1px solid #E2E8F0; }}
        .plane-icon {{
            font-size: 20pt;
            transition: all 1.5s linear;
            cursor: pointer;
            text-shadow: 0 0 4px #ffffff, 0 0 2px #000000;
        }}
    </style>
</head>
<body style="margin:0; padding:0;">
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([22.0, 78.0], 5);
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            maxZoom: 19,
            attribution: '© OpenStreetMap © CARTO'
        }}).addTo(map);

        var flights = {flights_json};
        var markers = [];

        flights.forEach(function(f, idx) {{
            var color = f.status === 'EN_ROUTE' ? '#1E88E5' : (f.status === 'ON_APPROACH' ? '#0284C7' : '#0F172A');
            var iconHtml = '<div id="plane-' + idx + '" class="plane-icon" style="color:' + color + '; transform: rotate(' + f.heading + 'deg);">✈️</div>';
            
            var customIcon = L.divIcon({{
                html: iconHtml,
                className: '',
                iconSize: [30, 30],
                iconAnchor: [15, 15]
            }});

            var marker = L.marker([f.lat, f.lon], {{icon: customIcon}}).addTo(map);
            
            var tooltipText = f.callsign + " (" + f.airline + ") | " + f.origin_iata + " -> " + f.destination_iata + " | Alt: " + f.altitude + "m | Speed: " + f.speed + "m/s";
            marker.bindTooltip(tooltipText);

            var popupText = '<div style="font-family:sans-serif; padding:4px;"><b style="color:#1E88E5; font-size:1.1rem;">✈️ ' + f.callsign + '</b><br/><b>Airline:</b> ' + f.airline + '<br/><b>Route:</b> ' + f.origin_iata + ' ➔ ' + f.destination_iata + '<br/><b>Altitude:</b> ' + f.altitude + 'm<br/><b>Speed:</b> ' + f.speed + 'm/s<br/><b>Status:</b> ' + f.status + '</div>';
            marker.bindPopup(popupText);

            markers.push({{
                marker: marker,
                data: f,
                elementId: 'plane-' + idx
            }});
        }});

        // Smooth Continuous Real-Time Flight Motion Loop
        setInterval(function() {{
            markers.forEach(function(item) {{
                var f = item.data;
                var rad = f.heading * Math.PI / 180;
                var speedMult = 0.003;

                f.lat += speedMult * Math.cos(rad);
                f.lon += speedMult * Math.sin(rad);

                if (f.lat > 36 || f.lat < 8) f.heading = (f.heading + 180) % 360;
                if (f.lon > 92 || f.lon < 65) f.heading = (f.heading + 180) % 360;

                item.marker.setLatLng([f.lat, f.lon]);
                
                var el = document.getElementById(item.elementId);
                if (el) {{
                    el.style.transform = 'rotate(' + f.heading + 'deg)';
                }}
            }});
        }}, 1500);
    </script>
</body>
</html>
"""

components.html(map_html, height=580)

# Active Telemetry Table below map
df_f = pd.DataFrame(flights_data)[["callsign", "airline", "origin_iata", "destination_iata", "altitude", "speed", "status"]]
df_f.columns = ["Callsign", "Airline Company", "Origin", "Destination", "Altitude (m)", "Speed (m/s)", "Flight Status"]
st.dataframe(df_f, use_container_width=True, hide_index=True)
