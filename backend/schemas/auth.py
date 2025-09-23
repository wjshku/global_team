from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, model_validator

from utils.validation import validate_email


class LoginRequest(BaseModel):
    # Allow login with either email or name. Exactly one must be provided.
    email: Optional[str] = None
    name: Optional[str] = None
    password: str = Field(..., min_length=1)

    @model_validator(mode="after")
    def validate_identifier(self):  # type: ignore[override]
        has_email = bool(self.email)
        has_name = bool(self.name)
        if has_email == has_name:  # both provided or both missing
            raise ValueError("Provide exactly one of 'email' or 'name'")
        if self.email and not validate_email(self.email):
            raise ValueError('Invalid email format')
        return self


class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(...)
    password: str = Field(..., min_length=8)
    timezone: str = Field('UTC')


class TokenResponse(BaseModel):
    accessToken: str
    tokenType: str = 'bearer'


class ProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    timezone: str
    role: str = 'member'
    avatar: Optional[str] = None
    createdAt: Optional[str] = None


class UpdateProfileRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    timezone: Optional[str] = None


