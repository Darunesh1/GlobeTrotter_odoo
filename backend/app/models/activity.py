from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String)  # e.g., "Sightseeing", "Food", "Adventure"
    description = Column(Text, nullable=True)
    estimated_cost = Column(Float, default=0.0)
    duration_hours = Column(Float, default=1.0)
    image_url = Column(String, nullable=True)

    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)

    # Relationships
    city = relationship("City", back_populates="activities")


# Link table: Connects a specific Stop in a Trip to an Activity
class StopActivity(Base):
    __tablename__ = "stop_activities"

    id = Column(Integer, primary_key=True, index=True)
    stop_id = Column(Integer, ForeignKey("stops.id"), nullable=False)
    activity_id = Column(Integer, ForeignKey("activities.id"), nullable=False)

    # User can customize these for their specific trip budget
    actual_cost = Column(Float, nullable=True)

    # Relationships
    stop = relationship(
        "Stop", back_populates="activities"
    )  # Note: Update Stop model to match this
    activity = relationship("Activity")
