import pytest


def test_register_user(client):
    """Test user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "password123",
            "full_name": "New User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["username"] == "newuser"
    assert "hashed_password" not in data


def test_register_duplicate_email(client, test_user):
    """Test registering with duplicate email fails"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",  # Already exists
            "username": "different",
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_register_duplicate_username(client, test_user):
    """Test registering with duplicate username fails"""
    response = client.post(
        "/auth/register",
        json={
            "email": "different@example.com",
            "username": "testuser",  # Already exists
            "password": "password123",
        },
    )
    assert response.status_code == 400
    assert "Username already taken" in response.json()["detail"]


def test_login_success(client, test_user):
    """Test successful login"""
    response = client.post("/auth/login", json=test_user["credentials"])
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Test login with wrong password fails"""
    response = client.post(
        "/auth/login", json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login with non-existent user fails"""
    response = client.post(
        "/auth/login", json={"email": "notexist@example.com", "password": "password123"}
    )
    assert response.status_code == 401


def test_get_current_user(client, test_user, auth_headers):
    """Test getting current user info"""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["user"]["email"]
    assert data["username"] == test_user["user"]["username"]


def test_get_current_user_no_auth(client):
    """Test getting current user without authentication fails"""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_get_current_user_invalid_token(client):
    """Test getting current user with invalid token fails"""
    response = client.get("/auth/me", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401
