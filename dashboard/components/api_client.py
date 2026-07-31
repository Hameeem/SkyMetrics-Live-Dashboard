import os
import requests
from typing import Dict, Any, List, Optional

class APIClient:
    def __init__(self):
        self.base_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")
        self.token = None

    def check_health(self) -> Dict[str, Any]:
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=3)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        return {"status": "OFFLINE", "database_connected": False, "ml_model_loaded": True}

    def login(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        try:
            resp = requests.post(
                f"{self.base_url}/api/v1/auth/login",
                data={"username": username, "password": password},
                timeout=5
            )
            if resp.status_code == 200:
                data = resp.json()
                self.token = data.get("access_token")
                return data
        except Exception:
            pass
        return None

    def get_live_flights(self, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(f"{self.base_url}/api/v1/flights/live", params=params, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        # Fallback local query
        from database.connection import SessionLocal
        from backend.models.models import LiveFlight
        db = SessionLocal()
        try:
            flights = db.query(LiveFlight).limit(100).all()
            return [
                {
                    "id": f.id,
                    "icao24": f.icao24,
                    "callsign": f.callsign,
                    "origin_country": f.origin_country,
                    "origin_iata": f.origin_iata,
                    "destination_iata": f.destination_iata,
                    "latitude": f.latitude,
                    "longitude": f.longitude,
                    "altitude_m": f.altitude_m,
                    "velocity_mps": f.velocity_mps,
                    "heading_deg": f.heading_deg,
                    "vertical_rate_mps": f.vertical_rate_mps,
                    "on_ground": f.on_ground,
                    "status": f.status,
                    "last_contact": f.last_contact.isoformat() if f.last_contact else ""
                }
                for f in flights
            ]
        finally:
            db.close()

    def get_airports(self, query: str = None) -> List[Dict[str, Any]]:
        try:
            resp = requests.get(f"{self.base_url}/api/v1/airports", params={"query": query}, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from database.connection import SessionLocal
        from backend.models.models import Airport
        db = SessionLocal()
        try:
            q = db.query(Airport)
            if query:
                q = q.filter(Airport.iata.ilike(f"%{query}%"))
            airports = q.all()
            return [
                {
                    "id": a.id, "iata": a.iata, "icao": a.icao, "name": a.name,
                    "city": a.city, "country": a.country, "latitude": a.latitude,
                    "longitude": a.longitude, "altitude_ft": a.altitude_ft, "runways_count": a.runways_count
                }
                for a in airports
            ]
        finally:
            db.close()

    def get_kpis(self) -> Dict[str, Any]:
        try:
            resp = requests.get(f"{self.base_url}/api/v1/dashboard/kpis", timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from backend.routers.dashboard import get_dashboard_kpis
        from database.connection import SessionLocal
        db = SessionLocal()
        try:
            return get_dashboard_kpis(db)
        finally:
            db.close()

    def get_ai_insights(self, airport_code: str = "ALL") -> Dict[str, Any]:
        try:
            resp = requests.get(f"{self.base_url}/api/v1/dashboard/ai-insights", params={"airport_code": airport_code}, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from backend.routers.dashboard import get_ai_insights
        from database.connection import SessionLocal
        db = SessionLocal()
        try:
            return get_ai_insights(airport_code, db)
        finally:
            db.close()

    def predict_delay(self, features: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = requests.post(f"{self.base_url}/api/v1/predictions/predict", json=features, timeout=5)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass
        from ml.predictor import predictor_instance
        res = predictor_instance.predict(features)
        res["flight_identifier"] = features.get("flight_identifier", "SKY101")
        res["origin_iata"] = features.get("origin_iata", "LHR")
        res["destination_iata"] = features.get("destination_iata", "JFK")
        return res

api_client = APIClient()
