from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.connection import get_db
from backend.models.models import LiveFlight, HistoricalFlight
from backend.schemas.schemas import LiveFlightResponse, HistoricalFlightResponse

router = APIRouter(prefix="/api/v1/flights", tags=["Flights"])

@router.get("/live", response_model=List[LiveFlightResponse])
def get_live_flights(
    origin: Optional[str] = Query(None, description="Origin IATA code"),
    destination: Optional[str] = Query(None, description="Destination IATA code"),
    country: Optional[str] = Query(None, description="Origin Country"),
    status: Optional[str] = Query(None, description="Flight status"),
    min_altitude: Optional[float] = Query(None, description="Minimum altitude in meters"),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    query = db.query(LiveFlight)
    if origin:
        query = query.filter(LiveFlight.origin_iata == origin.upper())
    if destination:
        query = query.filter(LiveFlight.destination_iata == destination.upper())
    if country:
        query = query.filter(LiveFlight.origin_country.ilike(f"%{country}%"))
    if status:
        query = query.filter(LiveFlight.status == status.upper())
    if min_altitude is not None:
        query = query.filter(LiveFlight.altitude_m >= min_altitude)

    return query.order_by(LiveFlight.last_contact.desc()).limit(limit).all()

@router.get("/history", response_model=List[HistoricalFlightResponse])
def get_historical_flights(
    airline: Optional[str] = None,
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    is_delayed: Optional[bool] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(HistoricalFlight)
    if airline:
        query = query.filter(HistoricalFlight.airline.ilike(f"%{airline}%"))
    if origin:
        query = query.filter(HistoricalFlight.origin_iata == origin.upper())
    if destination:
        query = query.filter(HistoricalFlight.destination_iata == destination.upper())
    if is_delayed is not None:
        query = query.filter(HistoricalFlight.is_delayed == is_delayed)

    return query.order_by(HistoricalFlight.scheduled_departure.desc()).limit(limit).all()

@router.get("/search")
def search_flights(query: str = Query(..., min_length=2), db: Session = Depends(get_db)):
    q = f"%{query}%"
    live_matches = db.query(LiveFlight).filter(
        or_(
            LiveFlight.callsign.ilike(q),
            LiveFlight.icao24.ilike(q),
            LiveFlight.origin_iata.ilike(q),
            LiveFlight.destination_iata.ilike(q),
            LiveFlight.origin_country.ilike(q)
        )
    ).limit(30).all()

    hist_matches = db.query(HistoricalFlight).filter(
        or_(
            HistoricalFlight.flight_number.ilike(q),
            HistoricalFlight.airline.ilike(q),
            HistoricalFlight.origin_iata.ilike(q),
            HistoricalFlight.destination_iata.ilike(q)
        )
    ).limit(30).all()

    return {
        "query": query,
        "live_flights": [LiveFlightResponse.model_validate(f) for f in live_matches],
        "historical_flights": [HistoricalFlightResponse.model_validate(f) for f in hist_matches]
    }

@router.get("/details/{identifier}")
def get_flight_details(identifier: str, db: Session = Depends(get_db)):
    lf = db.query(LiveFlight).filter(
        or_(LiveFlight.callsign == identifier.upper(), LiveFlight.icao24 == identifier.lower())
    ).first()

    if lf:
        return {"type": "live", "flight": LiveFlightResponse.model_validate(lf)}

    hf = db.query(HistoricalFlight).filter(HistoricalFlight.flight_number == identifier.upper()).first()
    if hf:
        return {"type": "historical", "flight": HistoricalFlightResponse.model_validate(hf)}

    raise HTTPException(status_code=404, detail=f"Flight '{identifier}' not found in live or historical records.")
