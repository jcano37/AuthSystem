import pytest
from fastapi.testclient import TestClient


def test_root_endpoint(client: TestClient):
    """Test the root endpoint returns the expected response."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "docs_url" in data
    assert "redoc_url" in data
    assert data["message"] == "Welcome to the Authentication Service"
    assert data["docs_url"] == "/docs"
    assert data["redoc_url"] == "/redoc"


def test_docs_endpoint(client: TestClient):
    """Test that the docs endpoint is accessible."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_endpoint(client: TestClient):
    """Test that the OpenAPI JSON endpoint is accessible."""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data 