from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TripBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: datetime
    end_date: datetime
    cover_photo: Optional[str] = None


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    cover_photo: Optional[str] = None


class TripResponse(TripBase):
    id: int
    user_id: int
    is_public: int
    share_token: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
