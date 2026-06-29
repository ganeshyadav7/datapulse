"""CRUD helpers for users."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def create_user(
    db: Session,
    email: str,
    hashed_password: str,
    role: str,
    full_name: str | None = None,
) -> User:
    user = User(
        email=email.lower(),
        full_name=full_name,
        hashed_password=hashed_password,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
