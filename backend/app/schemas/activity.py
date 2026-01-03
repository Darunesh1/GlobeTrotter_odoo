from typing import Optional

from pydantic import BaseModel


# --- Generic Activity Schemas ---
class ActivityBase(BaseModel):
    name: str
    category: Optional[str] = "Sightseeing"
    description: Optional[str] = None
    estimated_cost: Optional[float] = 0.0
    duration_hours: Optional[float] = 1.0
    image_url: Optional[str] = None


class ActivityCreate(ActivityBase):
    city_id: int


class ActivityUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    estimated_cost: Optional[float] = None
    duration_hours: Optional[float] = None
    image_url: Optional[str] = None


class ActivityResponse(ActivityBase):
    id: int
    city_id: int

    class Config:
        from_attributes = True


# --- Stop Activity Schemas (Linking Activities to a Trip) ---


# Payload for POST /activities/stop/{stop_id}
class StopActivityAdd(BaseModel):
    activity_id: int
    actual_cost: Optional[float] = None  # User can override default cost


# Payload for Response (showing what activities are in a stop)
class StopActivityResponse(BaseModel):
    id: int
    stop_id: int
    activity: ActivityResponse  # Nested full activity details
    actual_cost: Optional[float]

    class Config:
        from_attributes = True
