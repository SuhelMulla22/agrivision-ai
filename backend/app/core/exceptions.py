"""
Custom application exceptions with consistent error response format.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)


class NotFoundException(AppException):
    """Resource not found."""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="NOT_FOUND",
            message=f"{resource} with identifier '{identifier}' not found.",
        )


class ValidationException(AppException):
    """Request validation error."""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="VALIDATION_ERROR",
            message=message,
            details={"field": field} if field else {},
        )


class UnauthorizedException(AppException):
    """Authentication required."""

    def __init__(self, message: str = "Authentication required."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="UNAUTHORIZED",
            message=message,
        )


class ForbiddenException(AppException):
    """Insufficient permissions."""

    def __init__(self, message: str = "Insufficient permissions."):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="FORBIDDEN",
            message=message,
        )


class RateLimitException(AppException):
    """Too many requests."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            code="RATE_LIMITED",
            message="Too many requests. Please try again later.",
        )


class PredictionException(AppException):
    """ML prediction error."""

    def __init__(self, message: str = "Failed to process the image."):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            code="PREDICTION_ERROR",
            message=message,
        )


def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Format AppException into a consistent JSON response."""
    request_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
            "request_id": request_id,
        },
    )
