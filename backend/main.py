import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.core.config import settings
from database.connection import engine, Base
from database.seed_data import seed_database
from backend.routers import auth, flights, airports, weather, predictions, dashboard, alerts, admin, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB & Seed Data on Startup
    print("Initializing SkyMetrics Data Warehouse...")
    try:
        Base.metadata.create_all(bind=engine)
        seed_database()
    except Exception as e:
        print(f"Startup database initialization warning: {e}")
    yield
    print("Shutting down SkyMetrics backend...")

app = FastAPI(
    title="SkyMetrics API",
    description="Enterprise Aviation Analytics & Flight Intelligence Platform REST API",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={"deepLinking": True}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(flights.router)
app.include_router(airports.router)
app.include_router(weather.router)
app.include_router(predictions.router)
app.include_router(dashboard.router)
app.include_router(alerts.router)
app.include_router(admin.router)
app.include_router(health.router)

@app.get("/", tags=["Root"])
def root():
    return {
        "platform": "SkyMetrics Enterprise Flight Intelligence Platform",
        "version": "2.0.0",
        "status": "ONLINE",
        "docs_url": "/docs",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.BACKEND_HOST, port=settings.BACKEND_PORT, reload=True)
