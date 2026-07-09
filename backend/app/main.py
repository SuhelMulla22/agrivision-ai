"""
AgriVision AI — FastAPI Application Entry Point.

Production-grade crop disease detection API.
"""

import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.core.exceptions import AppException, app_exception_handler

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    # --- Startup ---
    logger.info("🌱 AgriVision AI starting up...")

    # Enforce secure configurations in production
    if settings.ENVIRONMENT == "production":
        if settings.SECRET_KEY == "dev-secret-key-change-in-production":
            logger.critical("🚨 CRITICAL SECURITY ERROR: SECRET_KEY is set to default development value in production!")
            raise RuntimeError(
                "Insecure configuration: You must change settings.SECRET_KEY in production to prevent token forging."
            )
        if len(settings.SECRET_KEY) < 32:
            logger.critical("🚨 CRITICAL SECURITY ERROR: SECRET_KEY is too short (must be at least 32 characters)!")
            raise RuntimeError(
                "Insecure configuration: SECRET_KEY must be a strong random secret with at least 32 characters."
            )

    # Load ML model into memory
    from app.services.model_service import ModelService
    model_service = ModelService()
    model_service.load_model()
    app.state.model_service = model_service
    logger.info("✅ ML model loaded successfully")

    # Initialize disease knowledge base
    from app.services.disease_service import DiseaseService
    disease_service = DiseaseService()
    app.state.disease_service = disease_service
    logger.info("✅ Disease knowledge base loaded")

    # Initialize translation service
    from app.services.translation_service import TranslationService
    translation_service = TranslationService()
    app.state.translation_service = translation_service

    # Initialize Supabase service (database, storage)
    from app.services.supabase_service import SupabaseService
    supabase_service = SupabaseService()
    app.state.supabase_service = supabase_service

    logger.info("AgriVision AI is ready to serve!")

    yield

    # --- Shutdown ---
    logger.info("👋 AgriVision AI shutting down...")


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description=(
            "AI-powered crop disease detection for Indian farmers. "
            "Upload a crop leaf image and get instant disease diagnosis "
            "with treatment recommendations in English, Hindi, and Marathi."
        ),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )

    # --- Middleware (order matters: last added = first executed) ---
    _configure_middleware(app)
    _configure_exception_handlers(app)
    _configure_routes(app)

    return app


def _configure_middleware(app: FastAPI) -> None:
    """Register all middleware."""

    # CORS — must be added last (executed first)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate Limiting
    try:
        from slowapi import Limiter, _rate_limit_exceeded_handler
        from slowapi.util import get_remote_address
        from slowapi.errors import RateLimitExceeded

        limiter = Limiter(key_func=get_remote_address)
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        logger.info(f"Rate limiting enabled: {settings.RATE_LIMIT_PER_MINUTE}/min")
    except ImportError:
        logger.warning("slowapi not installed. Rate limiting disabled.")

    # Request ID & Timing middleware
    @app.middleware("http")
    async def request_middleware(request: Request, call_next):
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        start = time.perf_counter()

        response = await call_next(request)

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time-Ms"] = str(duration_ms)
        
        # Security & Privacy Headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=*, microphone=(), geolocation=()"

        logger.info(
            f"[{request_id}] {request.method} {request.url.path} "
            f"→ {response.status_code} ({duration_ms}ms)"
        )
        return response


def _configure_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers."""

    @app.exception_handler(AppException)
    async def custom_app_exception(request: Request, exc: AppException):
        return app_exception_handler(request, exc)

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", "unknown")
        logger.error(f"[{request_id}] Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred. Please try again.",
                },
                "request_id": request_id,
            },
        )


def _configure_routes(app: FastAPI) -> None:
    """Register all API routers."""

    from app.routers import analytics, auth, diseases, health, history, predict

    app.include_router(health.router, tags=["Health"])
    app.include_router(predict.router, prefix="/api/v1", tags=["Prediction"])
    app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
    app.include_router(diseases.router, prefix="/api/v1", tags=["Diseases"])
    app.include_router(history.router, prefix="/api/v1", tags=["History"])
    app.include_router(analytics.router, prefix="/api/v1", tags=["Analytics"])


# Create the app instance
app = create_application()
