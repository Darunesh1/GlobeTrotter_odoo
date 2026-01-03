from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import activities, admin, auth, budget, cities, stops, trips
from app.database import Base, SessionLocal, engine
from app.models import City, Stop, Trip, User
from app.utils.auth import get_password_hash


# Startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables and admin user
    Base.metadata.create_all(bind=engine)

    # Auto-create admin user if not exists
    db = SessionLocal()
    try:
        admin_exists = db.query(User).filter(User.role == "admin").first()
        if not admin_exists:
            admin_user = User(
                email="admin@globetrotter.com",
                username="admin",
                hashed_password=get_password_hash("admin123"),
                full_name="System Admin",
                role="admin",
                is_verified=True,
            )
            db.add(admin_user)
            db.commit()
            print("✓ Admin user created: admin@globetrotter.com / admin123")
            print("  ⚠️  CHANGE PASSWORD IN PRODUCTION!")
        else:
            print("✓ Admin user already exists")
    finally:
        db.close()

    yield  # App runs here

    # Shutdown logic (if needed)
    print("Shutting down...")


app = FastAPI(
    title="GlobeTrotter API",
    description="Travel planning API for multi-city itineraries",
    version="1.0.0",
    lifespan=lifespan,  # ADD THIS
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(trips.router, prefix="/trips", tags=["Trips"])
app.include_router(cities.router, prefix="/cities", tags=["Cities"])
app.include_router(stops.router, prefix="", tags=["Stops"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(activities.router, prefix="/api/v1/activities", tags=["activities"])
app.include_router(budget.router, prefix="/api/v1/budget", tags=["budget"])


@app.get("/")
def root():
    return {"message": "GlobeTrotter API", "version": "1.0.0", "docs": "/docs"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
