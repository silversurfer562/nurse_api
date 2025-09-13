"""Request models for API endpoints"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator, ConfigDict
from enum import Enum


class ReadingLevel(str, Enum):
    """Available reading levels for generated content"""
    ELEMENTARY = "elementary"
    MIDDLE_SCHOOL = "middle-school"
    HIGH_SCHOOL = "high-school" 
    COLLEGE = "college"
    PROFESSIONAL = "professional"


class ContentType(str, Enum):
    """Types of content that can be generated"""
    PATIENT_EDUCATION = "patient-education"
    CLINICAL_SUMMARY = "clinical-summary"
    MEDICATION_INFO = "medication-info"
    PROCEDURE_EXPLANATION = "procedure-explanation"


class PatientEducationRequest(BaseModel):
    """Request model for patient education material generation"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    topic: str = Field(..., min_length=3, max_length=200, description="Medical topic for patient education")
    reading_level: ReadingLevel = Field(ReadingLevel.HIGH_SCHOOL, description="Target reading level")
    word_count: int = Field(300, ge=50, le=2000, description="Desired word count (50-2000 words)")
    include_sources: bool = Field(True, description="Include evidence-based sources")
    patient_age_group: Optional[str] = Field(None, description="Target age group (e.g., 'pediatric', 'adult', 'geriatric')")
    language: str = Field("english", description="Output language")
    
    @field_validator('topic')
    @classmethod
    def validate_topic(cls, v):
        """Validate topic contains appropriate medical content"""
        if not v or len(v.strip()) < 3:
            raise ValueError("Topic must be at least 3 characters long")
        return v.strip().lower()


class ClinicalSummaryRequest(BaseModel):
    """Request model for clinical summary generation"""
    
    model_config = ConfigDict(str_strip_whitespace=True)
    
    patient_data: str = Field(..., min_length=10, max_length=5000, description="Patient information and clinical data")
    summary_type: str = Field("general", description="Type of summary (general, admission, discharge, progress)")
    word_count: int = Field(500, ge=100, le=2000, description="Desired word count (100-2000 words)")
    include_recommendations: bool = Field(True, description="Include clinical recommendations")
    focus_areas: Optional[List[str]] = Field(None, description="Specific areas to focus on")
    
    @field_validator('patient_data')
    @classmethod
    def validate_patient_data(cls, v):
        """Validate patient data doesn't contain sensitive information patterns"""
        # Basic validation - in production, would include more sophisticated checks
        sensitive_patterns = ['ssn', 'social security', 'credit card']
        v_lower = v.lower()
        for pattern in sensitive_patterns:
            if pattern in v_lower:
                raise ValueError(f"Patient data may contain sensitive information: {pattern}")
        return v


class BiomedicalSearchRequest(BaseModel):
    """Request model for biomedical data search"""
    
    query: str = Field(..., min_length=3, max_length=500, description="Search query for biomedical literature")
    max_results: int = Field(10, ge=1, le=50, description="Maximum number of results to return")
    publication_years: Optional[List[int]] = Field(None, description="Filter by publication years")
    source_types: Optional[List[str]] = Field(None, description="Types of sources to include")