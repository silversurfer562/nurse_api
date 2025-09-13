"""
Health check endpoints.
"""
from datetime import datetime
from fastapi import APIRouter
from app.models.schemas import HealthCheckResponse
from app.config import settings

router = APIRouter()


@router.get("/", response_model=HealthCheckResponse)
async def health_check():
    """Basic health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.utcnow().isoformat()
    )


@router.get("/ready", response_model=HealthCheckResponse)
async def readiness_check():
    """Readiness check for Kubernetes deployments."""
    return HealthCheckResponse(
        status="ready",
        version=settings.app_version,
        timestamp=datetime.utcnow().isoformat()
    )