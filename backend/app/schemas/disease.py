"""
Disease-related Pydantic schemas.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class CropSummary(BaseModel):
    """Summary of a supported crop."""

    name: str = Field(..., description="Crop name")
    disease_count: int = Field(..., description="Number of known diseases")
    diseases: List[Dict[str, str]] = Field(
        default_factory=list, description="List of diseases"
    )


class DiseaseListItem(BaseModel):
    """Disease list item."""

    id: str = Field(..., description="Disease ID")
    name: str = Field(..., description="Disease name")
    crop: str = Field(..., description="Affected crop")
