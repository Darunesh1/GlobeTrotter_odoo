import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base, get_db
from app.main import app

# Test database
TEST_DATABASE_URL = settings.TEST_DATABASE_URL
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with test database"""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    """Create a test user and return credentials"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpass123",
        "full_name": "Test User",
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    return {
        "user": response.json(),
        "credentials": {"email": user_data["email"], "password": user_data["password"]},
    }


@pytest.fixture
def auth_token(client, test_user):
    """Get authentication token for test user"""
    response = client.post("/auth/login", json=test_user["credentials"])
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Get headers with authentication token"""
    return {"Authorization": f"Bearer {auth_token}"}
