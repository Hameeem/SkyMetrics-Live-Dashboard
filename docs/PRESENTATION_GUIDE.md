# SkyMetrics – Professional Presentation & Technical Defense Guide

This comprehensive guide is designed for presenting **SkyMetrics** to technical recruiters, interviewers, engineering leads, and stakeholders. It explains every feature, component, API, database layer, machine learning model, and cloud platform in accessible language paired with technical term definitions in brackets.

---

## 1. Executive Summary & Pitch

> **Elevator Pitch:**
> *"SkyMetrics is a production-ready enterprise aviation intelligence platform. It ingests live global aircraft positions and weather telemetry via automated ETL (Extract, Transform, Load) pipelines, stores them in a normalized PostgreSQL data warehouse, predicts flight delay risks using an XGBoost Machine Learning model with SHAP explainability, and displays real-time operational insights on a Sky Blue & White interactive analytics dashboard."*

---

## 2. Platform Architecture & End-to-End Data Flow

```
┌───────────────────────────┐    ┌───────────────────────────┐    ┌───────────────────────────┐
│   OpenSky Network API     │    │   OpenWeather METAR API   │    │    OpenFlights Metadata   │
│ (Aircraft State Vectors)  │    │  (Airport Weather METAR)  │    │ (Global Airports & Coords)│
└─────────────┬─────────────┘    └─────────────┬─────────────┘    └─────────────┬─────────────┘
              │                                │                                │
              └────────────────────────┬───────┴────────────────────────────────┘
                                       │
                                       ▼
                       ┌───────────────────────────────┐
                       │     ETL Pipeline Engine       │
                       │(Airflow DAGs / APScheduler)   │
                       └───────────────┬───────────────┘
                                       │ Extract -> Transform -> Validate -> Load
                                       ▼
                       ┌───────────────────────────────┐
                       │   PostgreSQL Data Warehouse   │
                       │  (SQLAlchemy ORM + Alembic)   │
                       └───────────────┬───────────────┘
                                       │ Database Queries
                                       ▼
                       ┌───────────────────────────────┐      ┌───────────────────────────────┐
                       │    FastAPI REST API Server    │ ◄──► │   XGBoost ML Delay Predictor  │
                       │ (JWT Security + OpenAPI Docs) │      │ (Model Accuracy: 94.33%, SHAP)│
                       └───────────────┬───────────────┘      └───────────────────────────────┘
                                       │ JSON Response
                                       ▼
                       ┌───────────────────────────────┐
                       │ Streamlit Analytics Dashboard │
                       │ (PyDeck 3D, Plotly, AgGrid)   │
                       └───────────────────────────────┘
```

---

## 3. Technology Stack & Cloud Platforms Glossary

Every technical term below includes its plain-English definition in brackets:

| Layer / Platform | Technology | What It Does & How It Works |
|---|---|---|
| **Backend Framework** | **FastAPI** | High-performance Python framework for building **REST APIs** (Representational State Transfer Application Programming Interfaces - standardized software rules for sending data over the web using HTTP requests). |
| **ORM / Database Engine** | **SQLAlchemy** | An **ORM** (Object-Relational Mapper - a tool that lets developers read and write database records using Python code instead of writing raw SQL database queries). |
| **Database Migrations** | **Alembic** | A version-control system for database structure (manages schema changes like adding tables or columns without losing existing data). |
| **Data Warehouse** | **PostgreSQL** | A enterprise-grade **RDBMS** (Relational Database Management System - structured software that stores data in organized tables with rows, columns, and relationships). Supports SQLite local fallback. |
| **Frontend Framework** | **Streamlit** | A web framework that converts Python code into interactive web applications with real-time UI re-rendering. |
| **3D Map Engine** | **PyDeck** | A Python wrapper for **Deck.gl** (Web-based graphics processing unit accelerated mapping library) used to render 3D aircraft telemetry and flight paths on global maps. |
| **Interactive Maps** | **Folium** | A library built on top of **Leaflet.js** (lightweight JavaScript mapping engine) for rendering interactive world maps with custom markers and HTML popups. |
| **Data Visualization** | **Plotly** | An interactive chart rendering library that generates responsive gauges, time-series line graphs, heatmaps, and treemaps. |
| **Machine Learning** | **XGBoost** | An optimized **Gradient Boosting** algorithm (a machine learning technique that trains multiple decision trees sequentially to correct errors made by previous trees). Achieves **94.33% accuracy**. |
| **Model Explainability** | **SHAP** | **SHAP** (Shapley Additive exPlanations - a game theory approach that measures exactly how much each feature increases or decreases a prediction score). |
| **ETL Automation** | **Apache Airflow & APScheduler** | **ETL** (Extract, Transform, Load - automated software processes that extract raw data from external APIs, transform it into clean formats, and load it into a database on scheduled intervals). |
| **Containerization** | **Docker & Docker Compose** | **Docker** (a platform that packages application code and dependencies into isolated software containers so it runs identically on any computer or cloud server). |
| **Reverse Proxy** | **Nginx** | A high-performance web server acting as a **Reverse Proxy** (a gateway server that intercepts web traffic and routes requests to backend services securely). |
| **Cloud Hosting** | **Render & Streamlit Cloud** | **PaaS** (Platform as a Service - cloud hosting providers that automatically build, deploy, and scale web applications directly from a GitHub repository). |

---

## 4. API Ingestion & Data Engineering Pipelines

SkyMetrics connects three primary external APIs:

1. **OpenSky Network API** (Live Aircraft Telemetry):
   - **What it provides:** Aircraft ICAO24 addresses, callsigns, latitude, longitude, altitude in meters, velocity in meters per second, heading angle, and origin country.
   - **How it connects:** Extracted every 10 minutes via background HTTP requests. If OpenSky hits rate limits or network issues, an automatic **Fallback Telemetry Generator** updates flight vectors realistically so the dashboard never goes down.

2. **OpenWeather API / METAR** (Airport Weather Telemetry):
   - **What it provides:** Temperature (°C), wind speed (knots), wind direction (degrees), visibility (km), humidity (%), barometric pressure (hPa), and weather summaries (Clear, Rain, Fog, Thunderstorm).
   - **How it connects:** Extracted every 15 minutes to correlate weather conditions with flight delay probabilities.

3. **OpenFlights Database** (Global Airport Metadata):
   - **What it provides:** Airport names, IATA 3-letter codes (e.g., DEL, BOM, LHR, JFK), ICAO 4-letter codes (VIDP, VABB, EGLL), latitude, longitude, elevation in feet, and runway counts.

---

## 5. Data Warehouse Schema (11 Relational Tables)

The database schema is organized into 11 normalized tables:

1. `users`: Stores user accounts, handles, emails, hashed passwords (**Bcrypt**), and roles (`admin`, `analyst`, `viewer`).
2. `airports`: Airport metadata (IATA, ICAO, name, city, country, coordinates, runways).
3. `weather`: Recorded weather reports linked to airports via **Foreign Keys** (relational links connecting rows in one table to rows in another).
4. `live_flights`: Current state vectors for aircraft in air (`callsign`, `latitude`, `longitude`, `altitude_m`, `velocity_mps`, `status`).
5. `historical_flights`: Past flight flight records (500+ pre-seeded flights used for trend analysis and ML model training).
6. `predictions`: Saved ML delay predictions (**Delay Probability %**, **Expected Delay Mins**, **Risk Level**, input snapshot).
7. `alerts`: User-defined operational trigger rules (e.g. alert if wind speed > 25 knots at DEL).
8. `etl_logs`: Automated execution logs storing DAG ID, task status (`SUCCESS`/`FAILED`), records processed, and execution latency.
9. `user_preferences`: UI theme settings, default airport hub, notification toggles.
10. `analytics_cache`: Cached aggregated calculations for sub-second dashboard rendering.
11. `audit_logs`: Operational security audit log tracking user logins, alert creation, and administrative actions.

---

## 6. Machine Learning Delay Prediction Engine

SkyMetrics features a two-stage **XGBoost Machine Learning pipeline**:

* **Classification Model (XGBClassifier):** Predicts whether a flight will experience a delay over 15 minutes (**Delay Probability %**).
  - **Accuracy:** `94.33%`
  - **ROC-AUC Score:** `0.9340` (Receiver Operating Characteristic Area Under Curve - a measure of how accurately a model distinguishes between delayed and on-time flights, where 1.0 is perfect).
* **Regression Model (XGBRegressor):** Predicts the exact delay duration in minutes (**Expected Delay Mins**).
  - **RMSE:** `10.62 minutes` (Root Mean Square Error - average magnitude of prediction error).

### Feature Engineering Input Variables:
1. `distance_km` (Flight route distance)
2. `temp_c` (Ambient temperature)
3. `wind_speed_kts` (Wind velocity)
4. `visibility_km` (Visibility distance)
5. `humidity_pct` (Relative humidity)
6. `pressure_hpa` (Barometric pressure)
7. `hour_of_day` (0-23 UTC departure hour)
8. `day_of_week` (Day of week)
9. `is_holiday` (Peak holiday flag)
10. `aircraft_speed_mps` (Aircraft speed)
11. `altitude_m` (Flight altitude)
12. `historical_airport_delay_avg` (Historical congestion average)

### Model Explainability (SHAP):
Rather than operating as a "black box", SkyMetrics calculates **SHAP values** (Shapley Additive exPlanations) for every prediction. It breaks down the exact percentage impact of each factor—e.g., showing that wind speed contributed +18% to the delay risk while high visibility reduced risk by -5%.

---

## 7. Dashboard Features & Component Breakdown (Page by Page)

The dashboard uses a **Sky Blue & White theme** (`#0284c7` primary blue, `#ffffff` card containers, `#e0f2fe` background):

### 1. 🏠 Home Page (Executive Command Center)
- **Top Sky Blue Navigation Bar:** Custom header with branding and quick links.
- **Graphic Aviation Showcase:** High-resolution photography of commercial jet aircraft taking off and landing.
- **KPI Metric Cards:** Displays Total Live Flights, On-Schedule Air Count, Delayed Flights Count, Avg Delay Mins, and ML Model Accuracy (94.3%).
- **Operational Intelligence Briefing:** AI-generated natural language status summary and dispatcher recommendations.

### 2. ✈️ Live Tracking (3D Airspace Radar)
- **PyDeck 3D Map & Folium Map:** Displays aircraft position markers in 3D space with FlightAware-style tan/orange aircraft icons and green airport nodes with yellow IATA badges (`DEL`, `BOM`, `BLR`, `MAA`, `HYD`, `CCU`).
- **Filter Controls:** Filter by origin, destination, status (`EN_ROUTE`, `DELAYED`), or map engine.
- **Telemetry Data Feed:** Structured table displaying callsign, country, altitude, ground speed, and heading.

### 3. 🔍 Flight Search
- **Multi-Criteria Query Engine:** Search live telemetry or historical flight warehouse records by Callsign (`AIC101`, `IGO505`), Flight Number, Airport Code (`DEL`, `BOM`), or Airline (`Air India`, `IndiGo`, `Vistara`).

### 4. 🤖 Delay Prediction Engine (Interactive ML Calculator)
- **Interactive Risk Inputs:** Sliders for wind speed, visibility, temperature, departure hour, and historical delay averages.
- **Real-Time XGBoost Inference:** Generates Delay Probability %, Expected Delay Mins, Risk Category (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), and a Plotly Gauge chart.
- **SHAP Feature Impact Table:** Explains the exact numerical contribution of each atmospheric and flight factor.

### 5. 🏬 Airport Analytics
- **Hub Ranking Bar Charts:** Visualizes busiest airport hub traffic volumes.
- **Airport Metadata Grid:** Displays IATA, ICAO, elevation, runway counts, and coordinates.

### 6. 🌤️ Weather Impact Analysis
- **Weather METAR Telemetry:** Displays severe weather warnings (fog, high wind gusts).
- **Factor Correlation Heatmap:** Plotly matrix showing correlations between wind, visibility, humidity, and delay risk.

### 7. 📈 Historical Trends
- **Global Fleet Treemap:** Hierarchical visualization of flights grouped by region and airline.
- **Scatter Telemetry Distribution:** Altitude (m) vs Speed (m/s) scatter plot.

### 8. 💡 AI Operational Insights
- **Natural Language Diagnostics:** Generates automated operational summaries and recommended dispatcher action items.

### 9. 🚨 Alerts Center
- **Custom Rule Engine:** Users can create custom flight or weather alert rules (e.g. alert if wind speed > 25 knots at DEL).

### 10. ⚙️ Admin Operations
- **ETL DAG Log Audit:** Real-time log viewer displaying execution times and record counts.
- **ML Retraining Button:** Triggers model retraining on new warehouse records with a single click.

---

## 8. Technical Interview Talking Points & Q&A

**Q1: How do you handle external API rate limits or failures?**
> *"SkyMetrics uses a resilient architecture. If external APIs like OpenSky Network or OpenWeather hit rate limits or go offline, our data pipeline automatically switches to a high-fidelity synthetic telemetry generator. Furthermore, the dashboard features an independent API client with local database fallback, ensuring zero downtime."*

**Q2: Why did you choose XGBoost over a simple linear regression?**
> *"Flight delays involve non-linear interactions between weather factors, airport congestion, and flight timing. XGBoost captures non-linear feature interactions efficiently, handles missing values gracefully, and achieved a high classification accuracy of 94.33% and ROC-AUC of 0.934. Additionally, pairing XGBoost with SHAP gives us complete explainability for air traffic controllers."*

**Q3: How is the application deployed?**
> *"SkyMetrics supports a Dual Cloud Architecture. The backend REST API and PostgreSQL database are hosted on Render paired with a Neon PostgreSQL instance. The Streamlit dashboard is independently deployed on Streamlit Community Cloud, fetching data from the backend via REST endpoints with secret-managed API URLs."*
