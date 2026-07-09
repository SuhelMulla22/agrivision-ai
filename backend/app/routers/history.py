"""
Prediction history endpoints — backed by Supabase.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, Request

from app.core.security import get_current_user
from app.schemas.common import APIResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/history")
async def get_prediction_history(
    request: Request,
    limit: int = Query(20, ge=1, le=100, description="Number of records"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: dict = Depends(get_current_user),
):
    """
    Get prediction history for the authenticated user.
    Requires authentication.
    """
    supabase_service = request.app.state.supabase_service
    result = await supabase_service.get_prediction_history(
        user_id=current_user["sub"],
        limit=limit,
        offset=offset,
    )

    return APIResponse(
        success=True,
        data={
            "predictions": result["predictions"],
            "total": result["total"],
            "limit": limit,
            "offset": offset,
            "has_more": result["has_more"],
        },
        message="History retrieved successfully.",
    )
