import pandas as pd
import numpy as np
import random
from typing import Tuple

def generate_flight_delay_dataset(num_samples: int = 2500, random_state: int = 42) -> pd.DataFrame:
    """Generates synthetic dataset combining flight telemetry, weather metrics, and time factors for training."""
    np.random.seed(random_state)
    random.seed(random_state)

    airports = ["ATL", "LHR", "HND", "DXB", "ORD", "CDG", "SIN", "DEL", "JFK", "SYD", "FRA", "AMS", "LAX", "SFO", "BOM"]

    data = []
    for _ in range(num_samples):
        orig = random.choice(airports)
        dest = random.choice([a for a in airports if a != orig])
        distance_km = float(np.random.uniform(500, 12000))
        temp_c = float(np.random.uniform(-10, 45))
        wind_speed_kts = float(np.random.uniform(2, 45))
        visibility_km = float(np.random.uniform(0.5, 10.0))
        humidity_pct = float(np.random.uniform(20, 100))
        pressure_hpa = float(np.random.uniform(980, 1030))
        
        hour_of_day = int(np.random.randint(0, 24))
        day_of_week = int(np.random.randint(0, 7))
        is_holiday = 1 if np.random.random() < 0.15 else 0

        aircraft_speed_mps = float(np.random.uniform(180, 270))
        altitude_m = float(np.random.uniform(3000, 12000))
        historical_airport_delay_avg = float(np.random.uniform(5, 45))

        # Synthetic target formula: High winds, low visibility, peak hour, long distance, low pressure increase delay risk
        weather_risk = (wind_speed_kts * 1.2) + ((10.0 - visibility_km) * 3.5) + (35 - min(35, temp_c)) * 0.2
        time_risk = 15.0 if (7 <= hour_of_day <= 9 or 17 <= hour_of_day <= 20) else 5.0
        airport_risk = historical_airport_delay_avg * 0.4

        base_delay = weather_risk + time_risk + airport_risk + (is_holiday * 10.0) + np.random.normal(0, 10)
        delay_minutes = float(max(0.0, base_delay - 20.0))
        is_delayed = 1 if delay_minutes >= 15.0 else 0

        data.append({
            "origin_iata": orig,
            "destination_iata": dest,
            "distance_km": round(distance_km, 1),
            "temp_c": round(temp_c, 1),
            "wind_speed_kts": round(wind_speed_kts, 1),
            "visibility_km": round(visibility_km, 1),
            "humidity_pct": round(humidity_pct, 1),
            "pressure_hpa": round(pressure_hpa, 1),
            "hour_of_day": hour_of_day,
            "day_of_week": day_of_week,
            "is_holiday": is_holiday,
            "aircraft_speed_mps": round(aircraft_speed_mps, 1),
            "altitude_m": round(altitude_m, 1),
            "historical_airport_delay_avg": round(historical_airport_delay_avg, 1),
            "delay_minutes": round(delay_minutes, 1),
            "is_delayed": is_delayed
        })

    return pd.DataFrame(data)
