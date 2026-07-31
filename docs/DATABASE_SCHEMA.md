# SkyMetrics Data Warehouse Relational Schema

SkyMetrics utilizes a normalized relational data model managed via SQLAlchemy ORM and Alembic migrations.

## Tables & Entity Specifications

### `users`
- `id` (INTEGER, PK): Primary key
- `username` (VARCHAR(50), UNIQUE, INDEX): Unique handle
- `email` (VARCHAR(100), UNIQUE, INDEX): User email
- `hashed_password` (VARCHAR(255)): Bcrypt hashed password
- `role` (VARCHAR(20)): `admin`, `analyst`, or `viewer`
- `is_active` (BOOLEAN): Active status flag
- `created_at` (DATETIME): Timestamp

### `airports`
- `id` (INTEGER, PK): Primary key
- `iata` (VARCHAR(3), UNIQUE, INDEX): IATA airport code
- `icao` (VARCHAR(4), UNIQUE, INDEX): ICAO airport code
- `name` (VARCHAR(150)): Full airport name
- `city` (VARCHAR(100)): City
- `country` (VARCHAR(100), INDEX): Country
- `latitude` (FLOAT), `longitude` (FLOAT): Geographic coordinates
- `altitude_ft` (FLOAT): Elevation in feet
- `runways_count` (INTEGER): Number of active runways

### `weather`
- `id` (INTEGER, PK): Primary key
- `airport_id` (INTEGER, FK -> airports.id, INDEX): Foreign key
- `temperature_c` (FLOAT): Ambient temperature °C
- `wind_speed_kts` (FLOAT): Wind velocity in knots
- `visibility_km` (FLOAT): Visibility distance in km
- `humidity_pct` (FLOAT): Relative humidity %
- `pressure_hpa` (FLOAT): Barometric pressure hPa
- `condition_text` (VARCHAR(100)): Summary METAR condition
- `recorded_at` (DATETIME, INDEX): Observation timestamp

### `live_flights`
- `id` (INTEGER, PK): Primary key
- `icao24` (VARCHAR(24), INDEX): Aircraft ICAO 24-bit address
- `callsign` (VARCHAR(20), INDEX): Flight callsign
- `origin_country` (VARCHAR(100)): Country of aircraft registration
- `origin_iata` (VARCHAR(3), INDEX): Departure hub code
- `destination_iata` (VARCHAR(3), INDEX): Destination hub code
- `latitude` (FLOAT), `longitude` (FLOAT): Live coordinates
- `altitude_m` (FLOAT): Altitude in meters
- `velocity_mps` (FLOAT): Ground speed in m/s
- `status` (VARCHAR(30)): Flight operational state (`EN_ROUTE`, `ON_APPROACH`, `DELAYED`)

### `predictions`
- `id` (INTEGER, PK): Primary key
- `flight_identifier` (VARCHAR(50), INDEX): Flight handle
- `delay_probability` (FLOAT): Predicted probability (0.0 - 1.0)
- `expected_delay_mins` (FLOAT): Estimated delay duration in minutes
- `risk_level` (VARCHAR(20)): `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- `feature_snapshot` (JSON): Input feature dictionary
- `created_at` (DATETIME, INDEX): Execution timestamp

### `etl_logs`
- `id` (INTEGER, PK): Primary key
- `dag_id` (VARCHAR(100), INDEX): Airflow/Runner DAG ID
- `task_id` (VARCHAR(100)): Task name
- `status` (VARCHAR(30), INDEX): `SUCCESS`, `FAILED`
- `records_processed` (INTEGER): Number of ingested records
- `execution_time_sec` (FLOAT): Execution latency
- `executed_at` (DATETIME, INDEX): Timestamp
