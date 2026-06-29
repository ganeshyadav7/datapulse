"""User ORM model for JWT authentication and RBAC."""

from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.utils.time import utc_now


class UserRole(StrEnum):
    ADMIN = "Admin"
    OPERATOR = "Operator"
    VIEWER = "Viewer"


class User(Base):
    """Authenticated DataPulse user."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(40), default=UserRole.VIEWER.value, index=True)
    is_active: Mapped[bool] = mapped_column(default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
