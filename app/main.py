"""
FastAPI application entry point for Nurse's AI Assistant API.
"""

from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
import uuid

from .auth import generate_user_token, get_token_info, verify_token

# Initialize FastAPI app
app = FastAPI(
    title="Nurse's AI Assistant API",
    description="AI-powered tool for nurses and healthcare professionals "
    "to access and summarize biomedical knowledge",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - returns API information."""
    return {
        "message": "Welcome to Nurse's AI Assistant API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "service": "nurse-ai-api", "version": "0.1.0"}


@app.post("/auth/token")
async def generate_token(
    user_name: Optional[str] = Query(None, description="Optional user name")
):
    """Generate a new authentication token for a user."""
    user_id = str(uuid.uuid4())
    token_data = generate_user_token(user_id, user_name)
    return token_data


@app.get("/auth/me")
async def get_my_token_info(token_payload: dict = Depends(verify_token)):
    """Get information about the current user's token."""
    return {
        "user_id": token_payload.get("sub"),
        "user_name": token_payload.get("name"),
        "issued_at": token_payload.get("iat"),
        "expires_at": token_payload.get("exp"),
        "message": "This is your authentication token information",
    }


@app.get("/auth/token-info")
async def check_token_info(
    token: str = Query(..., description="JWT token to check")
):
    """Check information about any token (public endpoint)."""
    info = get_token_info(token)
    return info


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
