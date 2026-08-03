# ✈️ SkyMetrics - Enterprise Aviation Intelligence Platform
## Complete Project Explanation & Sidebar Feature Technical Defense Guide

---

## 📌 Executive Overview
**SkyMetrics** is a production-ready, enterprise-grade Aviation Intelligence Platform built with **Python**, **Streamlit**, **FastAPI**, **SQLAlchemy**, and **XGBoost Machine Learning**. 

It aggregates real-time flight telemetry [telemetry: automated transmission of live data from remote sensors], processes atmospheric weather conditions, predicts flight delay risks using Machine Learning [ML: computer algorithms that improve automatically through experience], and displays live vector tracking maps across all 35+ major Indian airports and international flight corridors.

---

## 🛠️ System Architecture & Technology Stack

1. **Frontend Dashboard Layer**:
   - **Streamlit**: Python web framework used for rapid, dynamic enterprise UI rendering.
   - **Folium & Leaflet.js**: Open-source interactive map engine rendering rotated airplane markers [vector icons: scalable graphic markers representing aircraft direction and status].
   - **Plotly**: Interactive data visualization library for treemaps, scatter plots, pie charts, gauge meters, and monthly timeline bars.

2. **Backend API & Data Warehouse Layer**:
   - **FastAPI**: Asynchronous high-performance RESTful API [API: Application Programming Interface allowing system communication] backend.
   - **SQLAlchemy & SQLite / PostgreSQL**: Relational database ORM [ORM: Object-Relational Mapping framework translating database rows into Python objects].
   - **PyArrow & Pandas**: High-throughput data manipulation and columnar data processing libraries.

3. **Machine Learning Pipeline**:
   - **XGBoost Classifier**: Extreme Gradient Boosting decision tree algorithm trained on historical flight performance, wind velocity, visibility, and departure hour.
   - **SHAP (SHapley Additive exPlanations)**: Explainable AI framework calculating the exact mathematical contribution (+/- %) of each weather variable to the final delay prediction.

4. **Multi-Cloud Deployment Infrastructure**:
   - **Microsoft Azure App Service**: Production Linux Web App container hosted in Central India.
   - **Streamlit Community Cloud**: Official Snowflake cloud hosting linked directly to GitHub `main` branch.
   - **GitHub Pages (stlite Wasm)**: Client-side Pyodide WebAssembly [Wasm: low-level binary code format allowing Python to execute inside any web browser without a server] hosting.

---

## 🧭 Comprehensive Feature Breakdown: How Each Sidebar Feature Actually Works

Below is the technical breakdown of how every feature in the **SkyMetrics** left sidebar operates under the hood:

---

### 1. 🏠 Home (Executive Command Center Overview)
* **What it Does**: Serves as the central operational dashboard giving flight dispatchers and executive stakeholders an immediate overview of global airspace health.
* **How it Works Under the Hood**:
  - **KPI Metrics Cards**: Queries the live database to count total active flights (`48`), on-schedule flights (`42`), delayed flights (`6`), average delay duration (`38.8m`), and machine learning model accuracy (`94.3%`).
  - **Operational Status Breakdown Chart**: Renders a dynamic donut pie chart grouping active flights into `ON-TIME` (green), `ON-APPROACH` (yellow), and `DELAYED` (red).
  - **AI Operational Brief**: Evaluates current holding patterns and auto-generates dispatcher action items.

---

### 2. ✈️ Live Tracking (Real-Time Airspace Vector Radar)
* **What it Does**: Provides a real-time interactive map of Indian and international airspace displaying aircraft locations, headings, speeds, and altitudes.
* **How it Works Under the Hood**:
  - **GPS Latitude/Longitude Mapping**: Fetches live spatial coordinates (`latitude`, `longitude`, `heading`) for every flight.
  - **Rotated Plane Markers**: Uses CSS `transform: rotate(Ndeg)` to orient plane icons (`✈️`) in the exact heading direction of travel.
  - **Hover Tooltip System**: When a user hovers their cursor over any aircraft, Leaflet `tooltip` JavaScript events instantly display callsign (`IGO505`), airline (`IndiGo`), route (`DEL ➔ SXR`), altitude (`9,800 m`), and speed (`220 m/s`).
  - **Click Popups**: Clicking an airplane opens an HTML popup card with full flight telemetry.

---

### 3. 🔍 Flight Search (Multi-Column Global Search Engine)
* **What it Does**: Enables dispatchers to instantly find any flight or airport hub by typing a callsign, flight number, airport code, or city name.
* **How it Works Under the Hood**:
  - **SQLAlchemy Multi-Column `or_` Filter**: Executes a relational database query matching the search string against `origin_iata` [IATA: 3-letter international airport code e.g. SXR for Srinagar, DEL for Delhi], `destination_iata`, `callsign` (e.g. `IGO505`), `city`, and `country`.
  - **Dual-Pane Dataframe Output**: Displays matching active flights in the left pane and matching airport hubs in the right pane simultaneously.

---

### 4. 📊 Analysis (Airport & Airline Deep Operations Dashboard)
* **What it Does**: Executive operational dashboard providing deep granular analytics on airport takeoffs, landings, delays, on-time arrival % by airline company, and flight route density.
* **How it Works Under the Hood**:
  - **Airport Selector Dropdown**: Select any specific airport hub (`DEL`, `BOM`, `BLR`, `MAA`, `HYD`, `CCU`, `SXR`, `DHM`, `ATQ`, `IXC`, `TRZ`) or `ALL Indian Airspace Hubs`.
  - **Timeframe Horizon Filter**: Toggle between `Today (24 Hours)`, `Past 7 Days (Week)`, `Past 30 Days (Month)`, and `Past 365 Days (Year)`.
  - **Top KPI Cards with Trend Line Sparklines**: Displays total Takeoffs/Departures (`142`), Landings/Arrivals (`138`), Delayed Flights (`12`), and On-Time Arrival % Gauge (`87.2%`) paired with 7-day trend sparkline graphs.
  - **Airline Carrier Performance Table**: Compares IndiGo, Air India, Vistara, Akasa Air, and SpiceJet by total flight volume, on-time arrival %, average delay mins, and status rating.
  - **Route Corridor Traffic Share**: Renders flight volume and % share for top routes originating from the selected airport.

---

### 5. 🤖 Delay Prediction (XGBoost ML Risk Engine)
* **What it Does**: Allows air traffic managers to input expected weather conditions and flight parameters to calculate the exact probability (%) of a flight delay before takeoff.
* **How it Works Under the Hood**:
  - **Interactive Sliders**: Users adjust `Wind Speed (knots)` [knots: unit of speed equal to 1 nautical mile per hour], `Visibility (km)`, `Departure Hour (UTC)`, and `Departure Airport`.
  - **Inference Engine**: Passes the feature vector [feature vector: numerical list of input variables] to the pre-trained XGBoost model.
  - **SHAP Breakdown**: Computes feature attribution scores, showing the exact percentage contribution of wind, visibility, or departure hour to the final delay risk.

---

### 6. 🏬 Airport Analytics (Airspace Movement Rankings)
* **What it Does**: Analyzes airport hub capacity, total daily aircraft movements, and active runway counts across Indian airports.
* **How it Works Under the Hood**:
  - Aggregates origin and destination flight logs from the data warehouse, sorting airport hubs from highest movement volume (e.g. Delhi `DEL` with 1,420 movements/day) to regional hubs (Srinagar `SXR` with 280 movements/day, Dharamshala `DHM` with 140 movements/day).

---

### 7. 🌤️ Weather Impact (METAR Observation & Weather Search)
* **What it Does**: Displays live METAR [METAR: Meteorological Aerodrome Report standard format for airport weather observations] weather data and allows searching weather conditions for any airport.
* **How it Works Under the Hood**:
  - **Interactive Search Engine**: Users type any airport code (`SXR`, `DHM`, `DEL`, `BOM`, `DXB`, `LHR`) or city (`Srinagar`, `London`).
  - **METAR Telemetry Inspection**: Returns live temperature (`°C`), wind velocity (`kts`), visibility (`km`), weather phenomenon (`FOG`, `RAIN`, `HAZE`), and risk rating (`LOW`, `MEDIUM`, `HIGH`).

---

### 8. 📈 Historical Trends (Fleet Distribution & Multi-Dimensional Analytics)
* **What it Does**: Visualizes historical operational trends, airline market share distributions, monthly traffic timelines, and flight speed vs altitude scatter plots.
* **How it Works Under the Hood**:
  - **Treemap Chart**: Renders an interactive Plotly treemap grouping airlines by market share (IndiGo 61.2%, Air India 24.5%, Vistara 8.8%, Akasa Air 4.1%, SpiceJet 1.4%).
  - **Scatter Plot**: Plots cruising altitude (`meters`) on the X-axis against velocity (`meters/second`) on the Y-axis.
  - **Monthly Bar Timeline**: Displays monthly flight volume trends (thousands of flights) colored by historical on-time performance %.

---

### 9. 💡 AI Insights (ATC Operational Diagnostics)
* **What it Does**: Generates natural language operational briefings and automated dispatcher recommendations.
* **How it Works Under the Hood**:
  - Analyzes active sector congestion, evaluates wind shear warnings at high-altitude airports like Srinagar (`SXR`), and outputs prioritized dispatcher action items.

---

### 10. ⚙️ Admin Ops (ETL DAG Pipeline Audit Logs & Model Controls)
* **What it Does**: Provides system administrators with pipeline execution logs and a 1-click model retraining trigger.
* **How it Works Under the Hood**:
  - **ETL Audit Logs**: Monitors Airflow/APScheduler DAGs [DAG: Directed Acyclic Graph representing automated ETL data pipeline steps] fetching live OpenSky Network flight data and OpenWeather METAR feeds.
  - **Model Retraining Button**: Triggers the scikit-learn/XGBoost training pipeline to re-fit model weights on newly ingested flight performance records.

---

## 🏆 Presentation Defense Tips & Key Takeaways
1. **Explain the Architecture**: Highlight that SkyMetrics separates data ingestion (OpenSky APIs / SQL database), ML prediction (XGBoost / SHAP), and multi-cloud presentation (Azure / Streamlit / GitHub Pages).
2. **Demonstrate `📊 Analysis` Dashboard**: Select an airport (e.g. `DEL` or `SXR`) and switch timeframes (`Today` vs `Week` vs `Month`) to show executive sparkline trends, airline on-time %, and route traffic density.
3. **Showcase Interactive Tracking Radar**: Hover your cursor over plane icons on the **Live Tracking** map to demonstrate real-time tooltip telemetry.
