"""
FastAPI application entry point for Nurse's AI Assistant API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app import config

# Initialize FastAPI app using central config
app = FastAPI(
    title="Nurse's AI Assistant API",
    description=(
        "AI-powered tool for nurses and healthcare professionals "
        "to access and summarize biomedical knowledge"
    ),
    version=config.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS (read allowed origins from config)
allow_origins = config.CORS_ORIGINS if config.CORS_ORIGINS else ["*"]
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
        "version": config.VERSION,
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
asyn...