from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.city import CityResponse


class StopBase(BaseModel):
    city_id: int
    start_date: datetime
    end_date: datetime
    notes: Optional[str] = None


class StopCreate(BaseModel):
    city_id: int
    start_date: datetime
    end_date: datetime
    notes: Optional[str] = None
    transport_cost: Optional[float] = 0.0


class StopUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    notes: Optional[str] = None
    order: Optional[int] = None


class StopResponse(StopBase):
    id: int
    trip_id: int
    order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StopWithCityResponse(StopResponse):
    city: CityResponse

    class Config:
        from_attributes = True
