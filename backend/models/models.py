import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Index, JSON
)
from sqlalchemy.orm import relationship
from database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="analyst") # admin, analyst, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="user", cascade="all, delete-orphan")

class Airport(Base):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    iata = Column(String(3), unique=True, nullable=False, index=True)
    icao = Column(String(4), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude_ft = Column(Float, default=0.0)
    timezone = Column(String(50), default="UTC")
    runways_count = Column(Integer, default=2)

    weather_reports = relationship("Weather", back_populates="airport", cascade="all, delete-orphan")

class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True, index=True)
    airport_id = Column(Integer, ForeignKey("airports.id", ondelete="CASCADE"), nullable=False, index=True)
    temperature_c = Column(Float, nullable=False)
    wind_speed_kts = Column(Float, nullable=False)
    wind_direction_deg = Column(Float, default=0.0)
    visibility_km = Column(Float, nullable=False)
    humidity_pct = Column(Float, default=50.0)
    pressure_hpa = Column(Float, default=1013.25)
    condition_text = Column(String(100), default="Clear") # Clear, Rain, Fog, Storm, Snow
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    airport = relationship("Airport", back_populates="weather_reports")

class LiveFlight(Base):
    __tablename__ = "live_flights"

    id = Column(Integer, primary_key=True, index=True)
    icao24 = Column(String(24), nullable=False, index=True)
    callsign = Column(String(20), nullable=False, index=True)
    origin_country = Column(String(100), default="Unknown")
    origin_iata = Column(String(3), nullable=True, index=True)
    destination_iata = Column(String(3), nullable=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    altitude_m = Column(Float, default=0.0)
    velocity_mps = Column(Float, default=0.0)
    heading_deg = Column(Float, default=0.0)
    vertical_rate_mps = Column(Float, default=0.0)
    on_ground = Column(Boolean, default=False)
    status = Column(String(30), default="EN_ROUTE") # EN_ROUTE, ON_APPROACH, TAXIING, DELAYED
    last_contact = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class HistoricalFlight(Base):
    __tablename__ = "historical_flights"

    id = Column(Integer, primary_key=True, index=True)
    flight_number = Column(String(20), nullable=False, index=True)
    airline = Column(String(100), nullable=False, index=True)
    origin_iata = Column(String(3), nullable=False, index=True)
    destination_iata = Column(String(3), nullable=False, index=True)
    scheduled_departure = Column(DateTime, nullable=False)
    actual_departure = Column(DateTime, nullable=True)
    scheduled_arrival = Column(DateTime, nullable=False)
    actual_arrival = Column(DateTime, nullable=True)
    delay_minutes = Column(Float, default=0.0)
    is_delayed = Column(Boolean, default=False, index=True)
    distance_km = Column(Float, default=500.0)
    aircraft_type = Column(String(50), default="B737")
    status = Column(String(30), default="COMPLETED")

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    flight_identifier = Column(String(50), nullable=False, index=True)
    origin_iata = Column(String(3), nullable=False)
    destination_iata = Column(String(3), nullable=False)
    delay_probability = Column(Float, nullable=False) # 0.0 - 1.0
    expected_delay_mins = Column(Float, nullable=False)
    confidence_score = Column(Float, default=0.90)
    risk_level = Column(String(20), default="LOW") # LOW, MEDIUM, HIGH, CRITICAL
    feature_snapshot = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(150), nullable=False)
    alert_type = Column(String(50), nullable=False) # DELAY_THRESHOLD, WEATHER_WARNING, ALTITUDE_DEV
    target_airport = Column(String(10), nullable=True)
    target_flight = Column(String(20), nullable=True)
    threshold_value = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    triggered_count = Column(Integer, default=0)
    last_triggered = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="alerts")

class ETLLog(Base):
    __tablename__ = "etl_logs"

    id = Column(Integer, primary_key=True, index=True)
    dag_id = Column(String(100), nullable=False, index=True)
    task_id = Column(String(100), nullable=False)
    status = Column(String(30), nullable=False, index=True) # SUCCESS, FAILED, RUNNING
    records_processed = Column(Integer, default=0)
    execution_time_sec = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    executed_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    theme = Column(String(20), default="dark")
    default_airport = Column(String(3), default="LHR")
    email_notifications = Column(Boolean, default=True)
    auto_refresh_sec = Column(Integer, default=30)

    user = relationship("User", back_populates="preferences")

class AnalyticsCache(Base):
    __tablename__ = "analytics_cache"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String(100), unique=True, nullable=False, index=True)
    cached_data = Column(JSON, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False, index=True)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    ip_address = Column(String(50), default="127.0.0.1")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
