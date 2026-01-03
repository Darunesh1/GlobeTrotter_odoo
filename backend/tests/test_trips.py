from datetime import datetime, timedelta

import pytest


@pytest.fixture
def sample_trip_data():
    """Sample trip data for testing"""
    start = datetime.utcnow() + timedelta(days=7)
    end = start + timedelta(days=14)
    return {
        "name": "Europe Adventure",
        "description": "A wonderful trip across Europe",
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "cover_photo": "https://example.com/photo.jpg",
    }


def test_create_trip(client, auth_headers, sample_trip_data):
    """Test creating a new trip"""
    response = client.post("/trips/", json=sample_trip_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_trip_data["name"]
    assert data["description"] == sample_trip_data["description"]
    assert "id" in data
    assert "user_id" in data


def test_create_trip_no_auth(client, sample_trip_data):
    """Test creating trip without authentication fails"""
    response = client.post("/trips/", json=sample_trip_data)
    assert response.status_code == 401


def test_create_trip_invalid_dates(client, auth_headers):
    """Test creating trip with end date before start date fails"""
    start = datetime.utcnow() + timedelta(days=7)
    end = start - timedelta(days=1)  # End before start
    response = client.post(
        "/trips/",
        json={
            "name": "Invalid Trip",
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
        },
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert "End date must be after start date" in response.json()["detail"]


def test_get_all_trips(client, auth_headers, sample_trip_data):
    """Test getting all user trips"""
    # Create two trips
    client.post("/trips/", json=sample_trip_data, headers=auth_headers)
    sample_trip_data["name"] = "Asia Tour"
    client.post("/trips/", json=sample_trip_data, headers=auth_headers)

    # Get all trips
    response = client.get("/trips/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert isinstance(data, list)


def test_get_all_trips_empty(client, auth_headers):
    """Test getting trips when user has none"""
    response = client.get("/trips/", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_single_trip(client, auth_headers, sample_trip_data):
    """Test getting a single trip by ID"""
    # Create trip
    create_response = client.post(
        "/trips/", json=sample_trip_data, headers=auth_headers
    )
    trip_id = create_response.json()["id"]

    # Get trip
    response = client.get(f"/trips/{trip_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == trip_id
    assert data["name"] == sample_trip_data["name"]


def test_get_nonexistent_trip(client, auth_headers):
    """Test getting a trip that doesn't exist"""
    response = client.get("/trips/99999", headers=auth_headers)
    assert response.status_code == 404


def test_update_trip(client, auth_headers, sample_trip_data):
    """Test updating a trip"""
    # Create trip
    create_response = client.post(
        "/trips/", json=sample_trip_data, headers=auth_headers
    )
    trip_id = create_response.json()["id"]

    # Update trip
    update_data = {"name": "Updated Trip Name", "description": "Updated description"}
    response = client.put(f"/trips/{trip_id}", json=update_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Trip Name"
    assert data["description"] == "Updated description"


def test_update_trip_partial(client, auth_headers, sample_trip_data):
    """Test partial update of a trip"""
    # Create trip
    create_response = client.post(
        "/trips/", json=sample_trip_data, headers=auth_headers
    )
    trip_id = create_response.json()["id"]

    # Update only name
    response = client.put(
        f"/trips/{trip_id}", json={"name": "New Name"}, headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["description"] == sample_trip_data["description"]  # Unchanged


def test_update_nonexistent_trip(client, auth_headers):
    """Test updating a trip that doesn't exist"""
    response = client.put(
        "/trips/99999", json={"name": "New Name"}, headers=auth_headers
    )
    assert response.status_code == 404


def test_delete_trip(client, auth_headers, sample_trip_data):
    """Test deleting a trip"""
    # Create trip
    create_response = client.post(
        "/trips/", json=sample_trip_data, headers=auth_headers
    )
    trip_id = create_response.json()["id"]

    # Delete trip
    response = client.delete(f"/trips/{trip_id}", headers=auth_headers)
    assert response.status_code == 204

    # Verify trip is deleted
    get_response = client.get(f"/trips/{trip_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_delete_nonexistent_trip(client, auth_headers):
    """Test deleting a trip that doesn't exist"""
    response = client.delete("/trips/99999", headers=auth_headers)
    assert response.status_code == 404


def test_user_cannot_access_other_users_trips(client, sample_trip_data):
    """Test that users can only access their own trips"""
    # Create first user and trip
    user1_data = {
        "email": "user1@example.com",
        "username": "user1",
        "password": "pass123",
    }
    client.post("/auth/register", json=user1_data)
    login1 = client.post(
        "/auth/login",
        json={"email": user1_data["email"], "password": user1_data["password"]},
    )
    token1 = login1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    trip_response = client.post("/trips/", json=sample_trip_data, headers=headers1)
    trip_id = trip_response.json()["id"]

    # Create second user
    user2_data = {
        "email": "user2@example.com",
        "username": "user2",
        "password": "pass123",
    }
    client.post("/auth/register", json=user2_data)
    login2 = client.post(
        "/auth/login",
        json={"email": user2_data["email"], "password": user2_data["password"]},
    )
    token2 = login2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # User 2 tries to access User 1's trip
    response = client.get(f"/trips/{trip_id}", headers=headers2)
    assert response.status_code == 404  # Should not find it
