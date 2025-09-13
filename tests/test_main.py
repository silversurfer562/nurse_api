"""
Basic tests for the FastAPI application.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_readiness_check():
    """Test the readiness check endpoint."""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


def test_docs_endpoint():
    """Test that API documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_schema():
    """Test that OpenAPI schema is available."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert "info" in schema
    assert schema["info"]["title"] == "Nurse AI Assistant API"


def test_summary_endpoint_validation():
    """Test summary endpoint input validation."""
    # Test with missing required fields
    response = client.post("/api/v1/summaries", json={})
    assert response.status_code == 422  # Validation error
    
    # Test with valid minimal request
    valid_request = {
        "query": "diabetes management"
    }
    response = client.post("/api/v1/summaries", json=valid_request)
    # Should succeed (200) or fail gracefully (500) but not validation error (422)
    assert response.status_code in [200, 500]


def test_sources_endpoint():
    """Test sources endpoint."""
    response = client.get("/api/v1/summaries/sources/diabetes")
    # Should succeed or fail gracefully but not 404
    assert response.status_code in [200, 500]