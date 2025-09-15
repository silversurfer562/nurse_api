# Authentication Token Usage Guide

This guide explains how to generate and retrieve your authentication token in the Nurse's AI Assistant API.

## Getting Your Authentication Token

### Step 1: Generate a Token

To generate a new authentication token, make a POST request to `/auth/token`:

```bash
# Generate a token with your name
curl -X POST "http://localhost:8000/auth/token?user_name=YourName"
```

**Response:**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user_id": "f4c09f04-e345-4065-ae49-24d8bd3f9dee",
    "user_name": "YourName",
    "expires_in": 86400
}
```

### Step 2: What is My Authentication Token?

To answer "what is my authentication token", you have two options:

#### Option A: Use the Protected Endpoint (Recommended)
If you have your token, use the `/auth/me` endpoint to get information about your current token:

```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     "http://localhost:8000/auth/me"
```

**Response:**
```json
{
    "user_id": "f4c09f04-e345-4065-ae49-24d8bd3f9dee",
    "user_name": "YourName",
    "issued_at": 1757912764,
    "expires_at": 1757999164,
    "message": "This is your authentication token information"
}
```

#### Option B: Use the Public Token Info Endpoint
If you want to check any token's information:

```bash
curl "http://localhost:8000/auth/token-info?token=YOUR_TOKEN_HERE"
```

**Response:**
```json
{
    "user_id": "f4c09f04-e345-4065-ae49-24d8bd3f9dee",
    "user_name": "YourName",
    "issued_at": 1757912764,
    "expires_at": 1757999164,
    "valid": true
}
```

## Token Information

- **Token Type**: JWT (JSON Web Token)
- **Expiration**: 24 hours from generation
- **Format**: Bearer token for Authorization header
- **Usage**: Include in API requests as `Authorization: Bearer YOUR_TOKEN`

## Error Handling

- **Invalid Token**: Returns `{"valid": false, "error": "Invalid token"}`
- **Expired Token**: Returns `{"valid": false, "error": "Token has expired"}`
- **Missing Token**: Returns HTTP 403 with "Not authenticated" error

## Security Notes

- Store your token securely
- Tokens expire after 24 hours
- Generate new tokens as needed
- Never share your token with others