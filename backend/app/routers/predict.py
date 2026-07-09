"""
Prediction endpoints — the core of AgriVision AI.
"""

import logging
from io import BytesIO

from fastapi import APIRouter, File, Form, Request, UploadFile, Depends

from app.config import get_settings
from app.core.exceptions import PredictionException, ValidationException
from app.core.security import get_current_user
from app.schemas.common import APIResponse
from app.schemas.prediction import (
    DiseaseInfoResponse,
    PredictionData,
    TopPrediction,
    TreatmentInfo,
)
from app.services.translation_service import TranslationService

logger = logging.getLogger(__name__)
router = APIRouter()
settings = get_settings()


@router.post("/predict", response_model=APIResponse[PredictionData])
async def predict_disease(
    request: Request,
    file: UploadFile = File(..., description="Crop leaf image (JPG, PNG, WEBP)"),
    language: str = Form("en", description="Response language (en/hi/mr)"),
    current_user: dict = Depends(get_current_user),
):
    """
    Upload a crop leaf image and get instant disease diagnosis.

    Returns:
    - Disease name and confidence score
    - Severity assessment
    - Top 3 predictions
    - Complete disease information (symptoms, causes, treatment, prevention)
    - Localized in English, Hindi, or Marathi
    """
    # --- Validate inputs ---
    _validate_file(file)
    lang = TranslationService.validate_language(language)

    # --- Read and validate image ---
    try:
        contents = await file.read()
        if len(contents) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
            raise ValidationException(
                f"File size exceeds {settings.MAX_FILE_SIZE_MB}MB limit.",
                field="file",
            )

        from PIL import Image

        image = Image.open(BytesIO(contents))
    except ValidationException:
        raise
    except Exception as e:
        raise PredictionException(f"Invalid image file: {str(e)}")

    # --- Run prediction ---
    try:
        model_service = request.app.state.model_service
        prediction_result = model_service.predict(image, language=lang)
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise PredictionException("Failed to process the image. Please try again.")

    # --- Get disease information ---
    disease_service = request.app.state.disease_service
    translation_service = request.app.state.translation_service

    if "gemini_rich_info" in prediction_result:
        # Use Gemini's parsed rich info directly (bypassing local KB)
        rich_info = prediction_result["gemini_rich_info"]
        disease_info = DiseaseInfoResponse(
            name=rich_info.get("name", prediction_result["predicted_class"]),
            crop=rich_info.get("crop", prediction_result["crop"]),
            description=rich_info.get("description", ""),
            symptoms=rich_info.get("symptoms", []),
            causes=rich_info.get("causes", []),
            treatment=TreatmentInfo(
                organic=rich_info.get("treatment", {}).get("organic", []) if isinstance(rich_info.get("treatment"), dict) else [],
                chemical=rich_info.get("treatment", {}).get("chemical", []) if isinstance(rich_info.get("treatment"), dict) else [],
            ),
            prevention=rich_info.get("prevention", []),
            severity_info=rich_info.get("severity_info"),
        )
    else:
        disease_info_raw = disease_service.get_disease_info_by_class(
            prediction_result["predicted_class"]
        )

        # Build disease info response
        if disease_info_raw:
            localized_info = translation_service.localize_disease_info(
                disease_info_raw, lang
            )

            # Get severity-specific info
            severity = prediction_result["severity"]
            severity_info = None
            if severity and disease_info_raw.get("severity_info"):
                severity_data = disease_info_raw["severity_info"].get(severity)
                if severity_data:
                    severity_info = translation_service.get_localized_content(
                        severity_data, lang
                    )

            disease_info = DiseaseInfoResponse(
                name=localized_info.get("name", prediction_result["predicted_class"]),
                crop=localized_info.get("crop", prediction_result["crop"]),
                description=localized_info.get("description", ""),
                symptoms=localized_info.get("symptoms", []),
                causes=localized_info.get("causes", []),
                treatment=TreatmentInfo(
                    organic=(
                        localized_info.get("treatment", {}).get("organic", [])
                        if isinstance(localized_info.get("treatment"), dict)
                        else []
                    ),
                    chemical=(
                        localized_info.get("treatment", {}).get("chemical", [])
                        if isinstance(localized_info.get("treatment"), dict)
                        else []
                    ),
                ),
                prevention=localized_info.get("prevention", []),
                severity_info=severity_info,
            )
        else:
            # Fallback for unknown diseases - use our new dynamic fallback guidelines generator!
            fallback_data = disease_service.get_dynamic_fallback_info(
                prediction_result["predicted_class"],
                prediction_result["crop"],
                lang
            )
            disease_info = DiseaseInfoResponse(
                name=fallback_data["name"],
                crop=fallback_data["crop"],
                description=fallback_data["description"],
                symptoms=fallback_data["symptoms"],
                causes=fallback_data["causes"],
                treatment=TreatmentInfo(
                    organic=fallback_data["treatment"]["organic"],
                    chemical=fallback_data["treatment"]["chemical"],
                ),
                prevention=fallback_data["prevention"],
                severity_info=fallback_data["severity_info"],
            )

    # --- Build response ---
    top_predictions = [
        TopPrediction(
            disease=p["class"].replace("_", " ").replace("___", " — "),
            confidence=p["confidence"],
        )
        for p in prediction_result["top_predictions"]
    ]

    response_data = PredictionData(
        disease=disease_info.name,
        disease_id=prediction_result["predicted_class"].lower().replace("___", "_"),
        crop=prediction_result["crop"],
        confidence=prediction_result["confidence"],
        severity=prediction_result["severity"],
        is_healthy=prediction_result["is_healthy"],
        top_predictions=top_predictions,
        disease_info=disease_info,
        language=lang,
        processing_time_ms=prediction_result["processing_time_ms"],
    )

    # --- Save prediction to database ---
    try:
        from app.core.security import get_current_user_optional
        supabase_service = request.app.state.supabase_service

        # Upload image to storage
        image_url = await supabase_service.upload_image(contents, file.filename or "leaf.jpg")

        # Get user ID from authenticated payload
        user_id = current_user.get("sub")

        # Save prediction
        await supabase_service.save_prediction(
            user_id=user_id,
            prediction_data={
                "disease": response_data.disease,
                "disease_id": response_data.disease_id,
                "crop": response_data.crop,
                "confidence": response_data.confidence,
                "severity": response_data.severity,
                "is_healthy": response_data.is_healthy,
                "language": lang,
                "processing_time_ms": response_data.processing_time_ms,
                "top_predictions": [
                    {"class": p.disease, "confidence": p.confidence}
                    for p in response_data.top_predictions
                ],
                "disease_info": response_data.disease_info.model_dump() if response_data.disease_info else None,
            },
            image_url=image_url,
        )

        logger.info(
            f"Prediction: {prediction_result['predicted_class']} "
            f"({prediction_result['confidence']:.2%}) "
            f"crop={prediction_result['crop']} "
            f"lang={lang} "
            f"time={prediction_result['processing_time_ms']}ms"
        )
    except Exception:
        pass  # Don't fail prediction if storage fails

    return APIResponse(
        success=True,
        data=response_data,
        message="Prediction completed successfully.",
    )


def _validate_file(file: UploadFile) -> None:
    """Validate uploaded file."""
    if not file.filename:
        raise ValidationException("No file provided.", field="file")

    # Check extension
    ext = "." + file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise ValidationException(
            f"Invalid file type '{ext}'. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}",
            field="file",
        )

    # Check content type
    if file.content_type and not file.content_type.startswith("image/"):
        raise ValidationException(
            f"Invalid content type '{file.content_type}'. Must be an image.",
            field="file",
        )
