"""
API routes for deepstudy account management.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from app.models.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    DeepStudySession,
)
from app.services.auth import auth_service

router = APIRouter(prefix="/deepstudy", tags=["DeepStudy Account"])


@router.post(
    "/account/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_account(user_data: UserCreate):
    """Register a new deepstudy user account."""
    try:
        user = auth_service.create_account(user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@router.post("/account/login", response_model=dict)
async def login_account(login_data: UserLogin):
    """Login to deepstudy account."""
    user = auth_service.authenticate(login_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Create a session for the authenticated user
    session_id = auth_service.create_deepstudy_session(user.id)

    return {
        "message": "Login successful",
        "user": user,
        "session_id": session_id,
        "deepstudy_enabled": user.is_deepstudy_enabled,
    }


@router.get("/account/{user_id}", response_model=UserResponse)
async def get_account(user_id: int):
    """Get deepstudy account information by user ID."""
    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/account/email/{email}", response_model=UserResponse)
async def get_account_by_email(email: str):
    """Get deepstudy account information by email."""
    user = auth_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/session/create", response_model=dict)
async def create_study_session(user_id: int, topic: Optional[str] = None):
    """Create a new deepstudy session."""
    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    if not user.is_deepstudy_enabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="DeepStudy feature is not enabled for this account",
        )

    session_id = auth_service.create_deepstudy_session(user_id, topic)
    return {
        "message": "DeepStudy session created successfully",
        "session_id": session_id,
        "user_id": user_id,
        "topic": topic,
    }


@router.get("/session/{session_id}", response_model=DeepStudySession)
async def get_study_session(session_id: str):
    """Get deepstudy session information."""
    session = auth_service.get_session(session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
        )
    return session


@router.get("/user/{user_id}/sessions", response_model=List[DeepStudySession])
async def list_user_sessions(user_id: int):
    """List all active deepstudy sessions for a user."""
    user = auth_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    sessions = auth_service.list_user_sessions(user_id)
    return sessions


@router.get("/status", response_model=dict)
async def deepstudy_status():
    """Get deepstudy service status and statistics."""
    total_users = len(auth_service.users)
    active_sessions = len(
        [s for s in auth_service.sessions.values() if s.is_active]
    )

    return {
        "service": "DeepStudy Account Management",
        "status": "active",
        "total_users": total_users,
        "active_sessions": active_sessions,
        "features": [
            "account_registration",
            "authentication",
            "session_management",
        ],
    }
