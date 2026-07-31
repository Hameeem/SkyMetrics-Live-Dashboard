import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
import random
from sqlalchemy.orm import Session
from database.connection import engine, SessionLocal, Base

from backend.models.models import (
    User, Airport, Weather, LiveFlight, HistoricalFlight,
    Prediction, Alert, ETLLog, UserPreference, AnalyticsCache, AuditLog
)
from backend.core.security import get_password_hash

AIRPORTS_DATA = [
    {"iata": "DEL", "icao": "VIDP", "name": "Indira Gandhi International Airport", "city": "Delhi", "country": "India", "latitude": 28.5562, "longitude": 77.1000, "altitude_ft": 777.0, "runways": 4},
    {"iata": "BOM", "icao": "VABB", "name": "Chhatrapati Shivaji Maharaj Int'l", "city": "Mumbai", "country": "India", "latitude": 19.0896, "longitude": 72.8656, "altitude_ft": 37.0, "runways": 2},
    {"iata": "BLR", "icao": "VOBL", "name": "Kempegowda International Airport", "city": "Bengaluru", "country": "India", "latitude": 13.1986, "longitude": 77.7066, "altitude_ft": 3000.0, "runways": 2},
    {"iata": "MAA", "icao": "VOMM", "name": "Chennai International Airport", "city": "Chennai", "country": "India", "latitude": 12.9941, "longitude": 80.1709, "altitude_ft": 52.0, "runways": 2},
    {"iata": "CCU", "icao": "VECC", "name": "Netaji Subhash Chandra Bose Int'l", "city": "Kolkata", "country": "India", "latitude": 22.6547, "longitude": 88.4467, "altitude_ft": 16.0, "runways": 2},
    {"iata": "HYD", "icao": "VOHS", "name": "Rajiv Gandhi International Airport", "city": "Hyderabad", "country": "India", "latitude": 17.2403, "longitude": 78.4294, "altitude_ft": 2024.0, "runways": 2},
    {"iata": "AMD", "icao": "VAAH", "name": "Sardar Vallabhbhai Patel Int'l", "city": "Ahmedabad", "country": "India", "latitude": 23.0772, "longitude": 72.6347, "altitude_ft": 189.0, "runways": 1},
    {"iata": "ATL", "icao": "KATL", "name": "Hartsfield-Jackson Atlanta Int'l Airport", "city": "Atlanta", "country": "United States", "latitude": 33.6407, "longitude": -84.4277, "altitude_ft": 1026.0, "runways": 5},
    {"iata": "LHR", "icao": "EGLL", "name": "London Heathrow Airport", "city": "London", "country": "United Kingdom", "latitude": 51.4700, "longitude": -0.4543, "altitude_ft": 83.0, "runways": 2},
    {"iata": "HND", "icao": "RJTT", "name": "Tokyo Haneda Airport", "city": "Tokyo", "country": "Japan", "latitude": 35.5494, "longitude": 139.7798, "altitude_ft": 35.0, "runways": 4},
    {"iata": "DXB", "icao": "OMDB", "name": "Dubai International Airport", "city": "Dubai", "country": "United Arab Emirates", "latitude": 25.2532, "longitude": 55.3657, "altitude_ft": 62.0, "runways": 2},
    {"iata": "ORD", "icao": "KORD", "name": "Chicago O'Hare International Airport", "city": "Chicago", "country": "United States", "latitude": 41.9742, "longitude": -87.9073, "altitude_ft": 668.0, "runways": 8},
    {"iata": "CDG", "icao": "LFPG", "name": "Paris Charles de Gaulle Airport", "city": "Paris", "country": "France", "latitude": 49.0097, "longitude": 2.5479, "altitude_ft": 392.0, "runways": 4},
    {"iata": "SIN", "icao": "WSSS", "name": "Singapore Changi Airport", "city": "Singapore", "country": "Singapore", "latitude": 1.3644, "longitude": 103.9915, "altitude_ft": 22.0, "runways": 3},
    {"iata": "JFK", "icao": "KJFK", "name": "John F. Kennedy International Airport", "city": "New York", "country": "United States", "latitude": 40.6413, "longitude": -73.7781, "altitude_ft": 13.0, "runways": 4},
    {"iata": "SYD", "icao": "YSSY", "name": "Sydney Kingsford Smith Airport", "city": "Sydney", "country": "Australia", "latitude": -33.9461, "longitude": 151.1772, "altitude_ft": 21.0, "runways": 3},
    {"iata": "FRA", "icao": "EDDF", "name": "Frankfurt Airport", "city": "Frankfurt", "country": "Germany", "latitude": 50.0379, "longitude": 8.5622, "altitude_ft": 364.0, "runways": 4},
    {"iata": "AMS", "icao": "EHAM", "name": "Amsterdam Airport Schiphol", "city": "Amsterdam", "country": "Netherlands", "latitude": 52.3105, "longitude": 4.7683, "altitude_ft": -11.0, "runways": 6},
    {"iata": "LAX", "icao": "KLAX", "name": "Los Angeles International Airport", "city": "Los Angeles", "country": "United States", "latitude": 33.9416, "longitude": -118.4085, "altitude_ft": 128.0, "runways": 4},
    {"iata": "SFO", "icao": "KSFO", "name": "San Francisco International Airport", "city": "San Francisco", "country": "United States", "latitude": 37.6213, "longitude": -122.3790, "altitude_ft": 13.0, "runways": 4}
]

AIRLINES = ["Air India", "IndiGo", "Vistara", "SpiceJet", "Akasa Air", "Emirates", "British Airways", "United Airlines", "Lufthansa", "Singapore Airlines", "Qantas"]

AIRCRAFT_TYPES = ["Boeing 737-800", "Boeing 777-300ER", "Boeing 787-9", "Airbus A320neo", "Airbus A350-900", "Airbus A380-800"]

def init_db():
    Base.metadata.create_all(bind=engine)

def seed_database():
    init_db()
    db: Session = SessionLocal()

    try:
        # Check if users already exist
        if db.query(User).count() > 0:
            print("Database already seeded.")
            return

        print("Seeding users...")
        users = [
            User(username="admin", email="admin@skymetrics.ai", hashed_password=get_password_hash("AdminPassword123!"), role="admin"),
            User(username="analyst", email="analyst@skymetrics.ai", hashed_password=get_password_hash("AnalystPassword123!"), role="analyst"),
            User(username="viewer", email="viewer@skymetrics.ai", hashed_password=get_password_hash("ViewerPassword123!"), role="viewer"),
        ]
        db.add_all(users)
        db.commit()

        print("Seeding user preferences...")
        for u in users:
            db.add(UserPreference(user_id=u.id, theme="dark", default_airport="LHR", email_notifications=True))
        db.commit()

        print("Seeding airports...")
        airport_objs = []
        for a in AIRPORTS_DATA:
            airport_obj = Airport(
                iata=a["iata"],
                icao=a["icao"],
                name=a["name"],
                city=a["city"],
                country=a["country"],
                latitude=a["latitude"],
                longitude=a["longitude"],
                altitude_ft=a["altitude_ft"],
                runways_count=a["runways"]
            )
            airport_objs.append(airport_obj)
            db.add(airport_obj)
        db.commit()

        print("Seeding weather data...")
        now = datetime.datetime.utcnow()
        conditions = ["Clear", "Partly Cloudy", "Overcast", "Light Rain", "Thunderstorm", "Fog", "Strong Winds"]
        for ap in airport_objs:
            # Add current & past weather records
            for hours_back in [0, 1, 3, 6, 12, 24]:
                w = Weather(
                    airport_id=ap.id,
                    temperature_c=round(random.uniform(5.0, 35.0), 1),
                    wind_speed_kts=round(random.uniform(2.0, 35.0), 1),
                    wind_direction_deg=round(random.uniform(0, 360), 0),
                    visibility_km=round(random.uniform(1.0, 10.0), 1),
                    humidity_pct=round(random.uniform(30.0, 95.0), 1),
                    pressure_hpa=round(random.uniform(995.0, 1025.0), 1),
                    condition_text=random.choice(conditions),
                    recorded_at=now - datetime.timedelta(hours=hours_back)
                )
                db.add(w)
        db.commit()

        print("Seeding live flights...")
        callsigns = [
            "AIC101", "IGO505", "VTI811", "SEJ404", "AKJ202",
            "AIC302", "IGO214", "VTI920", "IGO808", "AIC129",
            "BAW117", "DAL241", "UAE003", "UAL901", "DLH400", "SIA321"
        ]
        for idx, cs in enumerate(callsigns * 3):

            orig = random.choice(AIRPORTS_DATA)
            dest = random.choice([a for a in AIRPORTS_DATA if a["iata"] != orig["iata"]])
            # Interpolate position between origin and dest
            progress = random.uniform(0.1, 0.9)
            lat = orig["latitude"] + (dest["latitude"] - orig["latitude"]) * progress
            lon = orig["longitude"] + (dest["longitude"] - orig["longitude"]) * progress

            lf = LiveFlight(
                icao24=f"a{idx:05x}",
                callsign=f"{cs}{idx}",
                origin_country=orig["country"],
                origin_iata=orig["iata"],
                destination_iata=dest["iata"],
                latitude=round(lat, 4),
                longitude=round(lon, 4),
                altitude_m=round(random.uniform(3000, 12000), 1),
                velocity_mps=round(random.uniform(180, 260), 1),
                heading_deg=round(random.uniform(0, 360), 1),
                vertical_rate_mps=round(random.uniform(-5, 5), 1),
                on_ground=False,
                status=random.choice(["EN_ROUTE", "EN_ROUTE", "EN_ROUTE", "ON_APPROACH", "DELAYED"]),
                last_contact=now
            )
            db.add(lf)
        db.commit()

        print("Seeding historical flights (500 records)...")
        for i in range(500):
            orig = random.choice(AIRPORTS_DATA)
            dest = random.choice([a for a in AIRPORTS_DATA if a["iata"] != orig["iata"]])
            airline = random.choice(AIRLINES)
            days_ago = random.randint(0, 30)
            sched_dep = now - datetime.timedelta(days=days_ago, hours=random.randint(1, 23))
            delay_mins = max(0.0, random.normalvariate(18.0, 25.0)) if random.random() < 0.35 else 0.0
            act_dep = sched_dep + datetime.timedelta(minutes=delay_mins)
            duration_mins = random.randint(90, 600)
            sched_arr = sched_dep + datetime.timedelta(minutes=duration_mins)
            act_arr = act_dep + datetime.timedelta(minutes=duration_mins)

            hf = HistoricalFlight(
                flight_number=f"{airline[:3].upper()}{random.randint(100, 999)}",
                airline=airline,
                origin_iata=orig["iata"],
                destination_iata=dest["iata"],
                scheduled_departure=sched_dep,
                actual_departure=act_dep,
                scheduled_arrival=sched_arr,
                actual_arrival=act_arr,
                delay_minutes=round(delay_mins, 1),
                is_delayed=delay_mins > 15.0,
                distance_km=round(random.uniform(500, 10000), 1),
                aircraft_type=random.choice(AIRCRAFT_TYPES),
                status="COMPLETED"
            )
            db.add(hf)
        db.commit()

        print("Seeding alerts & ETL logs...")
        db.add(Alert(
            user_id=users[0].id,
            title="LHR Heavy Wind Delay Threshold",
            alert_type="WEATHER_WARNING",
            target_airport="LHR",
            threshold_value=25.0,
            is_active=True,
            triggered_count=3,
            last_triggered=now - datetime.timedelta(hours=2)
        ))
        db.add(Alert(
            user_id=users[1].id,
            title="DEL Arrival Delay Alert (>30 mins)",
            alert_type="DELAY_THRESHOLD",
            target_airport="DEL",
            threshold_value=30.0,
            is_active=True,
            triggered_count=5,
            last_triggered=now - datetime.timedelta(hours=5)
        ))

        db.add(ETLLog(
            dag_id="fetch_live_flights_dag",
            task_id="extract_opensky",
            status="SUCCESS",
            records_processed=45,
            execution_time_sec=1.42,
            executed_at=now - datetime.timedelta(minutes=10)
        ))
        db.add(ETLLog(
            dag_id="fetch_weather_dag",
            task_id="extract_openweather",
            status="SUCCESS",
            records_processed=20,
            execution_time_sec=2.15,
            executed_at=now - datetime.timedelta(minutes=15)
        ))

        db.commit()
        print("Database seed completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
