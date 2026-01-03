# app/api/v1/budget.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.database import get_db
from app.models.activity import StopActivity
from app.models.city import City
from app.models.stop import Stop
from app.models.trip import Trip

router = APIRouter()


@router.get("/{trip_id}")
def get_trip_budget(
    trip_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # 1. Verify Ownership
    trip = (
        db.query(Trip)
        .filter(Trip.id == trip_id, Trip.user_id == current_user.id)
        .first()
    )
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # 2. Calculate Costs
    stops = db.query(Stop).filter(Stop.trip_id == trip_id).all()

    total_accommodation = 0.0
    total_activities = 0.0
    breakdown = []

    for stop in stops:
        # Calculate Duration (simple difference in days)
        duration = (stop.end_date - stop.start_date).days
        duration = max(duration, 1)  # Minimum 1 day

        # Accommodation (City Cost * Days)
        city = db.query(City).filter(City.id == stop.city_id).first()
        acc_cost = (city.avg_cost_per_day or 0) * duration
        total_accommodation += acc_cost

        # Activities Cost for this stop
        activities = (
            db.query(StopActivity).filter(StopActivity.stop_id == stop.id).all()
        )
        act_cost = sum(a.actual_cost or 0 for a in activities)
        total_activities += act_cost

        breakdown.append(
            {
                "city": city.name,
                "days": duration,
                "accommodation": acc_cost,
                "activities": act_cost,
                "subtotal": acc_cost + act_cost,
            }
        )

    return {
        "total_budget": total_accommodation + total_activities,
        "categories": {
            "accommodation": total_accommodation,
            "activities": total_activities,
            "transport": 0.0,  # Placeholder (requires transport feature)
        },
        "breakdown": breakdown,
    }
