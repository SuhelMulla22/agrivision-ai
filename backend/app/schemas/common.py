"""
Common response schemas used across all endpoints.
"""

from typing import Any, Dict, Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""

    success: bool = Field(..., description="Whether the request was successful")
    data: Optional[T] = Field(None, description="Response data")
    message: Optional[str] = Field(None, description="Human-readable message")
    request_id: Optional[str] = Field(None, description="Unique request identifier")


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    error: Dict[str, Any] = Field(
        ...,
        description="Error details with code and message",
    )
    request_id: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "ok"
    version: str
    model_loaded: bool
    environment: str
