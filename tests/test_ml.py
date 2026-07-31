import pytest
import os
from ml.dataset import generate_flight_delay_dataset
from ml.train import train_delay_model
from ml.predictor import DelayPredictor

def test_dataset_generation():
    df = generate_flight_delay_dataset(num_samples=100)
    assert len(df) == 100
    assert "wind_speed_kts" in df.columns
    assert "delay_minutes" in df.columns
    assert "is_delayed" in df.columns

def test_ml_training_and_inference(tmp_path):
    model_file = str(tmp_path / "test_delay_model.joblib")
    artifact = train_delay_model(output_path=model_file)

    assert os.path.exists(model_file)
    assert "metrics" in artifact
    assert artifact["metrics"]["accuracy"] > 0.60

    predictor = DelayPredictor(model_path=model_file)
    features = {
        "distance_km": 5000.0,
        "temp_c": 35.0,
        "wind_speed_kts": 28.0,
        "visibility_km": 2.0,
        "humidity_pct": 80.0,
        "pressure_hpa": 995.0,
        "hour_of_day": 8,
        "day_of_week": 4,
        "is_holiday": 1,
        "aircraft_speed_mps": 220.0,
        "altitude_m": 8000.0,
        "historical_airport_delay_avg": 30.0
    }
    res = predictor.predict(features)
    assert 0.0 <= res["delay_probability"] <= 1.0
    assert res["risk_level"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    assert "shap_contributions" in res
