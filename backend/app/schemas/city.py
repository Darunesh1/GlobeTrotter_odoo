from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    country: str
    region: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    avg_cost_per_day: Optional[float] = 0.0
    popularity_score: Optional[int] = 0
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    avg_cost_per_day: Optional[float] = None
    popularity_score: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CityResponse(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityListResponse(BaseModel):
    id: int
    name: str
    country: str
    image_url: Optional[str] = None
    avg_cost_per_day: float
    popularity_score: int

    class Config:
        from_attributes = True
