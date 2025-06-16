import pytest
from fastapi.testclient import TestClient


def test_register_user(client: TestClient):
    """Test user registration."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "hashed_password" not in data  # Should not return password


def test_login_user(client: TestClient):
    """Test user login."""
    # First register a user
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "loginpassword123",
        "full_name": "Login User"
    }
    
    register_response = client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200
    
    # Now try to login
    login_data = {
        "username": "loginuser",
        "password": "loginpassword123"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password(client: TestClient):
    """Test login with wrong password."""
    # First register a user
    user_data = {
        "email": "wrong@example.com",
        "username": "wronguser",
        "password": "correctpassword123",
        "full_name": "Wrong User"
    }
    
    register_response = client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200
    
    # Try to login with wrong password
    login_data = {
        "username": "wronguser",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_login_nonexistent_user(client: TestClient):
    """Test login with nonexistent user."""
    login_data = {
        "username": "nonexistent",
        "password": "anypassword"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Incorrect username or password"


def test_password_reset_request(client: TestClient):
    """Test password reset request."""
    # First register a user
    user_data = {
        "email": "reset@example.com",
        "username": "resetuser",
        "password": "resetpassword123",
        "full_name": "Reset User"
    }
    
    register_response = client.post("/api/v1/auth/register", json=user_data)
    assert register_response.status_code == 200
    
    # Request password reset
    reset_data = {
        "email": "reset@example.com"
    }
    
    response = client.post("/api/v1/auth/password-reset-request", json=reset_data)
    assert response.status_code == 202
    data = response.json()
    assert "message" in data 