import secrets
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.database import get_db
from app.models.activity import StopActivity
from app.models.stop import Stop
from app.models.trip import Trip
from app.models.user import User
from app.schemas.trip import TripCreate, TripResponse, TripUpdate

router = APIRouter()


@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    trip_data: TripCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    # Validate dates
    if trip_data.start_date >= trip_data.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date",
        )

    new_trip = Trip(
        name=trip_data.name,
        description=trip_data.description,
        start_date=trip_data.start_date,
        end_date=trip_data.end_date,
        cover_photo=trip_data.cover_photo,
        user_id=current_user.id,
    )

    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    return new_trip


@router.get("/", response_model=List[TripResponse])
def get_all_trips(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    trips = db.query(Trip).filter(Trip.user_id == current_user.id).all()
    return trips


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    trip = (
        db.query(Trip)
        .filter(Trip.id == trip_id, Trip.user_id == current_user.id)
        .first()
    )

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )

    return trip


@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: int,
    trip_data: TripUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    trip = (
        db.query(Trip)
        .filter(Trip.id == trip_id, Trip.user_id == current_user.id)
        .first()
    )

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )

    # Update only provided fields
    update_data = trip_data.model_dump(exclude_unset=True)

    # Validate dates if both are provided
    start = update_data.get("start_date", trip.start_date)
    end = update_data.get("end_date", trip.end_date)
    if start >= end:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date",
        )

    for key, value in update_data.items():
        setattr(trip, key, value)

    db.commit()
    db.refresh(trip)

    return trip


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    trip_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    trip = (
        db.query(Trip)
        .filter(Trip.id == trip_id, Trip.user_id == current_user.id)
        .first()
    )

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found"
        )

    db.delete(trip)
    db.commit()

    return None


@router.get("/share/{share_token}", response_model=TripResponse)
def get_shared_trip(share_token: str, db: Session = Depends(get_db)):
    """
    Get a trip by its public share token.
    Does NOT require authentication.
    """
    trip = db.query(Trip).filter(Trip.share_token == share_token).first()

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trip not found or invalid token",
        )

    if not trip.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This trip is currently private",
        )

    return trip


@router.put("/{trip_id}/share", response_model=TripResponse)
def toggle_trip_sharing(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Toggle trip public status and generate token if needed"""
    trip = (
        db.query(Trip)
        .filter(Trip.id == trip_id, Trip.user_id == current_user.id)
        .first()
    )

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    # Toggle status
    if trip.is_public:
        trip.is_public = False  # Turn off
    else:
        trip.is_public = True  # Turn on
        if not trip.share_token:
            # Generate a secure random token
            trip.share_token = secrets.token_urlsafe(16)

    db.commit()
    db.refresh(trip)
    return trip


@router.post(
    "/{trip_id}/copy", response_model=TripResponse, status_code=status.HTTP_201_CREATED
)
def copy_trip(
    trip_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """Clone an existing public trip to the current user's account"""
    # 1. Fetch original trip (must be public OR owned by user)
    original_trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not original_trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if not original_trip.is_public and original_trip.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot copy private trip")

    # 2. Create new Trip shell
    new_trip = Trip(
        name=f"Copy of {original_trip.name}",
        description=original_trip.description,
        start_date=original_trip.start_date,  # User usually updates this later
        end_date=original_trip.end_date,
        cover_photo=original_trip.cover_photo,
        user_id=current_user.id,
        is_public=False,  # New copy starts private
    )
    db.add(new_trip)
    db.commit()
    db.refresh(new_trip)

    # 3. Clone Stops
    original_stops = db.query(Stop).filter(Stop.trip_id == original_trip.id).all()

    for old_stop in original_stops:
        new_stop = Stop(
            trip_id=new_trip.id,
            city_id=old_stop.city_id,
            start_date=old_stop.start_date,
            end_date=old_stop.end_date,
            notes=old_stop.notes,
            order=old_stop.order,
            transport_cost=old_stop.transport_cost,  # New field (see below)
        )
        db.add(new_stop)
        db.commit()  # Commit to get new_stop.id

        # 4. Clone Activities for this stop
        old_activities = (
            db.query(StopActivity).filter(StopActivity.stop_id == old_stop.id).all()
        )
        for old_act in old_activities:
            new_act = StopActivity(
                stop_id=new_stop.id,
                activity_id=old_act.activity_id,
                actual_cost=old_act.actual_cost,
            )
            db.add(new_act)

    db.commit()
    return new_trip
