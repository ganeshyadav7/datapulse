"""Authentication API schemas."""

from pydantic import BaseModel, ConfigDict, Field

from app.models.user import UserRole


class UserRegister(BaseModel):
    email: str = Field(min_length=3, max_length=255, examples=["admin@datapulse.local"])
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)
    role: UserRole = UserRole.VIEWER


class UserLogin(BaseModel):
    email: str = Field(examples=["admin@datapulse.local"])
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    full_name: str | None
    role: str
    is_active: bool
