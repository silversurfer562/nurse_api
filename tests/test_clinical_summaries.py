"""Tests for clinical summary endpoints"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_generate_clinical_summary_success():
    """Test successful clinical summary generation."""
    request_data = {
        "patient_data": "Patient presents with chest pain and shortness of breath. History of hypertension and diabetes.",
        "summary_type": "admission",
        "word_count": 400,
        "include_recommendations": True,
        "focus_areas": ["cardiovascular", "respiratory"]
    }
    
    response = client.post("/api/v1/clinical-summary", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "summary" in data
    assert "key_findings" in data
    assert "recommendations" in data
    assert "risk_factors" in data
    assert "follow_up_needed" in data
    assert "metadata" in data
    assert "disclaimer" in data
    
    # Check metadata
    assert data["metadata"]["reading_level"] == "professional"
    assert data["metadata"]["requires_review"] is True
    assert "word_count" in data["metadata"]


def test_generate_clinical_summary_without_recommendations():
    """Test clinical summary generation without recommendations."""
    request_data = {
        "patient_data": "Patient presents with mild headache. Vital signs stable.",
        "summary_type": "general",
        "word_count": 300,
        "include_recommendations": False
    }
    
    response = client.post("/api/v1/clinical-summary", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    # When include_recommendations is False, recommendations should be None
    # (This depends on implementation - could be None or empty list)
    assert "recommendations" in data


def test_generate_clinical_summary_validation_errors():
    """Test validation errors for clinical summary requests."""
    
    # Test missing patient_data
    request_data = {
        "summary_type": "general",
        "word_count": 300
    }
    response = client.post("/api/v1/clinical-summary", json=request_data)
    assert response.status_code == 422
    
    # Test invalid word count (too high)
    request_data = {
        "patient_data": "Patient presents with symptoms.",
        "summary_type": "general",
        "word_count": 3000  # Exceeds maximum
    }
    response = client.post("/api/v1/clinical-summary", json=request_data)
    assert response.status_code == 422
    
    # Test invalid word count (too low)
    request_data = {
        "patient_data": "Patient presents with symptoms.",
        "summary_type": "general",
        "word_count": 50  # Below minimum
    }
    response = client.post("/api/v1/clinical-summary", json=request_data)
    assert response.status_code == 422


def test_generate_clinical_summary_short_patient_data():
    """Test validation for too short patient data."""
    request_data = {
        "patient_data": "Short",  # Too short
        "summary_type": "general",
        "word_count": 300
    }
    
    response = client.post("/api/v1/clinical-summary", json=request_data)
    assert response.status_code == 422


def test_clinical_summary_safety_flags():
    """Test that safety flags are properly generated."""
    # This test verifies that the compliance checker is working
    request_data = {
        "patient_data": "Patient has severe condition and requires immediate treatment.",
        "summary_type": "admission",
        "word_count": 300,
        "include_recommendations": True
    }
    
    response = client.post("/api/v1/clinical-summary", json=request_data)
    assert response.status_code == 200
    
    data = response.json()
    # The compliance checker should flag definitive statements
    assert len(data["metadata"]["safety_flags"]) > 0