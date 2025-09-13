"""Tests for the main FastAPI application"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint returns correct information."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to Nurse's AI Assistant API"
    assert data["version"] == "1.0.0"
    assert "/docs" in data["docs"]
    assert "/api/v1/health" in data["health"]


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["healthy", "degraded"]
    assert data["version"] == "1.0.0"
    assert "services" in data
    assert "timestamp" in data