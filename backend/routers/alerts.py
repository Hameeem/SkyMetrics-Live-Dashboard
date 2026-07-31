import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.models.models import Alert, User, AuditLog
from backend.schemas.schemas import AlertCreate, AlertResponse
from backend.core.security import get_current_user

router = APIRouter(prefix="/api/v1/alerts", tags=["Alerts"])

@router.get("", response_model=List[AlertResponse])
def get_user_alerts(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Alert).filter(Alert.user_id == current_user.id).order_by(Alert.created_at.desc()).all()

@router.post("/create", response_model=AlertResponse, status_code=status.HTTP_201_CREATED)
def create_alert(alert_in: AlertCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    new_alert = Alert(
        user_id=current_user.id,
        title=alert_in.title,
        alert_type=alert_in.alert_type,
        target_airport=alert_in.target_airport.upper() if alert_in.target_airport else None,
        target_flight=alert_in.target_flight.upper() if alert_in.target_flight else None,
        threshold_value=alert_in.threshold_value,
        is_active=True
    )
    db.add(new_alert)
    db.commit()
    db.refresh(new_alert)

    db.add(AuditLog(username=current_user.username, action="CREATE_ALERT", details=f"Created alert: {new_alert.title}"))
    db.commit()

    return new_alert

@router.delete("/{alert_id}")
def delete_alert(alert_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user.id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.delete(alert)
    db.commit()
    return {"message": "Alert deleted successfully"}
