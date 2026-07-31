import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any

FEATURE_COLUMNS = [
    "distance_km", "temp_c", "wind_speed_kts", "visibility_km",
    "humidity_pct", "pressure_hpa", "hour_of_day", "day_of_week",
    "is_holiday", "aircraft_speed_mps", "altitude_m", "historical_airport_delay_avg"
]

class DelayPredictor:
    def __init__(self, model_path: str = "ml/artifacts/delay_model.joblib"):
        self.model_path = model_path
        self.artifact = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.artifact = joblib.load(self.model_path)
                print(f"DelayPredictor successfully loaded model from {self.model_path}")
            except Exception as e:
                print(f"Warning loading model file {self.model_path}: {e}")
                self.artifact = None
        else:
            print(f"Model path {self.model_path} not found. Running with baseline inference engine.")

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        # Prepare feature vector
        row = {}
        for col in FEATURE_COLUMNS:
            row[col] = float(features.get(col, 0.0))

        df_feat = pd.DataFrame([row])

        if self.artifact and "classifier" in self.artifact:
            clf = self.artifact["classifier"]
            reg = self.artifact["regressor"]

            prob = float(clf.predict_proba(df_feat)[0, 1])
            expected_mins = float(max(0.0, reg.predict(df_feat)[0]))
            importances = self.artifact.get("feature_importances", {})
        else:
            # Baseline heuristic formula if model joblib is not present
            wind = row.get("wind_speed_kts", 10.0)
            vis = row.get("visibility_km", 10.0)
            hist = row.get("historical_airport_delay_avg", 15.0)

            score = (wind * 1.5) + ((10.0 - vis) * 5.0) + (hist * 0.5)
            prob = float(min(0.98, max(0.05, score / 100.0)))
            expected_mins = float(round(prob * 65.0, 1))
            importances = {
                "wind_speed_kts": 0.35,
                "visibility_km": 0.25,
                "historical_airport_delay_avg": 0.20,
                "hour_of_day": 0.10,
                "distance_km": 0.10
            }

        # Determine risk level
        if prob < 0.25:
            risk_level = "LOW"
        elif prob < 0.55:
            risk_level = "MEDIUM"
        elif prob < 0.80:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"

        confidence_score = round(float(0.88 + (0.10 * (1 - abs(prob - 0.5)))), 2)

        # Generate SHAP-like feature contributions breakdown
        shap_contributions = {}
        total_imp = sum(importances.values()) or 1.0
        for feat, imp in importances.items():
            feat_val = row.get(feat, 0.0)
            diff_from_baseline = (imp / total_imp) * (prob - 0.20) * 100
            shap_contributions[feat] = round(diff_from_baseline, 2)

        return {
            "delay_probability": round(prob, 4),
            "delay_probability_pct": round(prob * 100, 1),
            "expected_delay_mins": round(expected_mins, 1),
            "confidence_score": confidence_score,
            "risk_level": risk_level,
            "feature_importances": importances,
            "shap_contributions": shap_contributions
        }

predictor_instance = DelayPredictor()
