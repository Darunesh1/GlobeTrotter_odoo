from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    # Order of stop in the trip (1st stop, 2nd stop, etc.)
    order = Column(Integer, nullable=False)

    # Dates for this stop
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # Optional notes
    notes = Column(String, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="stops")
    city = relationship("City")

    # Add inside Stop class:
    activities = relationship(
        "StopActivity", back_populates="stop", cascade="all, delete-orphan"
    )
