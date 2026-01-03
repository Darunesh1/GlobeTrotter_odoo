from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.database import get_db
from app.models.city import City
from app.models.stop import Stop
from app.models.trip import Trip
from app.models.user import User
from app.schemas.stop import StopCreate, StopResponse, StopUpdate, StopWithCityResponse

router = APIRouter()


@router.post(
    "/trips/{trip_id}/stops",
    response_model=StopWithCityResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_stop_to_trip(
    trip_id: int,
    stop_data: StopCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Add a city stop to a trip"""
    # Verify trip exists and belongs to user
    trip = (
        db.query(Trip)
        .filter(Trip.id == trip_id, Trip.user_id == current_user.id)
        .first()
    )

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )

    # Verify city exists
    city = db.query(City).filter(City.id == stop_data.city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    # Validate dates
    if stop_data.start_date >= stop_data.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date",
        )

    # Check if dates are within trip dates
    if stop_data.start_date < trip.start_date or stop_data.end_date > trip.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Stop dates must be within trip dates",
        )

    # Get next order number
    max_order = db.query(Stop).filter(Stop.trip_id == trip_id).count()

    new_stop = Stop(
        trip_id=trip_id,
        city_id=stop_data.city_id,
        start_date=stop_data.start_date,
        end_date=stop_data.end_date,
        notes=stop_data.notes,
        order=max_order + 1,
    )

    db.add(new_stop)
    db.commit()
    db.refresh(new_stop)

    return new_stop


@router.get("/trips/{trip_id}/stops", response_model=List[StopWithCityResponse])
def get_trip_stops(
    trip_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get all stops for a trip"""
    # Verify trip exists and belongs to user
    trip = (
        db.query(Trip)
        .filter(Trip.id == trip_id, Trip.user_id == current_user.id)
        .first()
    )

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )

    stops = db.query(Stop).filter(Stop.trip_id == trip_id).order_by(Stop.order).all()

    return stops


@router.get("/stops/{stop_id}", response_model=StopWithCityResponse)
def get_stop(
    stop_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Get single stop details"""
    stop = db.query(Stop).filter(Stop.id == stop_id).first()

    if not stop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found"
        )

    # Verify user owns the trip
    trip = (
        db.query(Trip)
        .filter(Trip.id == stop.trip_id, Trip.user_id == current_user.id)
        .first()
    )

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found"
        )

    return stop


@router.put("/stops/{stop_id}", response_model=StopWithCityResponse)
def update_stop(
    stop_id: int,
    stop_data: StopUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Update a stop"""
    stop = db.query(Stop).filter(Stop.id == stop_id).first()

    if not stop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found"
        )

    # Verify user owns the trip
    trip = (
        db.query(Trip)
        .filter(Trip.id == stop.trip_id, Trip.user_id == current_user.id)
        .first()
    )

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found"
        )

    # Update fields
    update_data = stop_data.model_dump(exclude_unset=True)

    # Validate dates if provided
    start = update_data.get("start_date", stop.start_date)
    end = update_data.get("end_date", stop.end_date)
    if start >= end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date",
        )

    for key, value in update_data.items():
        setattr(stop, key, value)

    db.commit()
    db.refresh(stop)

    return stop


@router.delete("/stops/{stop_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_stop(
    stop_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Delete a stop"""
    stop = db.query(Stop).filter(Stop.id == stop_id).first()

    if not stop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found"
        )

    # Verify user owns the trip
    trip = (
        db.query(Trip)
        .filter(Trip.id == stop.trip_id, Trip.user_id == current_user.id)
        .first()
    )

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found"
        )

    db.delete(stop)
    db.commit()

    return None
