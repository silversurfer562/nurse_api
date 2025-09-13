"""Tests for patient education endpoints"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_generate_patient_education_success():
    """Test successful patient education generation."""
    request_data = {
        "topic": "hypertension",
        "reading_level": "high-school",
        "word_count": 300,
        "include_sources": True,
        "patient_age_group": "adult"
    }
    
    response = client.post("/api/v1/patient-education", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "content" in data
    assert "title" in data
    assert "key_points" in data
    assert "sources" in data
    assert "metadata" in data
    assert "disclaimer" in data
    
    # Check metadata
    assert data["metadata"]["reading_level"] == "high-school"
    assert data["metadata"]["requires_review"] is True
    assert "word_count" in data["metadata"]


def test_generate_patient_education_different_reading_levels():
    """Test patient education generation with different reading levels."""
    reading_levels = ["elementary", "middle-school", "high-school", "college", "professional"]
    
    for level in reading_levels:
        request_data = {
            "topic": "diabetes",
            "reading_level": level,
            "word_count": 200,
            "include_sources": False
        }
        
        response = client.post("/api/v1/patient-education", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["metadata"]["reading_level"] == level


def test_generate_patient_education_validation_errors():
    """Test validation errors for patient education requests."""
    
    # Test missing topic
    request_data = {
        "reading_level": "high-school",
        "word_count": 300
    }
    response = client.post("/api/v1/patient-education", json=request_data)
    assert response.status_code == 422
    
    # Test invalid word count (too high)
    request_data = {
        "topic": "diabetes",
        "reading_level": "high-school",
        "word_count": 3000  # Exceeds maximum
    }
    response = client.post("/api/v1/patient-education", json=request_data)
    assert response.status_code == 422
    
    # Test invalid word count (too low)
    request_data = {
        "topic": "diabetes",
        "reading_level": "high-school",
        "word_count": 10  # Below minimum
    }
    response = client.post("/api/v1/patient-education", json=request_data)
    assert response.status_code == 422


def test_generate_patient_education_short_topic():
    """Test validation for too short topics."""
    request_data = {
        "topic": "ab",  # Too short
        "reading_level": "high-school",
        "word_count": 300
    }
    
    response = client.post("/api/v1/patient-education", json=request_data)
    assert response.status_code == 422