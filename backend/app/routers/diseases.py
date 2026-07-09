"""
Disease information endpoints.
"""

import logging
from typing import List

from fastapi import APIRouter, Request

from app.core.exceptions import NotFoundException
from app.schemas.common import APIResponse
from app.schemas.disease import CropSummary, DiseaseListItem
from app.services.translation_service import TranslationService

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/crops", response_model=APIResponse[List[CropSummary]])
async def list_crops(request: Request):
    """
    List all supported crops and their diseases.
    """
    disease_service = request.app.state.disease_service
    crop_names = disease_service.get_supported_crops()

    crops = []
    for crop_name in crop_names:
        diseases = disease_service.get_diseases_for_crop(crop_name)
        crops.append(
            CropSummary(
                name=crop_name,
                disease_count=len(diseases),
                diseases=[
                    {"id": d["id"], "name": d["name"].get("en", d["id"])}
                    for d in diseases
                ],
            )
        )

    return APIResponse(success=True, data=crops)


@router.get("/crops/{crop}", response_model=APIResponse[CropSummary])
async def get_crop(crop: str, request: Request):
    """
    Get information about a specific crop.
    """
    disease_service = request.app.state.disease_service
    diseases = disease_service.get_diseases_for_crop(crop)

    if not diseases:
        raise NotFoundException("Crop", crop)

    crop_info = CropSummary(
        name=crop,
        disease_count=len(diseases),
        diseases=[
            DiseaseListItem(
                id=d["id"],
                name=d["name"].get("en", d["id"]),
                crop=d["crop"],
            )
            for d in diseases
        ],
    )

    return APIResponse(success=True, data=crop_info)


@router.get("/diseases/{disease_id}")
async def get_disease(
    disease_id: str,
    request: Request,
    language: str = "en",
):
    """
    Get detailed information about a specific disease.
    """
    disease_service = request.app.state.disease_service
    translation_service = request.app.state.translation_service

    disease_info = disease_service.get_disease_info(disease_id)
    if not disease_info:
        raise NotFoundException("Disease", disease_id)

    lang = TranslationService.validate_language(language)
    localized = translation_service.localize_disease_info(disease_info, lang)

    return APIResponse(success=True, data=localized)
