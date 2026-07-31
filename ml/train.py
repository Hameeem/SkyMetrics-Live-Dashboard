import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import joblib
import pandas as pd

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score, mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor

from ml.dataset import generate_flight_delay_dataset

FEATURE_COLUMNS = [
    "distance_km", "temp_c", "wind_speed_kts", "visibility_km",
    "humidity_pct", "pressure_hpa", "hour_of_day", "day_of_week",
    "is_holiday", "aircraft_speed_mps", "altitude_m", "historical_airport_delay_avg"
]

def train_delay_model(output_path: str = "ml/artifacts/delay_model.joblib"):
    print("Generating dataset for SkyMetrics ML training...")
    df = generate_flight_delay_dataset(num_samples=3000)

    X = df[FEATURE_COLUMNS]
    y_class = df["is_delayed"]
    y_reg = df["delay_minutes"]

    X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
        X, y_class, y_reg, test_size=0.2, random_state=42
    )

    print("Training XGBoost Delay Classification & Regression Models...")
    clf = XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.08, random_state=42)
    clf.fit(X_train, y_class_train)

    reg = XGBRegressor(n_estimators=100, max_depth=5, learning_rate=0.08, random_state=42)
    reg.fit(X_train, y_reg_train)

    # Evaluation
    class_preds = clf.predict(X_test)
    class_probs = clf.predict_proba(X_test)[:, 1]
    reg_preds = reg.predict(X_test)

    acc = accuracy_score(y_class_test, class_preds)
    roc_auc = roc_auc_score(y_class_test, class_probs)
    rmse = np.sqrt(mean_squared_error(y_reg_test, reg_preds))
    mae = mean_absolute_error(y_reg_test, reg_preds)

    print(f"--- Model Evaluation Results ---")
    print(f"Classification Accuracy: {acc:.4f}")
    print(f"ROC-AUC Score:           {roc_auc:.4f}")
    print(f"Delay Mins RMSE:         {rmse:.2f} mins")
    print(f"Delay Mins MAE:          {mae:.2f} mins")

    # Feature Importance
    importances = dict(zip(FEATURE_COLUMNS, clf.feature_importances_))
    sorted_importances = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    artifact = {
        "classifier": clf,
        "regressor": reg,
        "feature_columns": FEATURE_COLUMNS,
        "feature_importances": sorted_importances,
        "metrics": {
            "accuracy": float(acc),
            "roc_auc": float(roc_auc),
            "rmse": float(rmse),
            "mae": float(mae)
        }
    }

    joblib.dump(artifact, output_path)
    print(f"Model saved successfully to {output_path}")

    return artifact

if __name__ == "__main__":
    train_delay_model()
