import logging

from app.database import SessionLocal
from app.models.activity import Activity
from app.models.city import City

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def seed_activities():
    db = SessionLocal()

    try:
        logger.info("🌱 Starting activity seeding...")

        # List of activities to add
        # We use 'city_name' to find the correct ID dynamically
        activities_data = [
            # Paris
            {
                "city_name": "Paris",
                "name": "Eiffel Tower Summit Access",
                "category": "Sightseeing",
                "description": "Visit the top of the Eiffel Tower for panoramic views.",
                "estimated_cost": 30.0,
                "duration_hours": 3.0,
                "image_url": "https://example.com/eiffel.jpg",
            },
            {
                "city_name": "Paris",
                "name": "Louvre Museum Guided Tour",
                "category": "Culture",
                "description": "Skip-the-line guided tour of the world's largest art museum.",
                "estimated_cost": 45.0,
                "duration_hours": 4.0,
                "image_url": "https://example.com/louvre.jpg",
            },
            {
                "city_name": "Paris",
                "name": "Seine River Cruise",
                "category": "Relaxation",
                "description": "Evening boat cruise along the Seine river.",
                "estimated_cost": 20.0,
                "duration_hours": 1.5,
                "image_url": "https://example.com/seine.jpg",
            },
            # Tokyo
            {
                "city_name": "Tokyo",
                "name": "TeamLab Planets",
                "category": "Art",
                "description": "Immersive digital art museum where you walk through water.",
                "estimated_cost": 35.0,
                "duration_hours": 2.0,
                "image_url": "https://example.com/teamlab.jpg",
            },
            {
                "city_name": "Tokyo",
                "name": "Shibuya Crossing & Hachiko",
                "category": "Sightseeing",
                "description": "Walk the world's busiest pedestrian crossing.",
                "estimated_cost": 0.0,
                "duration_hours": 1.0,
                "image_url": "https://example.com/shibuya.jpg",
            },
            # New York
            {
                "city_name": "New York",
                "name": "Statue of Liberty Ferry",
                "category": "Sightseeing",
                "description": "Ferry ride to Liberty Island and Ellis Island.",
                "estimated_cost": 25.0,
                "duration_hours": 4.0,
                "image_url": "https://example.com/liberty.jpg",
            },
            {
                "city_name": "New York",
                "name": "Broadway Show: The Lion King",
                "category": "Entertainment",
                "description": "Premium seats for a top Broadway musical.",
                "estimated_cost": 150.0,
                "duration_hours": 3.0,
                "image_url": "https://example.com/broadway.jpg",
            },
            # London
            {
                "city_name": "London",
                "name": "London Eye Standard Ticket",
                "category": "Sightseeing",
                "description": "30-minute rotation on the iconic observation wheel.",
                "estimated_cost": 35.0,
                "duration_hours": 0.5,
                "image_url": "https://example.com/londoneye.jpg",
            },
            # Dubai
            {
                "city_name": "Dubai",
                "name": "Burj Khalifa At the Top",
                "category": "Sightseeing",
                "description": "Access to levels 124 and 125 of the world's tallest building.",
                "estimated_cost": 50.0,
                "duration_hours": 2.0,
                "image_url": "https://example.com/burj.jpg",
            },
            {
                "city_name": "Dubai",
                "name": "Desert Safari with BBQ Dinner",
                "category": "Adventure",
                "description": "Dune bashing, camel riding, and traditional dinner.",
                "estimated_cost": 70.0,
                "duration_hours": 6.0,
                "image_url": "https://example.com/safari.jpg",
            },
        ]

        count = 0
        for data in activities_data:
            # 1. Find the city ID first
            city = db.query(City).filter(City.name == data["city_name"]).first()

            if not city:
                logger.warning(
                    f"⚠️  City '{data['city_name']}' not found. Skipping activity '{data['name']}'."
                )
                continue

            # 2. Check if activity already exists to avoid duplicates
            exists = (
                db.query(Activity)
                .filter(Activity.name == data["name"], Activity.city_id == city.id)
                .first()
            )

            if not exists:
                # 3. Create and add
                activity = Activity(
                    name=data["name"],
                    category=data["category"],
                    description=data["description"],
                    estimated_cost=data["estimated_cost"],
                    duration_hours=data["duration_hours"],
                    image_url=data["image_url"],
                    city_id=city.id,
                )
                db.add(activity)
                count += 1
            else:
                logger.info(f"ℹ️  Activity '{data['name']}' already exists.")

        db.commit()
        logger.info(f"✅ Successfully added {count} new activities!")

    except Exception as e:
        logger.error(f"❌ Error seeding activities: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_activities()
