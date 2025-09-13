"""Response models for API endpoints"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from .requests import ReadingLevel


class GenerationMetadata(BaseModel):
    """Metadata for generated content"""
    
    model_config = ConfigDict(protected_namespaces=())
    
    generated_at: datetime = Field(default_factory=datetime.now, description="Timestamp of generation")
    word_count: int = Field(..., description="Actual word count of generated content")
    reading_level: ReadingLevel = Field(..., description="Target reading level used")
    model_used: str = Field(..., description="AI model used for generation")
    safety_flags: List[str] = Field(default=[], description="Any safety or compliance flags raised")
    requires_review: bool = Field(True, description="Whether content requires clinician review")


class SourceReference(BaseModel):
    """Reference to a biomedical source"""
    
    title: str = Field(..., description="Title of the source")
    authors: Optional[List[str]] = Field(None, description="Authors of the source")
    journal: Optional[str] = Field(None, description="Publication journal")
    year: Optional[int] = Field(None, description="Publication year")
    doi: Optional[str] = Field(None, description="Digital Object Identifier")
    url: Optional[str] = Field(None, description="URL to the source")
    relevance_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Relevance score (0-1)")


class PatientEducationResponse(BaseModel):
    """Response model for patient education material"""
    
    content: str = Field(..., description="Generated patient education content")
    title: str = Field(..., description="Generated title for the material")
    key_points: List[str] = Field(..., description="Key takeaway points")
    sources: List[SourceReference] = Field(default=[], description="Evidence-based sources referenced")
    metadata: GenerationMetadata = Field(..., description="Generation metadata")
    disclaimer: str = Field(
        default="This content is AI-generated and intended as a draft. "
                "It must be reviewed and approved by a qualified healthcare professional before use.",
        description="Legal disclaimer for AI-generated content"
    )


class ClinicalSummaryResponse(BaseModel):
    """Response model for clinical summary"""
    
    summary: str = Field(..., description="Generated clinical summary")
    key_findings: List[str] = Field(..., description="Key clinical findings")
    recommendations: Optional[List[str]] = Field(None, description="Clinical recommendations if requested")
    risk_factors: List[str] = Field(default=[], description="Identified risk factors")
    follow_up_needed: List[str] = Field(default=[], description="Suggested follow-up actions")
    metadata: GenerationMetadata = Field(..., description="Generation metadata")
    disclaimer: str = Field(
        default="This summary is AI-generated and intended to assist healthcare professionals. "
                "Clinical decisions should always be based on professional judgment and patient assessment.",
        description="Clinical disclaimer for AI-generated content"
    )


class BiomedicalSearchResponse(BaseModel):
    """Response model for biomedical data search"""
    
    results: List[SourceReference] = Field(..., description="Search results")
    total_found: int = Field(..., description="Total number of results found")
    search_metadata: Dict[str, Any] = Field(default={}, description="Search metadata")


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint"""
    
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(default_factory=datetime.now, description="Health check timestamp")
    version: str = Field(..., description="API version")
    services: Dict[str, str] = Field(default={}, description="Status of dependent services")


class ErrorResponse(BaseModel):
    """Response model for API errors"""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Detailed error message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request identifier for tracking")