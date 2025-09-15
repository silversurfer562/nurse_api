"""
Tests for authentication functionality.
"""

import jwt
from fastapi.testclient import TestClient
from app.main import app
from app.auth import SECRET_KEY, ALGORITHM

client = TestClient(app)


def test_generate_token():
    """Test token generation endpoint."""
    response = client.post("/auth/token")
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert "token_type" in data
    assert "user_id" in data
    assert "user_name" in data
    assert "expires_in" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 24 * 3600  # 24 hours in seconds

    # Verify the token is valid
    payload = jwt.decode(
        data["access_token"], SECRET_KEY, algorithms=[ALGORITHM]
    )
    assert payload["sub"] == data["user_id"]


def test_generate_token_with_user_name():
    """Test token generation with custom user name."""
    response = client.post("/auth/token?user_name=test_user")
    assert response.status_code == 200
    data = response.json()

    assert data["user_name"] == "test_user"

    # Verify the token contains the correct user name
    payload = jwt.decode(
        data["access_token"], SECRET_KEY, algorithms=[ALGORITHM]
    )
    assert payload["name"] == "test_user"


def test_get_my_token_info():
    """Test getting current user's token information."""
    # First generate a token
    token_response = client.post("/auth/token?user_name=test_user")
    token_data = token_response.json()
    access_token = token_data["access_token"]

    # Use the token to get info
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == token_data["user_id"]
    assert data["user_name"] == "test_user"
    assert "issued_at" in data
    assert "expires_at" in data
    assert "message" in data


def test_get_my_token_info_without_token():
    """Test getting token info without providing a token."""
    response = client.get("/auth/me")
    assert response.status_code == 403  # No credentials provided


def test_get_my_token_info_with_invalid_token():
    """Test getting token info with an invalid token."""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]


def test_check_token_info():
    """Test checking token information via public endpoint."""
    # First generate a token
    token_response = client.post("/auth/token?user_name=check_user")
    token_data = token_response.json()
    access_token = token_data["access_token"]

    # Check token info
    response = client.get(f"/auth/token-info?token={access_token}")
    assert response.status_code == 200

    data = response.json()
    assert data["valid"] is True
    assert data["user_id"] == token_data["user_id"]
    assert data["user_name"] == "check_user"
    assert "issued_at" in data
    assert "expires_at" in data


def test_check_invalid_token_info():
    """Test checking invalid token information."""
    response = client.get("/auth/token-info?token=invalid_token")
    assert response.status_code == 200

    data = response.json()
    assert data["valid"] is False
    assert "error" in data


def test_auth_endpoints_in_openapi():
    """Test that authentication endpoints appear in OpenAPI schema."""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    openapi_data = response.json()
    paths = openapi_data["paths"]

    assert "/auth/token" in paths
    assert "/auth/me" in paths
    assert "/auth/token-info" in paths

    # Check that auth/me requires security
    me_endpoint = paths["/auth/me"]["get"]
    assert "security" in me_endpoint
