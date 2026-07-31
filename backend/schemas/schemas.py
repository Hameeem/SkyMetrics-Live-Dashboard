from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import datetime

# Authentication Schemas
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "analyst"

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime.datetime
    last_login: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True

# Airport Schemas
class AirportResponse(BaseModel):
    id: int
    iata: str
    icao: str
    name: str
    city: str
    country: str
    latitude: float
    longitude: float
    altitude_ft: float
    runways_count: int

    class Config:
        from_attributes = True

# Weather Schemas
class WeatherResponse(BaseModel):
    id: int
    airport_id: int
    temperature_c: float
    wind_speed_kts: float
    wind_direction_deg: float
    visibility_km: float
    humidity_pct: float
    pressure_hpa: float
    condition_text: str
    recorded_at: datetime.datetime

    class Config:
        from_attributes = True

# Flight Schemas
class LiveFlightResponse(BaseModel):
    id: int
    icao24: str
    callsign: str
    origin_country: str
    origin_iata: Optional[str]
    destination_iata: Optional[str]
    latitude: float
    longitude: float
    altitude_m: float
    velocity_mps: float
    heading_deg: float
    vertical_rate_mps: float
    on_ground: bool
    status: str
    last_contact: datetime.datetime

    class Config:
        from_attributes = True

class HistoricalFlightResponse(BaseModel):
    id: int
    flight_number: str
    airline: str
    origin_iata: str
    destination_iata: str
    scheduled_departure: datetime.datetime
    actual_departure: Optional[datetime.datetime]
    scheduled_arrival: datetime.datetime
    actual_arrival: Optional[datetime.datetime]
    delay_minutes: float
    is_delayed: bool
    distance_km: float
    aircraft_type: str
    status: str

    class Config:
        from_attributes = True

# Prediction Schemas
class PredictionRequest(BaseModel):
    flight_identifier: str
    origin_iata: str
    destination_iata: str
    distance_km: float
    temp_c: float
    wind_speed_kts: float
    visibility_km: float
    humidity_pct: float = 60.0
    pressure_hpa: float = 1013.25
    hour_of_day: int = 14
    day_of_week: int = 2
    is_holiday: int = 0
    aircraft_speed_mps: float = 240.0
    altitude_m: float = 10000.0
    historical_airport_delay_avg: float = 15.0

class PredictionResponse(BaseModel):
    flight_identifier: str
    origin_iata: str
    destination_iata: str
    delay_probability: float
    delay_probability_pct: float
    expected_delay_mins: float
    confidence_score: float
    risk_level: str
    feature_importances: Dict[str, float]
    shap_contributions: Dict[str, float]

# Alert Schemas
class AlertCreate(BaseModel):
    title: str
    alert_type: str
    target_airport: Optional[str] = None
    target_flight: Optional[str] = None
    threshold_value: Optional[float] = None

class AlertResponse(BaseModel):
    id: int
    title: str
    alert_type: str
    target_airport: Optional[str]
    target_flight: Optional[str]
    threshold_value: Optional[float]
    is_active: bool
    triggered_count: int
    last_triggered: Optional[datetime.datetime]
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# Admin / System Schemas
class ETLLogResponse(BaseModel):
    id: int
    dag_id: str
    task_id: str
    status: str
    records_processed: int
    execution_time_sec: float
    error_message: Optional[str]
    executed_at: datetime.datetime

    class Config:
        from_attributes = True

class SystemHealthResponse(BaseModel):
    status: str
    database_connected: bool
    ml_model_loaded: bool
    active_flights_count: int
    airports_count: int
    timestamp: datetime.datetime
