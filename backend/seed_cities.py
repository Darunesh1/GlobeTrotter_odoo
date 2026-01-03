import logging

from app.database import SessionLocal
from app.models.city import City

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_cities():
    db = SessionLocal()

    try:
        logger.info("🌱 Starting city seeding...")

        cities_data = [
            {
                "name": "Paris",
                "country": "France",
                "region": "Europe",
                "description": "The city of lights, art, and romance.",
                "avg_cost_per_day": 150.0,
                "popularity_score": 98,
                "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80",
                "latitude": 48.8566,
                "longitude": 2.3522,
            },
            {
                "name": "Tokyo",
                "country": "Japan",
                "region": "Asia",
                "description": "A bustling metropolis mixing the ultramodern and the traditional.",
                "avg_cost_per_day": 120.0,
                "popularity_score": 95,
                "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=800&q=80",
                "latitude": 35.6762,
                "longitude": 139.6503,
            },
            {
                "name": "New York",
                "country": "USA",
                "region": "North America",
                "description": "The city that never sleeps.",
                "avg_cost_per_day": 200.0,
                "popularity_score": 94,
                "image_url": "https://images.unsplash.com/photo-1496442226666-8d4a0e2907eb?auto=format&fit=crop&w=800&q=80",
                "latitude": 40.7128,
                "longitude": -74.0060,
            },
            {
                "name": "London",
                "country": "UK",
                "region": "Europe",
                "description": "History meets modern culture.",
                "avg_cost_per_day": 160.0,
                "popularity_score": 92,
                "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800&q=80",
                "latitude": 51.5074,
                "longitude": -0.1278,
            },
            {
                "name": "Dubai",
                "country": "UAE",
                "region": "Middle East",
                "description": "Luxury shopping, ultramodern architecture and nightlife.",
                "avg_cost_per_day": 180.0,
                "popularity_score": 90,
                "image_url": "https://images.unsplash.com/photo-1512453979798-5ea904acfb5a?auto=format&fit=crop&w=800&q=80",
                "latitude": 25.2048,
                "longitude": 55.2708,
            },
        ]

        count = 0
        for data in cities_data:
            exists = db.query(City).filter(City.name == data["name"]).first()
            if not exists:
                city = City(**data)
                db.add(city)
                count += 1
            else:
                logger.info(f"ℹ️  City '{data['name']}' already exists.")

        db.commit()
        logger.info(f"✅ Successfully added {count} new cities!")

    except Exception as e:
        logger.error(f"❌ Error seeding cities: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_cities()
