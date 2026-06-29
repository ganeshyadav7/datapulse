"""Authentication, password hashing, and JWT helpers."""

import base64
import hashlib
import hmac
import json
import secrets
from datetime import timedelta
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.user import User, UserRole
from app.utils.time import utc_now

oauth2_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    """Hash a password with PBKDF2-HMAC using only the Python standard library."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"pbkdf2_sha256$100000${salt}${digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt, expected = password_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), int(iterations))
        return hmac.compare_digest(digest.hex(), expected)
    except ValueError:
        return False


def _b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _b64decode(data: str) -> bytes:
    padding = "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def create_token(subject: str, role: str, expires_delta: timedelta, token_type: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    expires_at = int((utc_now() + expires_delta).timestamp())
    payload = {"sub": subject, "role": role, "exp": expires_at, "typ": token_type}
    signing_input = ".".join(
        [
            _b64encode(json.dumps(header, separators=(",", ":")).encode()),
            _b64encode(json.dumps(payload, separators=(",", ":")).encode()),
        ]
    )
    signature = hmac.new(
        settings.jwt_secret_key.encode(), signing_input.encode(), hashlib.sha256
    ).digest()
    return f"{signing_input}.{_b64encode(signature)}"


def decode_token(token: str, expected_type: str = "access") -> dict[str, Any]:
    try:
        header_b64, payload_b64, signature_b64 = token.split(".")
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc

    signing_input = f"{header_b64}.{payload_b64}"
    expected_signature = hmac.new(
        settings.jwt_secret_key.encode(), signing_input.encode(), hashlib.sha256
    ).digest()
    if not hmac.compare_digest(_b64encode(expected_signature), signature_b64):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    payload = json.loads(_b64decode(payload_b64))
    if payload.get("typ") != expected_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
    if int(payload.get("exp", 0)) < int(utc_now().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    return payload


def create_access_token(user: User) -> str:
    return create_token(
        subject=user.email,
        role=user.role,
        expires_delta=timedelta(minutes=settings.jwt_access_token_minutes),
        token_type="access",
    )


def create_refresh_token(user: User) -> str:
    return create_token(
        subject=user.email,
        role=user.role,
        expires_delta=timedelta(minutes=settings.jwt_refresh_token_minutes),
        token_type="refresh",
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    from app.services import user_service

    if not settings.auth_enabled:
        return user_service.get_or_create_system_user(db)
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    payload = decode_token(credentials.credentials)
    user = user_service.get_user_by_email(db, payload["sub"])
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user


def require_roles(*roles: UserRole):
    allowed = {role.value for role in roles}

    def dependency(user: User = Depends(get_current_user)) -> User:
        if not settings.auth_enabled:
            return user
        if user.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return user

    return dependency
