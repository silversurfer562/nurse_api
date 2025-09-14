"""
Tests for the main FastAPI application.
"""

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns expected information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to Nurse's AI Assistant API"

    assert data["status"] == "running"
    assert data["docs"] == "/docs"
    assert data["redoc"] == "/redoc"


def test_health_check_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"



def test_api_docs_available():
    """Test that API documentation endpoints are accessible."""
    # Test OpenAPI schema
    response = client.get("/openapi.json")
    assert response.status_code == 200

    # Test Swagger UI (should return HTML)
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

    # Test ReDoc (should return HTML)
    response = client.get("/redoc")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
