from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database.connection import get_db
from backend.models.models import Weather, Airport
from backend.schemas.schemas import WeatherResponse

router = APIRouter(prefix="/api/v1/weather", tags=["Weather"])

@router.get("/current", response_model=List[WeatherResponse])
def get_current_weather(
    min_wind: Optional[float] = Query(None, description="Minimum wind speed in knots"),
    max_vis: Optional[float] = Query(None, description="Maximum visibility in km"),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db)
):
    query = db.query(Weather)
    if min_wind is not None:
        query = query.filter(Weather.wind_speed_kts >= min_wind)
    if max_vis is not None:
        query = query.filter(Weather.visibility_km <= max_vis)

    return query.order_by(Weather.recorded_at.desc()).limit(limit).all()
