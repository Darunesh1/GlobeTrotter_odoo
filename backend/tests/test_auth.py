import pytest
from fastapi import status

# --- Registration Tests ---


def test_register_user_success(client):
    """Test successful user registration"""
    response = client.post(
        "/auth/register",
        json={
            "email": "alice@example.com",
            "username": "alice_wonder",
            "password": "securepassword123",
            "full_name": "Alice Wonderland",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "alice@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # Security check


def test_register_duplicate_email(client, test_user):
    """Test registering with an email that already exists"""
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",  # Existing email from fixture
            "username": "new_username",
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Email already registered" in response.json()["detail"]


def test_register_duplicate_username(client, test_user):
    """Test registering with a username that already exists"""
    response = client.post(
        "/auth/register",
        json={
            "email": "unique@example.com",
            "username": "testuser",  # Existing username from fixture
            "password": "password123",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Username already taken" in response.json()["detail"]


def test_register_validation_missing_fields(client):
    """Test registration validation (missing password)"""
    response = client.post(
        "/auth/register",
        json={
            "email": "incomplete@example.com",
            "username": "incomplete",
            # Password missing
        },
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# --- Login Tests ---


def test_login_success(client, test_user):
    """Test successful login returns a token"""
    response = client.post("/auth/login", json=test_user["credentials"])
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, test_user):
    """Test login with incorrect password"""
    credentials = test_user["credentials"].copy()
    credentials["password"] = "wrong_password"

    response = client.post("/auth/login", json=credentials)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Incorrect email or password" in response.json()["detail"]


def test_login_nonexistent_user(client):
    """Test login for a user that doesn't exist"""
    response = client.post(
        "/auth/login", json={"email": "ghost@example.com", "password": "boo"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# --- Access Control Tests ---


def test_get_current_user_profile(client, auth_headers, test_user):
    """Test retrieving profile with valid token"""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user["user"]["email"]


def test_protected_route_no_token(client):
    """Test accessing protected route without token fails"""
    # Attempt to access profile without headers
    response = client.get("/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_protected_route_invalid_token(client):
    """Test accessing protected route with garbage token fails"""
    headers = {"Authorization": "Bearer not_a_real_token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_route_access_denied_for_normal_user(client, auth_headers):
    """Test that a normal user CANNOT access admin analytics"""
    # Assuming /api/v1/admin/analytics exists and requires admin
    response = client.get("/api/v1/admin/analytics", headers=auth_headers)
    # Should return 403 Forbidden or 404 Not Found (depending on router order),
    # but definitely NOT 200
    assert response.status_code in [
        status.HTTP_403_FORBIDDEN,
        status.HTTP_404_NOT_FOUND,
    ]
