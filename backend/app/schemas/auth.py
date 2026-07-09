"""
Authentication-related Pydantic schemas.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegisterRequest(BaseModel):
    """User registration request."""

    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., min_length=6, max_length=128, description="Password")
    location: Optional[str] = Field(None, description="User location (city/state)")


class UserLoginRequest(BaseModel):
    """User login request."""

    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")


class UserProfile(BaseModel):
    """User profile data."""

    id: str = Field(..., description="User ID")
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    location: Optional[str] = Field(None, description="User location")
    created_at: Optional[str] = Field(None, description="Account creation date")
    total_predictions: int = Field(0, description="Total predictions made")


class AuthResponse(BaseModel):
    """Authentication response with token."""

    user: UserProfile
    token: str = Field(..., description="JWT access token")
