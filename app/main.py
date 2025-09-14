"""
FastAPI application entry point for Nurse's AI Assistant API.
"""

from typing import List, Any
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Try to import central config if available; if not, provide safe defaults.
try:
    from app import config  # PR provides this module
except ImportError:
    # Fallback config used only if the config module isn't present (safety during merge)
    class _FallbackConfig:
        VERSION = "0.1.0"
        SERVICE_NAME = "nurse-ai-api"
        HOST = "0.0.0.0"
        PORT = 8000
        CORS_ORIGINS: List[str] = ["*"]

    config = _FallbackConfig()

logger = logging.getLogger(__name__)

def _normalize_cors(raw: Any) -> List[str]:
    """
    Normalize CORS configuration into a list of origins.

    Accepts:
    - list -> returned as-is (copied)
    - comma-separated string -> split and stripped
    - "*" or empty -> returns ["*"]
    """
    if raw is None:
        return ["*"]

    # Direct list-like
    if isinstance(raw, (list, tuple)):
        origins = [str(x).strip() for x in raw if str(x).strip()]
        return origins or ["*"]

    # Single wildcard
    raw_str = str(raw).strip()
    if raw_str == "*" or raw_str == "":
        return ["*"]

    # Comma-separated string
    origins = [s.strip() for s in raw_str.split(",") if s.strip()]
    return origins or ["*"]


# Resolve version and service name (prefer config values, fall back to literals)
APP_VERSION = getattr(config, "VERSION", "0.1.0")
SERVICE_NAME = getattr(config, "SERVICE_NAME", "nurse-ai-api")

# Initialize FastAPI app using central config (or fallbacks)
app = FastAPI(
    title="Nurse's AI Assistant API",
    description=(
        "AI-powered tool for nurses and healthcare professionals "
        "to access and summarize biomedical knowledge"
    ),
    version=APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS (read allowed origins from config, normalize wildcard)
allow_origins = _normalize_cors(getattr(config, "CORS_ORIGINS", ["*"]))
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - returns API information."""
    return {
        "message": "Welcome to Nurse's AI Assistant API",
        "version": APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": SERVICE_NAME,
        "version": APP_VERSION,
    }


if __name__ == "__main__":
    # Use values from config for local development run; ensure port is an int.
    host = getattr(config, "HOST", "0.0.0.0")
    try:
        port = int(getattr(config, "PORT", 8000))
    except (TypeError, ValueError):
        logger.warning("Invalid PORT in config; falling back to 8000")
        port = 8000

    uvicorn.run("app.main:app", host=host, port=port, reload=True)
