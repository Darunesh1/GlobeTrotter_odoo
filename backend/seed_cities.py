from app.database import Base, SessionLocal, engine
from app.models.city import City


def seed_cities():
    """Seed database with sample cities"""
    db = SessionLocal()

    # Check if cities already exist
    if db.query(City).count() > 0:
        print("⚠️  Cities already exist. Skipping seed.")
        db.close()
        return

    cities_data = [
        # Europe
        {
            "name": "Paris",
            "country": "France",
            "region": "Europe",
            "description": "The City of Light, known for the Eiffel Tower, art, and cuisine",
            "avg_cost_per_day": 120.0,
            "popularity_score": 95,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "image_url": "https://images.unsplash.com/photo-1502602898657-3e91760cbb34",
        },
        {
            "name": "London",
            "country": "United Kingdom",
            "region": "Europe",
            "description": "Historic capital with royal palaces, museums, and diverse culture",
            "avg_cost_per_day": 150.0,
            "popularity_score": 92,
            "latitude": 51.5074,
            "longitude": -0.1278,
            "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad",
        },
        {
            "name": "Rome",
            "country": "Italy",
            "region": "Europe",
            "description": "Ancient city with the Colosseum, Vatican, and incredible Italian food",
            "avg_cost_per_day": 100.0,
            "popularity_score": 90,
            "latitude": 41.9028,
            "longitude": 12.4964,
            "image_url": "https://images.unsplash.com/photo-1552832230-c0197dd311b5",
        },
        {
            "name": "Barcelona",
            "country": "Spain",
            "region": "Europe",
            "description": "Mediterranean city famous for Gaudí architecture and beaches",
            "avg_cost_per_day": 90.0,
            "popularity_score": 88,
            "latitude": 41.3851,
            "longitude": 2.1734,
            "image_url": "https://images.unsplash.com/photo-1583422409516-2895a77efded",
        },
        {
            "name": "Amsterdam",
            "country": "Netherlands",
            "region": "Europe",
            "description": "Canal city known for art museums, cycling, and liberal culture",
            "avg_cost_per_day": 110.0,
            "popularity_score": 85,
            "latitude": 52.3676,
            "longitude": 4.9041,
            "image_url": "https://images.unsplash.com/photo-1534351590666-13e3e96b5017",
        },
        # Asia
        {
            "name": "Tokyo",
            "country": "Japan",
            "region": "Asia",
            "description": "Ultra-modern metropolis blending tradition with cutting-edge technology",
            "avg_cost_per_day": 130.0,
            "popularity_score": 93,
            "latitude": 35.6762,
            "longitude": 139.6503,
            "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf",
        },
        {
            "name": "Bangkok",
            "country": "Thailand",
            "region": "Asia",
            "description": "Vibrant city with ornate temples, street food, and nightlife",
            "avg_cost_per_day": 50.0,
            "popularity_score": 87,
            "latitude": 13.7563,
            "longitude": 100.5018,
            "image_url": "https://images.unsplash.com/photo-1508009603885-50cf7c579365",
        },
        {
            "name": "Singapore",
            "country": "Singapore",
            "region": "Asia",
            "description": "Futuristic city-state with Gardens by the Bay and diverse cuisine",
            "avg_cost_per_day": 140.0,
            "popularity_score": 84,
            "latitude": 1.3521,
            "longitude": 103.8198,
            "image_url": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd",
        },
        {
            "name": "Dubai",
            "country": "United Arab Emirates",
            "region": "Middle East",
            "description": "Luxurious desert city with world's tallest building and shopping",
            "avg_cost_per_day": 160.0,
            "popularity_score": 86,
            "latitude": 25.2048,
            "longitude": 55.2708,
            "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c",
        },
        {
            "name": "Mumbai",
            "country": "India",
            "region": "Asia",
            "description": "Bollywood capital with colonial architecture and vibrant street life",
            "avg_cost_per_day": 40.0,
            "popularity_score": 78,
            "latitude": 19.0760,
            "longitude": 72.8777,
            "image_url": "https://images.unsplash.com/photo-1566552881560-0be862a7c445",
        },
        # Americas
        {
            "name": "New York",
            "country": "United States",
            "region": "North America",
            "description": "The Big Apple - iconic skyline, Broadway, and endless energy",
            "avg_cost_per_day": 180.0,
            "popularity_score": 94,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "image_url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9",
        },
        {
            "name": "Los Angeles",
            "country": "United States",
            "region": "North America",
            "description": "Hollywood, beaches, and year-round sunshine",
            "avg_cost_per_day": 160.0,
            "popularity_score": 85,
            "latitude": 34.0522,
            "longitude": -118.2437,
            "image_url": "https://images.unsplash.com/photo-1534190239940-9ba8944ea261",
        },
        {
            "name": "Rio de Janeiro",
            "country": "Brazil",
            "region": "South America",
            "description": "Beach paradise with Christ the Redeemer and Carnival spirit",
            "avg_cost_per_day": 70.0,
            "popularity_score": 82,
            "latitude": -22.9068,
            "longitude": -43.1729,
            "image_url": "https://images.unsplash.com/photo-1483729558449-99ef09a8c325",
        },
        {
            "name": "Buenos Aires",
            "country": "Argentina",
            "region": "South America",
            "description": "Paris of South America with tango, steak, and European flair",
            "avg_cost_per_day": 60.0,
            "popularity_score": 79,
            "latitude": -34.6037,
            "longitude": -58.3816,
            "image_url": "https://images.unsplash.com/photo-1589909202802-8f4aadce1849",
        },
        {
            "name": "Toronto",
            "country": "Canada",
            "region": "North America",
            "description": "Multicultural city with CN Tower and nearby Niagara Falls",
            "avg_cost_per_day": 130.0,
            "popularity_score": 77,
            "latitude": 43.6532,
            "longitude": -79.3832,
            "image_url": "https://images.unsplash.com/photo-1517935706615-2717063c2225",
        },
        # Oceania & Africa
        {
            "name": "Sydney",
            "country": "Australia",
            "region": "Oceania",
            "description": "Harbor city with Opera House, beaches, and laid-back vibe",
            "avg_cost_per_day": 140.0,
            "popularity_score": 89,
            "latitude": -33.8688,
            "longitude": 151.2093,
            "image_url": "https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9",
        },
        {
            "name": "Cape Town",
            "country": "South Africa",
            "region": "Africa",
            "description": "Stunning coastal city with Table Mountain and wine country",
            "avg_cost_per_day": 70.0,
            "popularity_score": 81,
            "latitude": -33.9249,
            "longitude": 18.4241,
            "image_url": "https://images.unsplash.com/photo-1580060839134-75a5edca2e99",
        },
        {
            "name": "Istanbul",
            "country": "Turkey",
            "region": "Europe/Asia",
            "description": "Bridge between continents with rich history and bazaars",
            "avg_cost_per_day": 60.0,
            "popularity_score": 83,
            "latitude": 41.0082,
            "longitude": 28.9784,
            "image_url": "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200",
        },
    ]

    # Add cities to database
    for city_data in cities_data:
        city = City(**city_data)
        db.add(city)

    db.commit()
    print(f"✓ Seeded {len(cities_data)} cities successfully!")
    db.close()


if __name__ == "__main__":
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    seed_cities()
