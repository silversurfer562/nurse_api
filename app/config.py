"""Central configuration for the Nurse API.

Read runtime configuration from environment variables.
"""

from __future__ import annotations

import os
from typing import List, Optional

from dotenv import load_dotenv

# Load .env if present (development convenience)
load_dotenv()

def _parse_list(env_value: Optional[str]) -> List[str]:
    if not env_value:
        return []
    return [s.strip() for s in env_value.split(",") if s.strip()]

# App metadata
VERSION: str = os.getenv("VERSION", "0.1.0")
SERVICE_NAME: str = os.getenv("SERVICE_NAME", "nurse-ai-api")

# Server settings
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))

# CORS origins: comma-separated hosts, or "*" for all
_CORS_RAW = os.getenv("CORS_ORIGINS", "*")
CORS_ORIGINS: List[str] = _parse_list(_CORS_RAW)
# If the parse produced an empty list, expose wildcard for middleware
if not CORS_ORIGINS:
    CORS_ORIGINS = ["*"]
