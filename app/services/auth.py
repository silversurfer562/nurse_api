"""
Authentication and user management service for deepstudy accounts.
"""

from datetime import datetime
from typing import Optional, Dict, List
import hashlib
import secrets
from app.models.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    DeepStudySession,
)


class AuthService:
    """Simple in-memory authentication service for deepstudy accounts."""

    def __init__(self):
        # In-memory storage (would be replaced with database in production)
        self.users: Dict[int, dict] = {}
        self.users_by_email: Dict[str, int] = {}
        self.sessions: Dict[str, DeepStudySession] = {}
        self.next_user_id = 1

    def _hash_password(self, password: str) -> str:
        """Hash password with salt for security."""
        salt = "nurse_api_salt"  # In production, use random salt
        return hashlib.sha256((password + salt).encode()).hexdigest()

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return self._hash_password(password) == hashed

    def create_account(self, user_data: UserCreate) -> UserResponse:
        """Create a new deepstudy user account."""
        # Check if email already exists
        if user_data.email in self.users_by_email:
            raise ValueError("Email already registered")

        # Create user record
        user_id = self.next_user_id
        self.next_user_id += 1

        now = datetime.now()
        user_record = {
            "id": user_id,
            "email": user_data.email,
            "username": user_data.username,
            "full_name": user_data.full_name,
            "password_hash": self._hash_password(user_data.password),
            "is_deepstudy_enabled": user_data.is_deepstudy_enabled,
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }

        self.users[user_id] = user_record
        self.users_by_email[user_data.email] = user_id

        return UserResponse(**user_record)

    def authenticate(self, login_data: UserLogin) -> Optional[UserResponse]:
        """Authenticate user and return user info if valid."""
        user_id = self.users_by_email.get(login_data.email)
        if not user_id:
            return None

        user_record = self.users.get(user_id)
        if not user_record or not user_record["is_active"]:
            return None

        if self._verify_password(
            login_data.password, user_record["password_hash"]
        ):
            return UserResponse(**user_record)

        return None

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Get user by ID."""
        user_record = self.users.get(user_id)
        if user_record and user_record["is_active"]:
            return UserResponse(**user_record)
        return None

    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email."""
        user_id = self.users_by_email.get(email)
        if user_id:
            return self.get_user_by_id(user_id)
        return None

    def create_deepstudy_session(
        self, user_id: int, topic: Optional[str] = None
    ) -> str:
        """Create a new deepstudy session for the user."""
        session_id = secrets.token_urlsafe(32)
        session = DeepStudySession(
            user_id=user_id, session_id=session_id, topic=topic
        )
        self.sessions[session_id] = session
        return session_id

    def get_session(self, session_id: str) -> Optional[DeepStudySession]:
        """Get deepstudy session by ID."""
        return self.sessions.get(session_id)

    def list_user_sessions(self, user_id: int) -> List[DeepStudySession]:
        """List all active sessions for a user."""
        return [
            session
            for session in self.sessions.values()
            if session.user_id == user_id and session.is_active
        ]


# Global service instance
auth_service = AuthService()
