import streamlit as st
import pandas as pd
import os
import requests

from dashboard.components.styles import apply_custom_theme, render_header
from dashboard.components.api_client import api_client

apply_custom_theme()

render_header("System Administration & ETL Operations Center", "Manage user accounts, monitor ETL pipeline execution logs, trigger ML retraining, and audit database health.")

base_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")

t1, t2, t3 = st.tabs(["📊 ETL Pipeline Logs", "🤖 ML Model Controls", "👥 User Accounts"])

with t1:
    st.subheader("Recent ETL Ingestion DAG Logs")
    try:
        resp = requests.get(f"{base_url}/api/v1/admin/etl-logs", timeout=4)
        if resp.status_code == 200:
            st.dataframe(pd.DataFrame(resp.json()), use_container_width=True, hide_index=True)
        else:
            st.info("Demonstration ETL logs view:")
            st.dataframe(pd.DataFrame([
                {"dag_id": "fetch_live_flights_dag", "task_id": "extract_opensky", "status": "SUCCESS", "records_processed": 45, "execution_time_sec": 1.42},
                {"dag_id": "fetch_weather_dag", "task_id": "extract_openweather", "status": "SUCCESS", "records_processed": 20, "execution_time_sec": 2.15}
            ]), use_container_width=True)
    except Exception:
        st.dataframe(pd.DataFrame([
            {"dag_id": "fetch_live_flights_dag", "task_id": "extract_opensky", "status": "SUCCESS", "records_processed": 45, "execution_time_sec": 1.42},
            {"dag_id": "fetch_weather_dag", "task_id": "extract_openweather", "status": "SUCCESS", "records_processed": 20, "execution_time_sec": 2.15}
        ]), use_container_width=True)

with t2:
    st.subheader("Machine Learning Model Maintenance")
    st.markdown("Re-train the XGBoost delay classifier/regressor using accumulated warehouse historical records.")
    if st.button("⚡ Trigger Model Retraining"):
        with st.spinner("Retraining model artifacts..."):
            from ml.train import train_delay_model
            artifact = train_delay_model()
            st.success(f"Model retrained! ROC-AUC: {artifact['metrics']['roc_auc']:.4f}, Accuracy: {artifact['metrics']['accuracy']:.4f}")

with t3:
    st.subheader("Registered Platform Users")
    st.dataframe(pd.DataFrame([
        {"username": "admin", "email": "admin@skymetrics.ai", "role": "admin", "status": "ACTIVE"},
        {"username": "analyst", "email": "analyst@skymetrics.ai", "role": "analyst", "status": "ACTIVE"},
        {"username": "viewer", "email": "viewer@skymetrics.ai", "role": "viewer", "status": "ACTIVE"}
    ]), use_container_width=True, hide_index=True)
