import pytest
from fastapi.testclient import TestClient


@pytest.mark.integration  
def test_register_user(client: TestClient, auth_headers):
    """Test user registration by authenticated superuser."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User",
        "company_id": 1  # Root company ID
    }
    
    response = client.post("/api/v1/users/", json=user_data, headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert data["company_id"] == user_data["company_id"]
    assert "id" in data
    assert "hashed_password" not in data  # Should not return password


@pytest.mark.integration
def test_login_user(client: TestClient, auth_headers):
    """Test user login."""
    # First create a user using admin endpoint
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "loginpassword123",
        "full_name": "Login User",
        "company_id": 1  # Root company ID
    }
    
    register_response = client.post("/api/v1/users/", json=user_data, headers=auth_headers)
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


@pytest.mark.integration
def test_login_with_wrong_password(client: TestClient, auth_headers):
    """Test login with wrong password."""
    # First create a user using admin endpoint
    user_data = {
        "email": "wrong@example.com",
        "username": "wronguser",
        "password": "correctpassword123",
        "full_name": "Wrong User",
        "company_id": 1  # Root company ID
    }
    
    register_response = client.post("/api/v1/users/", json=user_data, headers=auth_headers)
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


@pytest.mark.integration
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


@pytest.mark.integration
def test_password_reset_request(client: TestClient, auth_headers):
    """Test password reset request."""
    # First create a user using admin endpoint
    user_data = {
        "email": "reset@example.com",
        "username": "resetuser",
        "password": "resetpassword123",
        "full_name": "Reset User",
        "company_id": 1  # Root company ID
    }
    
    register_response = client.post("/api/v1/users/", json=user_data, headers=auth_headers)
    assert register_response.status_code == 200
    
    # Request password reset
    reset_data = {
        "email": "reset@example.com"
    }
    
    response = client.post("/api/v1/auth/password-reset-request", json=reset_data)
    assert response.status_code == 202
    data = response.json()
    assert "message" in data


@pytest.mark.integration
def test_root_user_login(client: TestClient):
    """Test that root user can login."""
    login_data = {
        "username": "root",
        "password": "Root1234!"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.integration
def test_unauthorized_register_attempt(client: TestClient):
    """Test that registration without authentication fails."""
    user_data = {
        "email": "unauthorized@example.com",
        "username": "unauthorized",
        "password": "password123",
        "full_name": "Unauthorized User",
        "company_id": 1
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authenticated" 