"""User and authentication service logic."""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.crud.user import create_user
from app.crud.user import get_user_by_email as fetch_user_by_email
from app.models.user import User, UserRole
from app.schemas.auth import UserRegister


def register_user(db: Session, payload: UserRegister) -> User:
    if fetch_user_by_email(db, payload.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return create_user(
        db=db,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
        role=payload.role.value,
    )


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = fetch_user_by_email(db, email)
    if user is None or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")
    return user


def get_or_create_system_user(db: Session) -> User:
    user = fetch_user_by_email(db, "system@datapulse.local")
    if user:
        return user
    return create_user(
        db=db,
        email="system@datapulse.local",
        full_name="Local System User",
        hashed_password=hash_password("system-local-password"),
        role=UserRole.ADMIN.value,
    )


def get_user_by_email(db: Session, email: str) -> User | None:
    return fetch_user_by_email(db, email)
