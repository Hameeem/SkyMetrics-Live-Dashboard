import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import engine, SessionLocal, Base
from backend.models.models import Airport, Weather, LiveFlight, HistoricalFlight, User
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data
    db.query(LiveFlight).delete()
    db.query(HistoricalFlight).delete()
    db.query(Weather).delete()
    db.query(Airport).delete()
    db.query(User).delete()
    db.commit()

    # Seed Indian and International Hub Airports (including SXR, DHM, Tamil Nadu & Punjab)
    airports_data = [
        {"iata": "DEL", "icao": "VIDP", "name": "Indira Gandhi International Airport", "city": "New Delhi", "country": "India", "latitude": 28.5562, "longitude": 77.1000, "altitude_ft": 777, "runways_count": 4},
        {"iata": "BOM", "icao": "VABB", "name": "Chhatrapati Shivaji Maharaj International Airport", "city": "Mumbai", "country": "India", "latitude": 19.0896, "longitude": 72.8656, "altitude_ft": 39, "runways_count": 2},
        {"iata": "BLR", "icao": "VOBL", "name": "Kempegowda International Airport", "city": "Bengaluru", "country": "India", "latitude": 13.1986, "longitude": 77.7066, "altitude_ft": 3000, "runways_count": 2},
        {"iata": "MAA", "icao": "VOMM", "name": "Chennai International Airport", "city": "Chennai", "country": "India", "latitude": 12.9941, "longitude": 80.1709, "altitude_ft": 52, "runways_count": 2},
        {"iata": "HYD", "icao": "VOHS", "name": "Rajiv Gandhi International Airport", "city": "Hyderabad", "country": "India", "latitude": 17.2403, "longitude": 78.4294, "altitude_ft": 2024, "runways_count": 2},
        {"iata": "CCU", "icao": "VECC", "name": "Netaji Subhash Chandra Bose International Airport", "city": "Kolkata", "country": "India", "latitude": 22.6547, "longitude": 88.4467, "altitude_ft": 16, "runways_count": 2},
        {"iata": "AMD", "icao": "VAAH", "name": "Sardar Vallabhbhai Patel International Airport", "city": "Ahmedabad", "country": "India", "latitude": 23.0772, "longitude": 72.6347, "altitude_ft": 189, "runways_count": 1},
        
        # SXR (Srinagar), DHM (Dharamshala), Punjab (Amritsar ATQ, Chandigarh IXC), Tamil Nadu (Tiruchirappalli TRZ, Coimbatore CJB, Madurai IXM)
        {"iata": "SXR", "icao": "VISR", "name": "Sheikh ul-Alam International Airport", "city": "Srinagar", "country": "India", "latitude": 33.9872, "longitude": 74.7741, "altitude_ft": 5458, "runways_count": 1},
        {"iata": "DHM", "icao": "VIGG", "name": "Kangra Gaggal Airport", "city": "Dharamshala", "country": "India", "latitude": 32.1651, "longitude": 76.2634, "altitude_ft": 2525, "runways_count": 1},
        {"iata": "ATQ", "icao": "VIAR", "name": "Sri Guru Ram Dass Jee International Airport", "city": "Amritsar", "country": "India", "latitude": 31.7096, "longitude": 74.7973, "altitude_ft": 756, "runways_count": 1},
        {"iata": "IXC", "icao": "VICG", "name": "Shaheed Bhagat Singh International Airport", "city": "Chandigarh", "country": "India", "latitude": 30.6735, "longitude": 76.7885, "altitude_ft": 1012, "runways_count": 1},
        {"iata": "TRZ", "icao": "VOTR", "name": "Tiruchirappalli International Airport", "city": "Tiruchirappalli", "country": "India", "latitude": 10.7654, "longitude": 78.7097, "altitude_ft": 288, "runways_count": 1},
        {"iata": "CJB", "icao": "VOCB", "name": "Coimbatore International Airport", "city": "Coimbatore", "country": "India", "latitude": 11.0300, "longitude": 77.0434, "altitude_ft": 1319, "runways_count": 1},
        {"iata": "IXM", "icao": "VOMD", "name": "Madurai Airport", "city": "Madurai", "country": "India", "latitude": 9.8345, "longitude": 78.0934, "altitude_ft": 463, "runways_count": 1},
        
        # International Hubs
        {"iata": "LHR", "icao": "EGLL", "name": "London Heathrow Airport", "city": "London", "country": "United Kingdom", "latitude": 51.4700, "longitude": -0.4543, "altitude_ft": 83, "runways_count": 2},
        {"iata": "JFK", "icao": "KJFK", "name": "John F. Kennedy International Airport", "city": "New York", "country": "United States", "latitude": 40.6413, "longitude": -73.7781, "altitude_ft": 13, "runways_count": 4},
        {"iata": "DXB", "icao": "OMDB", "name": "Dubai International Airport", "city": "Dubai", "country": "United Arab Emirates", "latitude": 25.2532, "longitude": 55.3657, "altitude_ft": 62, "runways_count": 2},
        {"iata": "SIN", "icao": "WSSS", "name": "Singapore Changi Airport", "city": "Singapore", "country": "Singapore", "latitude": 1.3644, "longitude": 103.9915, "altitude_ft": 22, "runways_count": 3}
    ]

    for ap in airports_data:
        db.add(Airport(**ap))
    db.commit()

    # Seed Sample Live Flights connecting DEL, BOM, SXR, DHM, ATQ, IXC, TRZ, CJB, IXM
    callsigns = [
        ("800101", "AIC101", "DEL", "BOM", 28.55, 77.10, 10500, 240, 190, "EN_ROUTE"),
        ("800505", "IGO505", "DEL", "SXR", 31.20, 75.80, 9800, 220, 340, "EN_ROUTE"),
        ("800811", "VTI811", "BOM", "ATQ", 24.50, 73.80, 11200, 250, 15, "EN_ROUTE"),
        ("800404", "SEJ404", "DEL", "DHM", 30.50, 76.50, 6500, 180, 20, "EN_ROUTE"),
        ("800202", "AKJ202", "BLR", "MAA", 13.00, 78.50, 7500, 210, 85, "EN_ROUTE"),
        ("800612", "IGO612", "MAA", "TRZ", 11.80, 79.40, 5500, 190, 210, "EN_ROUTE"),
        ("800441", "AIC441", "DEL", "IXC", 29.80, 76.90, 4800, 175, 350, "ON_APPROACH"),
        ("800711", "SEJ711", "MAA", "CJB", 12.00, 78.60, 6200, 195, 250, "EN_ROUTE"),
        ("800309", "IGO309", "MAA", "IXM", 11.00, 79.00, 5800, 185, 200, "EN_ROUTE"),
        ("800121", "AIC121", "DEL", "LHR", 35.00, 65.00, 11500, 260, 290, "DELAYED")
    ]

    for icao24, cs, orig, dest, lat, lon, alt, vel, hdg, st in callsigns:
        db.add(LiveFlight(
            icao24=icao24,
            callsign=cs,
            origin_iata=orig,
            destination_iata=dest,
            latitude=lat,
            longitude=lon,
            altitude_m=alt,
            velocity_mps=vel,
            heading_deg=hdg,
            status=st,
            origin_country="India",
            last_contact=datetime.now(timezone.utc)
        ))
    db.commit()

    print("Database successfully seeded with SXR, DHM, Tamil Nadu & Punjab airports!")

if __name__ == "__main__":
    seed_database()
