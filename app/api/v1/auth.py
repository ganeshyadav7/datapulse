"""JWT authentication endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, decode_token
from app.db.session import get_db
from app.schemas.auth import RefreshTokenRequest, TokenResponse, UserLogin, UserRead, UserRegister
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    return user_service.register_user(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = user_service.authenticate_user(db, payload.email, payload.password)
    return TokenResponse(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
        role=user.role,
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)):
    token_payload = decode_token(payload.refresh_token, expected_type="refresh")
    user = user_service.get_user_by_email(db, token_payload["sub"])
    if user is None:
        user = user_service.get_or_create_system_user(db)
    return TokenResponse(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
        role=user.role,
    )
