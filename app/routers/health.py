"""Health check endpoints"""

from fastapi import APIRouter
from app.models.responses import HealthCheckResponse
from app.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify API status and dependencies.
    
    Returns current service status, version information, and status of dependent services.
    """
    
    # Check dependent services (mock implementation)
    services = {
        "database": "healthy",
        "llm_service": "healthy" if settings.llm_api_key else "not_configured",
        "biomedical_api": "healthy" if settings.enable_live_data else "disabled"
    }
    
    overall_status = "healthy" if all(status != "error" for status in services.values()) else "degraded"
    
    return HealthCheckResponse(
        status=overall_status,
        version=settings.api_version,
        services=services
    )