import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from database.connection import get_db
from backend.models.models import LiveFlight, Airport
from ml.predictor import predictor_instance

router = APIRouter(tags=["Health & Monitoring"])

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db_ok = False
    try:
        db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    ml_ok = predictor_instance.artifact is not None

    return {
        "status": "HEALTHY" if (db_ok and ml_ok) else "DEGRADED",
        "database_connected": db_ok,
        "ml_model_loaded": ml_ok,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@router.get("/metrics")
def metrics(db: Session = Depends(get_db)):
    active_flights = db.query(LiveFlight).count()
    airports_count = db.query(Airport).count()

    return {
        "skymetrics_active_flights_gauge": active_flights,
        "skymetrics_airports_monitored_gauge": airports_count,
        "skymetrics_ml_predictor_status": 1 if predictor_instance.artifact else 0,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
