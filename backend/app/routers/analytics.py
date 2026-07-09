"""
Analytics endpoints — user statistics and insights, backed by Supabase.
"""

import logging
from fastapi import APIRouter, Depends, Request

from app.core.security import get_current_user
from app.schemas.common import APIResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/analytics")
async def get_analytics(
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    """
    Get analytics and statistics for the authenticated user.
    Requires authentication.
    """
    supabase_service = request.app.state.supabase_service
    analytics = await supabase_service.get_user_analytics(
        user_id=current_user["sub"],
    )

    return APIResponse(
        success=True,
        data=analytics,
        message="Analytics retrieved successfully.",
    )
