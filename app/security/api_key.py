"""
API Key authentication dependency for FastAPI.
Minimal implementation with environment variable and header validation.
"""

import os
import secrets
from dotenv import load_dotenv
from fastapi import Header, HTTPException, status

# Load environment variables from .env file
load_dotenv()

# Read API key from environment variable
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("API_KEY environment variable must be set")


def verify_api_key(x_api_key: str = Header(default=None, alias="X-API-Key")) -> bool:
    """
    FastAPI dependency that validates X-API-Key header.
    
    Args:
        x_api_key: X-API-Key header value (defaults to None)
        
    Returns:
        bool: Always returns True if key is valid
        
    Raises:
        HTTPException: 401 if key is missing or invalid
    """
    # Check if header is provided
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key missing"
        )
    
    # Validate API key using constant-time comparison
    if not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return True