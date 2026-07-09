"""
Health check endpoint.
"""

from fastapi import APIRouter, Request

from app.config import get_settings
from app.schemas.common import HealthResponse

router = APIRouter()
settings = get_settings()


@router.get("/api/health", response_model=HealthResponse)
async def health_check(request: Request):
    """
    Health check endpoint.
    Returns application status, version, and model availability.
    """
    model_loaded = hasattr(request.app.state, "model_service") and request.app.state.model_service.is_loaded

    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        model_loaded=model_loaded,
        environment=settings.ENVIRONMENT,
    )
