import pytest
from database.connection import SessionLocal
from scripts.etl_runner import task_fetch_live_flights, task_fetch_weather

def test_etl_tasks():
    db = SessionLocal()
    try:
        flights_processed = task_fetch_live_flights(db)
        assert flights_processed >= 0

        weather_processed = task_fetch_weather(db)
        assert weather_processed > 0
    finally:
        db.close()
