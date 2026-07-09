"""
Authentication endpoints — register, login, profile.
"""

import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Request

from app.core.exceptions import ValidationException
from app.core.security import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.schemas.auth import AuthResponse, UserLoginRequest, UserRegisterRequest, UserProfile
from app.schemas.common import APIResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/register", response_model=APIResponse[AuthResponse])
async def register(request: Request, register_data: UserRegisterRequest):
    """
    Register a new user account.
    """
    supabase_service = request.app.state.supabase_service

    # Check if email already exists
    existing_user = await supabase_service.get_user_by_email(register_data.email)
    if existing_user:
        raise ValidationException(
            "An account with this email already exists.", field="email"
        )

    # Hash password and create user in database
    pw_hash = hash_password(register_data.password)
    user_record = await supabase_service.create_user(
        name=register_data.name,
        email=register_data.email,
        password_hash=pw_hash,
        location=register_data.location
    )

    if not user_record:
        raise ValidationException("Failed to register user. Please try again.")

    user_id = str(user_record["id"])
    token = create_access_token(user_id, user_record["email"])
    profile = UserProfile(
        id=user_id,
        name=user_record["name"],
        email=user_record["email"],
        location=user_record.get("location"),
        created_at=user_record.get("created_at"),
        total_predictions=0,
    )

    logger.info(f"New user registered: {register_data.email}")
    return APIResponse(
        success=True,
        data=AuthResponse(user=profile, token=token),
        message="Account created successfully.",
    )


@router.post("/login", response_model=APIResponse[AuthResponse])
async def login(request: Request, login_data: UserLoginRequest):
    """
    Login with email and password.
    """
    supabase_service = request.app.state.supabase_service

    # Find user by email
    user = await supabase_service.get_user_by_email(login_data.email)

    if not user or not verify_password(login_data.password, user["password_hash"]):
        raise ValidationException("Invalid email or password.")

    user_id = str(user["id"])
    token = create_access_token(user_id, user["email"])

    # Count total predictions for this user
    total_predictions = 0
    if supabase_service.is_configured:
        try:
            count_result = (
                supabase_service._client.table("predictions")
                .select("id", count="exact")
                .eq("user_id", user_id)
                .execute()
            )
            total_predictions = count_result.count or 0
        except Exception:
            pass

    profile = UserProfile(
        id=user_id,
        name=user["name"],
        email=user["email"],
        location=user.get("location"),
        created_at=user.get("created_at"),
        total_predictions=total_predictions,
    )

    logger.info(f"User logged in: {login_data.email}")
    return APIResponse(
        success=True,
        data=AuthResponse(user=profile, token=token),
        message="Login successful.",
    )


@router.get("/me", response_model=APIResponse[UserProfile])
async def get_profile(request: Request, current_user: dict = Depends(get_current_user)):
    """
    Get current user's profile. Requires authentication.
    """
    supabase_service = request.app.state.supabase_service
    user_id = current_user["sub"]

    user = await supabase_service.get_user_by_id(user_id)
    if not user:
        raise ValidationException("User not found.")

    # Count total predictions
    total_predictions = 0
    if supabase_service.is_configured:
        try:
            count_result = (
                supabase_service._client.table("predictions")
                .select("id", count="exact")
                .eq("user_id", user_id)
                .execute()
            )
            total_predictions = count_result.count or 0
        except Exception:
            pass

    profile = UserProfile(
        id=str(user["id"]),
        name=user["name"],
        email=user["email"],
        location=user.get("location"),
        created_at=user.get("created_at"),
        total_predictions=total_predictions,
    )

    return APIResponse(success=True, data=profile)
