from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.city import City
from app.schemas.city import CityListResponse, CityResponse

router = APIRouter()


@router.get("/", response_model=List[CityListResponse])
def search_cities(
    search: Optional[str] = Query(None, description="Search by city or country name"),
    country: Optional[str] = Query(None, description="Filter by country"),
    region: Optional[str] = Query(None, description="Filter by region"),
    min_cost: Optional[float] = Query(None, description="Minimum cost per day"),
    max_cost: Optional[float] = Query(None, description="Maximum cost per day"),
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
):
    """Search and filter cities"""
    query = db.query(City)

    # Search filter
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (City.name.ilike(search_term)) | (City.country.ilike(search_term))
        )

    # Country filter
    if country:
        query = query.filter(City.country.ilike(f"%{country}%"))

    # Region filter
    if region:
        query = query.filter(City.region.ilike(f"%{region}%"))

    # Cost filters
    if min_cost is not None:
        query = query.filter(City.avg_cost_per_day >= min_cost)
    if max_cost is not None:
        query = query.filter(City.avg_cost_per_day <= max_cost)

    # Order by popularity by default
    query = query.order_by(City.popularity_score.desc())

    cities = query.limit(limit).all()
    return cities


@router.get("/popular", response_model=List[CityListResponse])
def get_popular_cities(limit: int = Query(10, le=50), db: Session = Depends(get_db)):
    """Get most popular cities"""
    cities = db.query(City).order_by(City.popularity_score.desc()).limit(limit).all()
    return cities


@router.get("/{city_id}", response_model=CityResponse)
def get_city(city_id: int, db: Session = Depends(get_db)):
    """Get single city details"""
    from fastapi import HTTPException, status

    city = db.query(City).filter(City.id == city_id).first()

    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="City not found"
        )

    return city
