"""
Nurse's AI Assistant - FastAPI Backend
======================================

A FastAPI application that combines live biomedical data sources with large language models
to generate draft patient education materials and clinical summaries.

Features:
- Multiple reading levels support
- Flexible word counts
- Safe draft-only outputs for clinician review
- Compliance and guardrails built-in
- Evidence-informed information access for nurses and allied health professionals
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import patient_education, clinical_summaries, health
from app.config import settings

app = FastAPI(
    title="Nurse's AI Assistant API",
    description="Backend service for generating draft patient education materials and clinical summaries with AI assistance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(patient_education.router, prefix="/api/v1", tags=["patient-education"])
app.include_router(clinical_summaries.router, prefix="/api/v1", tags=["clinical-summaries"])

@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "Welcome to Nurse's AI Assistant API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)