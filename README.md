# SkyMetrics – Enterprise Flight Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-2.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-FF4B4B.svg)](https://streamlit.io/)
[![XGBoost](https://img.shields.io/badge/XGBoost-ML%20Predictor-green.svg)](https://xgboost.readthedocs.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**SkyMetrics** is a production-ready, enterprise-grade aviation analytics platform. It ingests live aircraft position vectors, airport METAR weather reports, and global airport metadata, processes them through automated ETL pipelines, stores the records inside a PostgreSQL data warehouse, predicts flight delay risks using Machine Learning (XGBoost/SHAP), and visualizes real-time operational insights via an interactive Streamlit analytics dashboard.

---

## ✈️ System Architecture Overview

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

---

## 🚀 Key Features

- 🛰️ **Live Flight Tracking**: Interactive PyDeck 3D & Folium world maps displaying real-time aircraft positions, telemetry, velocity vectors, altitude layers, and flight status.
- 🤖 **Machine Learning Delay Predictor**: XGBoost model computing delay probability %, estimated delay minutes, risk categories, feature importances, and SHAP explainability breakdowns.
- 🌤️ **Weather Disruption Analytics**: Ingests airport temperature, wind speed, visibility, and humidity to correlate atmospheric conditions with delay risks.
- ⚡ **Automated ETL Pipelines**: Airflow DAGs and APScheduler background runners for 10-min flight updates, 15-min weather refreshes, hourly ML predictions, and nightly cleanup with full `etl_logs` auditing.
- 💡 **AI Operational Insights**: Pluggable natural language briefing layer generating operational diagnostics and dispatcher recommendations.
- 🔒 **Enterprise JWT Security**: Role-Based Access Control (`admin`, `analyst`, `viewer`), password hashing with Bcrypt, and audit logging.
- 🐳 **Dockerized Infrastructure**: Complete multi-container setup with FastAPI, Streamlit, PostgreSQL, Redis, and Nginx reverse proxy.

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Backend API** | FastAPI, SQLAlchemy ORM, Alembic, Pydantic, JWT Auth, Uvicorn |
| **Frontend Dashboard** | Streamlit, Plotly, PyDeck, Folium, Streamlit-AgGrid |
| **Data Engineering** | Apache Airflow, APScheduler, Pandas, NumPy |
| **Machine Learning** | XGBoost, Scikit-Learn, SHAP, Joblib |
| **Database** | PostgreSQL (Production) / SQLite (Local Zero-Config Fallback) |
| **DevOps & Cloud** | Docker, Docker Compose, Nginx, GitHub Actions CI/CD |

---

## ⚡ Quickstart Guide

### 1. Local Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/SkyMetrics.git
cd SkyMetrics

# Create and activate Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Seed database and train ML model artifact
python database/seed_data.py
python ml/train.py

# Launch FastAPI Backend (Terminal 1)
uvicorn backend.main:app --reload --port 8000

# Launch Streamlit Dashboard (Terminal 2)
streamlit run dashboard/app.py
```

Access the dashboard at `http://localhost:8501` and interactive Swagger docs at `http://localhost:8000/docs`.

---

## 🐳 Docker Deployment

```bash
# Build and start all services via Docker Compose
docker-compose up --build -d

# Check service status
docker-compose ps
```

---

## 🧪 Automated Testing

Execute the comprehensive test suite with coverage reporting:

```bash
pytest tests/ -v --cov=backend --cov=ml --cov=scripts
```

---

## 📡 API Endpoint Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register new user account |
| `POST` | `/api/v1/auth/login` | Authenticate user & return JWT token |
| `GET` | `/api/v1/flights/live` | Retrieve active live flight telemetry |
| `GET` | `/api/v1/flights/search` | Search flights by callsign, airport, or airline |
| `GET` | `/api/v1/airports` | Get global airport metadata |
| `POST` | `/api/v1/predictions/predict` | Run ML delay risk inference |
| `POST` | `/api/v1/predictions/retrain` | Retrain XGBoost delay prediction model |
| `GET` | `/api/v1/dashboard/kpis` | Get high-level operational KPIs |
| `GET` | `/api/v1/dashboard/ai-insights` | Get AI natural language summaries |
| `GET` | `/health` | System health check endpoint |

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
