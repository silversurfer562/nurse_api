"""
Pydantic models for deepstudy user accounts.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    """Base user model with common fields."""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(
        ..., min_length=3, max_length=50, description="Username"
    )
    full_name: Optional[str] = Field(
        None, max_length=100, description="Full name"
    )
    is_deepstudy_enabled: bool = Field(
        default=True, description="DeepStudy feature enabled"
    )


class UserCreate(UserBase):
    """Model for creating a new user account."""

    password: str = Field(..., min_length=8, description="Password")


class UserUpdate(BaseModel):
    """Model for updating user account information."""

    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, max_length=100)
    is_deepstudy_enabled: Optional[bool] = None


class UserResponse(UserBase):
    """Model for user account response (without sensitive data)."""

    id: int = Field(..., description="User ID")
    created_at: datetime = Field(
        ..., description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        ..., description="Last update timestamp"
    )
    is_active: bool = Field(
        default=True, description="Account active status"
    )

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    """Model for user login credentials."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="Password")


class DeepStudySession(BaseModel):
    """Model for deepstudy session information."""

    user_id: int = Field(..., description="User ID")
    session_id: str = Field(..., description="Session ID")
    topic: Optional[str] = Field(None, description="Study topic")
    created_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = Field(default=True)
