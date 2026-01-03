# app/api/v1/activities.py
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.database import get_db
from app.models.activity import Activity, StopActivity
from app.models.stop import Stop
from app.models.trip import Trip

router = APIRouter()


# Schema for Adding Activity to Stop
class ActivityAdd(BaseModel):
    activity_id: int
    actual_cost: Optional[float] = None  # User can override generic cost


# 1. Search Generic Activities (Public)
@router.get("/", response_model=List[dict])
def search_activities(
    city_id: Optional[int] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Activity)
    if city_id:
        query = query.filter(Activity.city_id == city_id)
    if category:
        query = query.filter(Activity.category == category)

    activities = query.limit(50).all()
    # Simple manual serialization to avoid needing a new Schema file just for this
    return [
        {
            "id": a.id,
            "name": a.name,
            "category": a.category,
            "estimated_cost": a.estimated_cost,
            "city_id": a.city_id,
        }
        for a in activities
    ]


# 2. Add Activity to a specific Stop (Protected)
@router.post("/stop/{stop_id}", status_code=status.HTTP_201_CREATED)
def add_activity_to_stop(
    stop_id: int,
    payload: ActivityAdd,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # Verify stop belongs to user
    stop = db.query(Stop).filter(Stop.id == stop_id).first()
    if not stop:
        raise HTTPException(status_code=404, detail="Stop not found")

    trip = (
        db.query(Trip)
        .filter(Trip.id == stop.trip_id, Trip.user_id == current_user.id)
        .first()
    )
    if not trip:
        raise HTTPException(status_code=403, detail="Not authorized to edit this trip")

    # Get generic cost if user didn't provide one
    activity = db.query(Activity).filter(Activity.id == payload.activity_id).first()
    cost = (
        payload.actual_cost
        if payload.actual_cost is not None
        else activity.estimated_cost
    )

    # Link it
    stop_activity = StopActivity(
        stop_id=stop_id, activity_id=payload.activity_id, actual_cost=cost
    )
    db.add(stop_activity)
    db.commit()
    return {"message": "Activity added"}
