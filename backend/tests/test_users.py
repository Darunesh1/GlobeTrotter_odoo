import pytest
from fastapi import status


def test_get_user_profile(client, auth_headers, test_user):
    """Test retrieving the current user's profile"""
    # Note: Depending on your main.py router prefix, this might be /users/profile or /api/v1/users/profile
    # Based on standard naming, we assume the router is mounted at /users
    response = client.get("/users/profile", headers=auth_headers)

    # If this fails with 404, check main.py prefixes.
    # It might be /api/v1/users/profile or just /users/profile
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user["user"]["email"]
    assert "password" not in data


def test_update_user_profile(client, auth_headers):
    """Test updating user profile details"""
    new_data = {"full_name": "Updated Name", "username": "updated_user_123"}
    response = client.put("/users/profile", json=new_data, headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["full_name"] == "Updated Name"
    assert data["username"] == "updated_user_123"


def test_update_profile_unauthorized(client):
    """Test that non-logged-in users cannot update profiles"""
    response = client.put("/users/profile", json={"full_name": "Hacker"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_user_profile(client, auth_headers):
    """Test deleting the user account"""
    # 1. Delete the account
    response = client.delete("/users/profile", headers=auth_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # 2. Try to access profile again (should fail because user is deleted)
    response_check = client.get("/users/profile", headers=auth_headers)
    # The token is valid signature-wise, but the user ID won't exist in DB
    assert response_check.status_code == status.HTTP_401_UNAUTHORIZED
