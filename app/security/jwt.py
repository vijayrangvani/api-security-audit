"""
Minimal JWT implementation for FastAPI using python-jose.
Loads configuration from environment variables.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from jose import JWTError, jwt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# JWT Configuration from environment variables
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))

# Validate required environment variables
if not SECRET_KEY:
    raise ValueError("JWT_SECRET_KEY environment variable must be set")


def create_access_token(data: Dict[str, Any]) -> str:
    """
    Create a JWT access token with expiration.
    
    Args:
        data: Dictionary of claims to encode in the token
        
    Returns:
        str: Encoded JWT token
        
    Example:
        token = create_access_token({"sub": "user123"})
    """
    # Create a copy of data to avoid modifying the original
    to_encode = data.copy()
    
    # Add expiration claim with timezone-aware datetime
    expire = datetime.now(timezone.utc) + timedelta(minutes=EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Encode JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        Dict[str, Any]: Decoded token payload
        
    Raises:
        JWTError: If token is invalid, expired, or malformed
        
    Example:
        payload = verify_token(token)
        user_id = payload.get("sub")
    """
    try:
        # Decode and verify token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        # Re-raise JWTError for caller to handle
        raise e