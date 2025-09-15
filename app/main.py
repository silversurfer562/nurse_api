"""
FastAPI application entry point for Nurse's AI Assistant API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


    docs_url="/docs",
    redoc_url="/redoc",
)


    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - returns API information."""
    return {
        "message": "Welcome to Nurse's AI Assistant API",

        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""

