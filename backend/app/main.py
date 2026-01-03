from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth, cities, stops, trips
from app.database import Base, engine
from app.models import User  # Import all models

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GlobeTrotter API",
    description="Travel planning API for multi-city itineraries",
    version="1.0.0",
)

# CORS - Allow Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(trips.router, prefix="/trips", tags=["Trips"])
app.include_router(cities.router, prefix="/cities", tags=["Cities"])
app.include_router(stops.router, prefix="", tags=["Stops"])


@app.get("/")
def root():
    return {"message": "GlobeTrotter API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
