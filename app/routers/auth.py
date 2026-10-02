import os

from fastapi import APIRouter, HTTPException, status
from dotenv import load_dotenv

from app.schemas import LoginRequest, TokenResponse
from app.security.jwt import create_access_token

load_dotenv()

router = APIRouter(prefix="/auth", tags=["authentication"])

AUTH_USERNAME = os.getenv("AUTH_USERNAME")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD")


@router.post("/login", response_model=TokenResponse)
def login(credentials: LoginRequest) -> TokenResponse:
    if (
        credentials.username != AUTH_USERNAME
        or credentials.password != AUTH_PASSWORD
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    access_token = create_access_token(
        {"sub": credentials.username}
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )