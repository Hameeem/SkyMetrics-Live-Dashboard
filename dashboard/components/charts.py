import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Any

PLOTLY_DARK_TEMPLATE = "plotly_dark"

def create_flight_status_pie(status_data: List[Dict[str, Any]]):
    df = pd.DataFrame(status_data)
    if df.empty:
        df = pd.DataFrame([{"status": "EN_ROUTE", "count": 35}, {"status": "ON_APPROACH", "count": 10}, {"status": "DELAYED", "count": 5}])

    fig = px.pie(
        df,
        values="count",
        names="status",
        title="Active Aircraft Operational Status",
        color_discrete_sequence=["#10b981", "#3b82f6", "#ef4444", "#f59e0b"],
        hole=0.4
    )
    fig.update_layout(template=PLOTLY_DARK_TEMPLATE, margin=dict(t=40, b=20, l=20, r=20))
    return fig

def create_airport_delays_bar(airport_data: List[Dict[str, Any]]):
    df = pd.DataFrame(airport_data)
    if df.empty:
        df = pd.DataFrame([
            {"airport": "LHR", "count": 45}, {"airport": "DEL", "count": 38},
            {"airport": "JFK", "count": 32}, {"airport": "DXB", "count": 29},
            {"airport": "ORD", "count": 25}
        ])

    fig = px.bar(
        df,
        x="airport",
        y="count",
        title="Top 10 Busiest Airport Hubs (Traffic Volume)",
        color="count",
        color_continuous_scale="Blues"
    )
    fig.update_layout(template=PLOTLY_DARK_TEMPLATE, margin=dict(t=40, b=20, l=20, r=20))
    return fig

def create_delay_probability_gauge(prob_pct: float, risk_level: str):
    color = "#10b981"
    if risk_level == "MEDIUM":
        color = "#f59e0b"
    elif risk_level == "HIGH":
        color = "#ef4444"
    elif risk_level == "CRITICAL":
        color = "#991b1b"

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_pct,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Delay Risk: {risk_level}", 'font': {'size': 20, 'color': "#ffffff"}},
        number={'suffix': "%", 'font': {'color': color, 'size': 36}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#ffffff"},
            'bar': {'color': color},
            'bgcolor': "rgba(30, 41, 59, 0.5)",
            'bordercolor': "rgba(255, 255, 255, 0.2)",
            'steps': [
                {'range': [0, 25], 'color': "rgba(16, 185, 129, 0.15)"},
                {'range': [25, 55], 'color': "rgba(245, 158, 11, 0.15)"},
                {'range': [55, 80], 'color': "rgba(239, 68, 68, 0.15)"},
                {'range': [80, 100], 'color': "rgba(153, 27, 27, 0.25)"}
            ]
        }
    ))
    fig.update_layout(template=PLOTLY_DARK_TEMPLATE, height=260, margin=dict(t=30, b=10, l=20, r=20))
    return fig

def create_feature_importance_chart(importances: Dict[str, float]):
    df = pd.DataFrame([{"feature": k.replace("_", " ").title(), "importance": v} for k, v in importances.items()])
    df = df.sort_values(by="importance", ascending=True)

    fig = px.bar(
        df,
        x="importance",
        y="feature",
        orientation="h",
        title="ML Feature Importance Ranking",
        color="importance",
        color_continuous_scale="Viridis"
    )
    fig.update_layout(template=PLOTLY_DARK_TEMPLATE, margin=dict(t=40, b=20, l=20, r=20))
    return fig

def create_weather_delay_heatmap():
    # Sample correlation heatmap between Wind, Visibility, Humidity and Delays
    corr_data = [
        [1.0, -0.68, 0.42, 0.76],
        [-0.68, 1.0, -0.35, -0.82],
        [0.42, -0.35, 1.0, 0.38],
        [0.76, -0.82, 0.38, 1.0]
    ]
    labels = ["Wind Speed", "Visibility", "Humidity", "Delay Risk"]

    fig = px.imshow(
        corr_data,
        x=labels,
        y=labels,
        color_continuous_scale="RdBu_r",
        title="Weather Factor Correlation Heatmap"
    )
    fig.update_layout(template=PLOTLY_DARK_TEMPLATE, margin=dict(t=40, b=20, l=20, r=20))
    return fig

def create_altitude_speed_scatter(flights: List[Dict[str, Any]]):
    df = pd.DataFrame(flights)
    if df.empty:
        return go.Figure()

    fig = px.scatter(
        df,
        x="velocity_mps",
        y="altitude_m",
        color="status",
        size="altitude_m",
        hover_name="callsign",
        hover_data=["origin_iata", "destination_iata", "origin_country"],
        title="Flight Telemetry: Speed (m/s) vs Altitude (m)",
        color_discrete_sequence=["#38bdf8", "#10b981", "#ef4444", "#f59e0b"]
    )
    fig.update_layout(template=PLOTLY_DARK_TEMPLATE, margin=dict(t=40, b=20, l=20, r=20))
    return fig

def create_airline_treemap():
    data = {
        "Region": ["Europe", "Europe", "Europe", "North America", "North America", "Asia-Pacific", "Asia-Pacific", "Middle East"],
        "Airline": ["British Airways", "Lufthansa", "Air France", "Delta Air Lines", "United Airlines", "Singapore Airlines", "Japan Airlines", "Emirates"],
        "FlightCount": [120, 110, 95, 210, 195, 150, 130, 240]
    }
    df = pd.DataFrame(data)
    fig = px.treemap(
        df,
        path=["Region", "Airline"],
        values="FlightCount",
        title="Global Fleet Volume Treemap",
        color="FlightCount",
        color_continuous_scale="Blues"
    )
    fig.update_layout(template=PLOTLY_DARK_TEMPLATE, margin=dict(t=40, b=20, l=20, r=20))
    return fig
