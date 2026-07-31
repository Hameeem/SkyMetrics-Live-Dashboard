# SkyMetrics Technical Architecture & System Overview

SkyMetrics is built as a modular, enterprise-grade aviation intelligence and data processing platform.

```
                               ┌───────────────────────────────────────────┐
                               │      Streamlit Analytics Dashboard        │
                               │    (Multi-page, Dark Glassmorphism, UI)   │
                               └─────────────────────┬─────────────────────┘
                                                     │ HTTP / REST API
                                                     ▼
                               ┌───────────────────────────────────────────┐
                               │         FastAPI Backend Application       │
                               │  (JWT Auth, Router endpoints, CORS, Docs) │
                               └──────┬─────────────────────────────┬──────┘
                                      │                             │
                                      ▼                             ▼
                           ┌─────────────────────┐       ┌──────────────────────┐
                           │ ML Delay Predictor  │       │ SQLAlchemy DB Engine │
                           │ (XGBoost/SHAP/Joblib│       │(PostgreSQL / SQLite) │
                           └─────────────────────┘       └──────────┬───────────┘
                                                                    ▲
                                                                    │ ETL Ingestion
                               ┌────────────────────────────────────┴──────┐
                               │       ETL Pipelines & Data Engine         │
                               │  (Airflow DAGs + Standalone APScheduler)  │
                               │   OpenSky Network  │  OpenWeather API     │
                               └───────────────────────────────────────────┘
```

## System Components

### 1. Data Engineering & ETL Pipeline (`airflow/`, `scripts/`)
- Ingests real-time aircraft telemetry from OpenSky Network API and weather observations from OpenWeather API.
- Implements fallback simulation generators to guarantee zero-downtime execution even under API rate limits or network degradation.
- Stores execution statistics (records processed, execution latency, error messages) in the `etl_logs` data warehouse table.

### 2. Machine Learning Engine (`ml/`)
- Trained on historical flight telemetry, weather METAR metrics, distance, aircraft speed, altitude, and historical hub delay averages.
- Built using **XGBoost Classifier** (Delay Probability %) and **XGBoost Regressor** (Expected Delay Mins).
- Computes feature importances and SHAP values for operational explainability.

### 3. Backend API Service (`backend/`)
- Powered by **FastAPI** and **SQLAlchemy ORM**.
- Uses JWT authentication with password hashing (Bcrypt) and Role-Based Access Control (Admin, Analyst, Viewer).
- Implements structured OpenAPI / Swagger documentation at `/docs`.

### 4. Interactive Frontend Dashboard (`dashboard/`)
- Built with **Streamlit**, **Plotly**, **PyDeck**, **Folium**, and **AgGrid**.
- Configured with custom CSS glassmorphic dark enterprise theme.
- Capable of independent deployment to Streamlit Community Cloud with automatic API endpoint detection.
