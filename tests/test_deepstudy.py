"""
Tests for deepstudy account functionality.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_deepstudy_status():
    """Test deepstudy status endpoint."""
    response = client.get("/deepstudy/status")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "DeepStudy Account Management"
    assert data["status"] == "active"
    assert "total_users" in data
    assert "active_sessions" in data
    assert "features" in data


def test_register_account():
    """Test user account registration."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "full_name": "Test User",
        "is_deepstudy_enabled": True,
    }

    response = client.post("/deepstudy/account/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert data["full_name"] == user_data["full_name"]
    assert data["is_deepstudy_enabled"] is True
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data  # Password should not be in response


def test_register_duplicate_email():
    """Test that duplicate email registration fails."""
    user_data = {
        "email": "duplicate@example.com",
        "username": "user1",
        "password": "password123",
    }

    # First registration should succeed
    response = client.post("/deepstudy/account/register", json=user_data)
    assert response.status_code == 201

    # Second registration with same email should fail
    user_data["username"] = "user2"
    response = client.post("/deepstudy/account/register", json=user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_account():
    """Test user account login."""
    # First register a user
    user_data = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "password123",
    }
    register_response = client.post(
        "/deepstudy/account/register", json=user_data
    )
    assert register_response.status_code == 201

    # Then login with the same credentials
    login_data = {"email": "login@example.com", "password": "password123"}

    response = client.post("/deepstudy/account/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Login successful"
    assert "user" in data
    assert "session_id" in data
    assert data["deepstudy_enabled"] is True


def test_login_invalid_credentials():
    """Test login with invalid credentials."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword",
    }

    response = client.post("/deepstudy/account/login", json=login_data)
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_get_account_by_id():
    """Test getting account information by user ID."""
    # Register a user first
    user_data = {
        "email": "getuser@example.com",
        "username": "getuser",
        "password": "password123",
    }
    register_response = client.post(
        "/deepstudy/account/register", json=user_data
    )
    user_id = register_response.json()["id"]

    # Get account by ID
    response = client.get(f"/deepstudy/account/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["id"] == user_id


def test_get_account_by_email():
    """Test getting account information by email."""
    # Register a user first
    user_data = {
        "email": "getemail@example.com",
        "username": "getemailuser",
        "password": "password123",
    }
    client.post("/deepstudy/account/register", json=user_data)

    # Get account by email
    response = client.get(f"/deepstudy/account/email/{user_data['email']}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]


def test_create_study_session():
    """Test creating a deepstudy session."""
    # Register a user first
    user_data = {
        "email": "session@example.com",
        "username": "sessionuser",
        "password": "password123",
    }
    register_response = client.post(
        "/deepstudy/account/register", json=user_data
    )
    user_id = register_response.json()["id"]

    # Create a study session
    response = client.post(
        f"/deepstudy/session/create?user_id={user_id}&topic=Cardiology"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "DeepStudy session created successfully"
    assert "session_id" in data
    assert data["user_id"] == user_id
    assert data["topic"] == "Cardiology"


def test_get_study_session():
    """Test getting study session information."""
    # Register user and create session
    user_data = {
        "email": "getsession@example.com",
        "username": "getsessionuser",
        "password": "password123",
    }
    register_response = client.post(
        "/deepstudy/account/register", json=user_data
    )
    user_id = register_response.json()["id"]

    session_response = client.post(
        f"/deepstudy/session/create?user_id={user_id}&topic=Neurology"
    )
    session_id = session_response.json()["session_id"]

    # Get session information
    response = client.get(f"/deepstudy/session/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert data["user_id"] == user_id
    assert data["topic"] == "Neurology"
    assert data["is_active"] is True


def test_list_user_sessions():
    """Test listing all sessions for a user."""
    # Register user
    user_data = {
        "email": "listsessions@example.com",
        "username": "listsessionsuser",
        "password": "password123",
    }
    register_response = client.post(
        "/deepstudy/account/register", json=user_data
    )
    user_id = register_response.json()["id"]

    # Create multiple sessions
    client.post(
        f"/deepstudy/session/create?user_id={user_id}&topic=Pediatrics"
    )
    client.post(
        f"/deepstudy/session/create?user_id={user_id}&topic=Oncology"
    )

    # List user sessions
    response = client.get(f"/deepstudy/user/{user_id}/sessions")
    assert response.status_code == 200
    sessions = response.json()
    assert len(sessions) == 2
    topics = [session["topic"] for session in sessions]
    assert "Pediatrics" in topics
    assert "Oncology" in topics


def test_nonexistent_user_operations():
    """Test operations with nonexistent user IDs."""
    # Test getting nonexistent user
    response = client.get("/deepstudy/account/9999")
    assert response.status_code == 404

    # Test creating session for nonexistent user
    response = client.post("/deepstudy/session/create?user_id=9999")
    assert response.status_code == 404

    # Test listing sessions for nonexistent user
    response = client.get("/deepstudy/user/9999/sessions")
    assert response.status_code == 404


def test_nonexistent_session():
    """Test getting nonexistent session."""
    response = client.get("/deepstudy/session/nonexistent_session_id")
    assert response.status_code == 404
