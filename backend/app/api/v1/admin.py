from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_admin_user
from app.database import get_db
from app.models.city import City
from app.models.stop import Stop
from app.models.trip import Trip
from app.models.user import User

router = APIRouter()


@router.get("/analytics")
def get_analytics(
    current_admin: User = Depends(get_current_admin_user), db: Session = Depends(get_db)
):
    """Admin dashboard analytics"""

    # User stats
    total_users = db.query(func.count(User.id)).scalar()
    verified_users = (
        db.query(func.count(User.id)).filter(User.is_verified == True).scalar()
    )

    # Trip stats
    total_trips = db.query(func.count(Trip.id)).scalar()
    public_trips = db.query(func.count(Trip.id)).filter(Trip.is_public == 1).scalar()

    # Popular cities (most visited)
    popular_cities = (
        db.query(City.name, City.country, func.count(Stop.id).label("visit_count"))
        .join(Stop, Stop.city_id == City.id)
        .group_by(City.id)
        .order_by(func.count(Stop.id).desc())
        .limit(10)
        .all()
    )

    # Recent trips
    recent_trips = db.query(Trip).order_by(Trip.created_at.desc()).limit(10).all()

    return {
        "users": {
            "total": total_users,
            "verified": verified_users,
            "unverified": total_users - verified_users,
        },
        "trips": {
            "total": total_trips,
            "public": public_trips,
            "private": total_trips - public_trips,
        },
        "popular_cities": [
            {"name": city.name, "country": city.country, "visits": count}
            for city, count in popular_cities
        ],
        "recent_trips": [
            {
                "id": trip.id,
                "name": trip.name,
                "user_id": trip.user_id,
                "created_at": trip.created_at,
            }
            for trip in recent_trips
        ],
    }


@router.get("/users")
def get_all_users(
    current_admin: User = Depends(get_current_admin_user), db: Session = Depends(get_db)
):
    """Get all users (admin only)"""
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "role": user.role,
            "is_verified": user.is_verified,
            "created_at": user.created_at,
        }
        for user in users
    ]


@router.get("/trips")
def get_all_trips(
    current_admin: User = Depends(get_current_admin_user), db: Session = Depends(get_db)
):
    """Get all trips (admin only)"""
    trips = db.query(Trip).all()
    return trips
