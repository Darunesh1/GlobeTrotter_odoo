from sqlalchemy import Column, Float, Integer, String, Text

from app.database import Base


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False, index=True)
    region = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)

    # Cost and popularity metrics
    avg_cost_per_day = Column(Float, default=0.0)  # USD
    popularity_score = Column(Integer, default=0)  # 0-100

    # Coordinates (optional for maps)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
