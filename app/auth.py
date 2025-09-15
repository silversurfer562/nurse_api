"""
Authentication utilities for Nurse's AI Assistant API.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

import jwt
from jwt.exceptions import PyJWTError, ExpiredSignatureError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

# Security scheme
security = HTTPBearer()


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            hours=ACCESS_TOKEN_EXPIRE_HOURS
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Dict[str, Any]:
    """Verify and decode JWT token."""
    try:
        payload = jwt.decode(
            credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM]
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def generate_user_token(
    user_id: str, user_name: Optional[str] = None
) -> Dict[str, Any]:
    """Generate a new authentication token for a user."""
    token_data = {
        "sub": user_id,
        "name": user_name or f"User_{user_id}",
        "iat": datetime.now(timezone.utc),
    }

    access_token = create_access_token(data=token_data)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user_id,
        "user_name": token_data["name"],
        "expires_in": ACCESS_TOKEN_EXPIRE_HOURS * 3600,  # seconds
    }


def get_token_info(token: str) -> Dict[str, Any]:
    """Get information about a token without requiring authentication."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "user_id": payload.get("sub"),
            "user_name": payload.get("name"),
            "issued_at": payload.get("iat"),
            "expires_at": payload.get("exp"),
            "valid": True,
        }
    except ExpiredSignatureError:
        return {"valid": False, "error": "Token has expired"}
    except PyJWTError:
        return {"valid": False, "error": "Invalid token"}
