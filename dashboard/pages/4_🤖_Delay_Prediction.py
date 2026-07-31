import streamlit as st
import pandas as pd

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client
from dashboard.components.charts import create_delay_probability_gauge, create_feature_importance_chart

apply_custom_theme()

render_header("AI Flight Delay Prediction Engine", "Predict flight delay risk using XGBoost Machine Learning and SHAP explainability models.")

st.markdown("Configure flight parameters and atmospheric conditions below to run delay risk inference:")

col_f1, col_f2, col_f3 = st.columns(3)

with col_f1:
    flight_id = st.text_input("Flight Number / Callsign", value="AIC101")
    origin = st.text_input("Departure Airport (IATA)", value="DEL").upper()
    destination = st.text_input("Arrival Airport (IATA)", value="LHR").upper()
    distance = st.number_input("Distance (km)", value=6720.0, step=100.0)

with col_f2:
    wind_kts = st.slider("Wind Speed (knots)", min_value=0.0, max_value=60.0, value=24.0, step=1.0)
    vis_km = st.slider("Visibility (km)", min_value=0.1, max_value=10.0, value=3.5, step=0.5)
    temp_c = st.number_input("Temperature (°C)", value=34.0, step=1.0)
    humidity = st.slider("Humidity (%)", min_value=10.0, max_value=100.0, value=75.0)

with col_f3:
    hour_of_day = st.slider("Departure Hour (UTC)", min_value=0, max_value=23, value=8)
    day_of_week = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    is_holiday = st.checkbox("Holiday / Peak Season Flag", value=False)
    hist_delay_avg = st.number_input("Historical Airport Delay Avg (mins)", value=28.0)

if st.button("🚀 Execute Delay Risk Inference", use_container_width=True):
    dow_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}

    features = {
        "flight_identifier": flight_id,
        "origin_iata": origin,
        "destination_iata": destination,
        "distance_km": distance,
        "temp_c": temp_c,
        "wind_speed_kts": wind_kts,
        "visibility_km": vis_km,
        "humidity_pct": humidity,
        "pressure_hpa": 1013.25,
        "hour_of_day": hour_of_day,
        "day_of_week": dow_map[day_of_week],
        "is_holiday": 1 if is_holiday else 0,
        "aircraft_speed_mps": 240.0,
        "altitude_m": 10500.0,
        "historical_airport_delay_avg": hist_delay_avg
    }

    with st.spinner("Processing XGBoost ML Inference & SHAP Explainability..."):
        res = api_client.predict_delay(features)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.subheader("Prediction Results & Risk Assessment")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="value">{res.get('delay_probability_pct', 45.0)}%</div>
                <div class="label">Delay Probability</div>
            </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="value" style="color: #f59e0b;">{res.get('expected_delay_mins', 28.5)}m</div>
                <div class="label">Expected Delay</div>
            </div>
        """, unsafe_allow_html=True)

    with c3:
        risk = res.get('risk_level', 'MEDIUM')
        risk_color = "#ef4444" if risk in ["HIGH", "CRITICAL"] else "#f59e0b" if risk == "MEDIUM" else "#10b981"
        st.markdown(f"""
            <div class="metric-card">
                <div class="value" style="color: {risk_color};">{risk}</div>
                <div class="label">Risk Category</div>
            </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="value" style="color: #38bdf8;">{res.get('confidence_score', 0.91)}</div>
                <div class="label">Model Confidence</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    c_left, c_right = st.columns([5, 5])
    with c_left:
        st.plotly_chart(create_delay_probability_gauge(res.get('delay_probability_pct', 45.0), res.get('risk_level', 'MEDIUM')), use_container_width=True)

    with c_right:
        st.subheader("SHAP Feature Impact Breakdown")
        shap_dict = res.get("shap_contributions", {})
        if shap_dict:
            df_shap = pd.DataFrame([{"Feature": k.replace("_", " ").title(), "Impact (%)": v} for k, v in shap_dict.items()])
            st.dataframe(df_shap, use_container_width=True, hide_index=True)
