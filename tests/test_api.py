import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "database_connected" in data

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "skymetrics_active_flights_gauge" in data

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["platform"] == "SkyMetrics Enterprise Flight Intelligence Platform"

def test_auth_register_and_login():
    import random
    rand_id = random.randint(10000, 99999)
    username = f"testuser_{rand_id}"
    email = f"test_{rand_id}@skymetrics.ai"
    password = "TestPassword123!"

    # Register
    reg_resp = client.post("/api/v1/auth/register", json={
        "username": username,
        "email": email,
        "password": password,
        "role": "analyst"
    })
    assert reg_resp.status_code == 201
    assert reg_resp.json()["username"] == username

    # Login
    login_resp = client.post("/api/v1/auth/login", data={
        "username": username,
        "password": password
    })
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()

def test_get_live_flights():
    response = client.get("/api/v1/flights/live")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_airports():
    response = client.get("/api/v1/airports")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

def test_ml_prediction_api():
    payload = {
        "flight_identifier": "TEST999",
        "origin_iata": "LHR",
        "destination_iata": "JFK",
        "distance_km": 5500.0,
        "temp_c": 22.0,
        "wind_speed_kts": 18.0,
        "visibility_km": 8.0,
        "humidity_pct": 50.0,
        "pressure_hpa": 1013.25,
        "hour_of_day": 14,
        "day_of_week": 2,
        "is_holiday": 0,
        "aircraft_speed_mps": 240.0,
        "altitude_m": 10000.0,
        "historical_airport_delay_avg": 15.0
    }
    response = client.post("/api/v1/predictions/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "delay_probability" in data
    assert "risk_level" in data

def test_dashboard_kpis():
    response = client.get("/api/v1/dashboard/kpis")
    assert response.status_code == 200
    data = response.json()
    assert "total_live_flights" in data
    assert "busiest_airport" in data
