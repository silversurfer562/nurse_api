"""
FastAPI application for the Nurse AI Assistant API.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import asyncio
from datetime import datetime

from app.config import settings
from app.services.cache_service import cache_service
from app.services.openai_service import openai_service
from app.services.biomedical_service import biomedical_service
from app.routers import health, summaries
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting Nurse AI Assistant API")
    
    # Initialize services
    await cache_service.connect()
    openai_service.initialize()
    
    logger.info("Services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Nurse AI Assistant API")
    await cache_service.disconnect()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="""
        **Nurse's AI Assistant API** - An AI-powered tool that helps nurses and allied health 
        professionals quickly access, summarize, and adapt biomedical knowledge.
        
        ## Key Features
        - Generate draft summaries & education materials
        - Customize reading levels for different audiences  
        - Flexible word counts for clear, concise content
        - Live data retrieval from biomedical databases
        - Safety guardrails with clinician review requirements
        
        ## Data Sources
        - **PubMed** for research articles
        - **ClinicalTrials.gov** for trial information
        - **MedlinePlus** for patient education resources
        - **MyGene/MyChem** for genetic and chemical data
        
        **⚠️ Important:** All generated content is for draft purposes only and requires 
        review by qualified healthcare professionals before use.
        """,
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health.router, prefix="/health", tags=["Health"])
    app.include_router(summaries.router, prefix="/api/v1", tags=["Summaries"])
    
    return app


# Create the application instance
app = create_app()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": "An unexpected error occurred. Please try again later.",
            "status_code": 500,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )