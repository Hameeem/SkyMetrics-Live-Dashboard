from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.connection import get_db
from backend.models.models import Airport, Weather
from backend.schemas.schemas import AirportResponse, WeatherResponse

router = APIRouter(prefix="/api/v1/airports", tags=["Airports"])

@router.get("", response_model=List[AirportResponse])
def get_airports(
    country: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    q = db.query(Airport)
    if country:
        q = q.filter(Airport.country.ilike(f"%{country}%"))
    if query:
        search_str = f"%{query}%"
        q = q.filter(
            or_(
                Airport.iata.ilike(search_str),
                Airport.icao.ilike(search_str),
                Airport.name.ilike(search_str),
                Airport.city.ilike(search_str)
            )
        )
    return q.order_by(Airport.iata.asc()).limit(limit).all()

@router.get("/{code}", response_model=AirportResponse)
def get_airport_by_code(code: str, db: Session = Depends(get_db)):
    code_upper = code.upper()
    ap = db.query(Airport).filter(
        or_(Airport.iata == code_upper, Airport.icao == code_upper)
    ).first()
    if not ap:
        raise HTTPException(status_code=404, detail=f"Airport '{code}' not found")
    return ap

@router.get("/{code}/weather", response_model=List[WeatherResponse])
def get_airport_weather(code: str, limit: int = 10, db: Session = Depends(get_db)):
    code_upper = code.upper()
    ap = db.query(Airport).filter(
        or_(Airport.iata == code_upper, Airport.icao == code_upper)
    ).first()
    if not ap:
        raise HTTPException(status_code=404, detail=f"Airport '{code}' not found")

    reports = db.query(Weather).filter(Weather.airport_id == ap.id).order_by(Weather.recorded_at.desc()).limit(limit).all()
    return reports
