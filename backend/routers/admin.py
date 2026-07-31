from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db, engine
from backend.models.models import User, ETLLog, AuditLog, LiveFlight, HistoricalFlight, Airport
from backend.schemas.schemas import UserResponse, ETLLogResponse
from backend.core.security import require_role

router = APIRouter(prefix="/api/v1/admin", tags=["Admin Center"])

@router.get("/users", response_model=List[UserResponse])
def get_all_users(current_user: User = Depends(require_role(["admin"])), db: Session = Depends(get_db)):
    return db.query(User).order_by(User.created_at.desc()).all()

@router.get("/etl-logs", response_model=List[ETLLogResponse])
def get_etl_logs(limit: int = 50, current_user: User = Depends(require_role(["admin", "analyst"])), db: Session = Depends(get_db)):
    return db.query(ETLLog).order_by(ETLLog.executed_at.desc()).limit(limit).all()

@router.get("/audit-logs")
def get_audit_logs(limit: int = 50, current_user: User = Depends(require_role(["admin"])), db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    return logs

@router.get("/db-stats")
def get_database_stats(current_user: User = Depends(require_role(["admin"])), db: Session = Depends(get_db)):
    return {
        "users_count": db.query(User).count(),
        "airports_count": db.query(Airport).count(),
        "live_flights_count": db.query(LiveFlight).count(),
        "historical_flights_count": db.query(HistoricalFlight).count(),
        "etl_logs_count": db.query(ETLLog).count(),
        "database_driver": engine.name
    }
