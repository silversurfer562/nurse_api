"""
Pydantic models for request/response schemas.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class ReadingLevel(str, Enum):
    """Reading level options for content generation."""
    ELEMENTARY = "elementary"
    MIDDLE_SCHOOL = "middle_school"
    HIGH_SCHOOL = "high_school"
    COLLEGE = "college"
    GRADUATE = "graduate"
    PROFESSIONAL = "professional"


class ContentType(str, Enum):
    """Type of content to generate."""
    PATIENT_EDUCATION = "patient_education"
    CLINICAL_SUMMARY = "clinical_summary"
    RESEARCH_SUMMARY = "research_summary"
    MEDICATION_INFO = "medication_info"
    CONDITION_OVERVIEW = "condition_overview"


class SummaryRequest(BaseModel):
    """Request model for generating summaries."""
    query: str = Field(..., description="The medical topic or condition to research")
    content_type: ContentType = Field(default=ContentType.PATIENT_EDUCATION)
    reading_level: ReadingLevel = Field(default=ReadingLevel.HIGH_SCHOOL)
    word_count: int = Field(default=300, ge=50, le=2000, description="Target word count")
    include_sources: bool = Field(default=True, description="Include source citations")
    audience: Optional[str] = Field(None, description="Specific audience (e.g., 'diabetes patients')")


class SourceInfo(BaseModel):
    """Information about a source used in content generation."""
    title: str
    authors: Optional[List[str]] = None
    publication_date: Optional[str] = None
    source_type: str  # pubmed, clinicaltrials, medlineplus, etc.
    url: Optional[str] = None
    pmid: Optional[str] = None


class SummaryResponse(BaseModel):
    """Response model for generated summaries."""
    content: str
    word_count: int
    reading_level: ReadingLevel
    content_type: ContentType
    sources: List[SourceInfo] = []
    metadata: Dict[str, Any] = {}
    disclaimer: str = Field(
        default="This is a draft summary for educational purposes only. "
                "Please consult with healthcare professionals for medical advice."
    )


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
    timestamp: str


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
    error_code: Optional[str] = None