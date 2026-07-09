"""
Prediction-related Pydantic schemas.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class TopPrediction(BaseModel):
    """A single prediction with confidence."""

    disease: str = Field(..., description="Disease name")
    confidence: float = Field(..., ge=0, le=1, description="Confidence score (0-1)")


class TreatmentInfo(BaseModel):
    """Treatment recommendations."""

    organic: List[str] = Field(default_factory=list, description="Organic treatment methods")
    chemical: List[str] = Field(default_factory=list, description="Chemical treatment methods")


class DiseaseInfoResponse(BaseModel):
    """Complete disease information."""

    name: str = Field(..., description="Disease name")
    crop: str = Field(..., description="Affected crop")
    description: str = Field(..., description="Disease description")
    symptoms: List[str] = Field(default_factory=list, description="Observable symptoms")
    causes: List[str] = Field(default_factory=list, description="Disease causes")
    treatment: TreatmentInfo = Field(default_factory=TreatmentInfo)
    prevention: List[str] = Field(default_factory=list, description="Prevention tips")
    severity_info: Optional[str] = Field(None, description="Severity-specific guidance")


class PredictionData(BaseModel):
    """Complete prediction response data."""

    disease: str = Field(..., description="Predicted disease name")
    disease_id: str = Field(..., description="Disease identifier")
    crop: str = Field(..., description="Detected crop")
    confidence: float = Field(..., ge=0, le=1, description="Prediction confidence")
    severity: Optional[str] = Field(None, description="Disease severity (high/moderate/low)")
    is_healthy: bool = Field(False, description="Whether the plant is healthy")
    top_predictions: List[TopPrediction] = Field(
        default_factory=list, description="Top 3 predictions"
    )
    disease_info: DiseaseInfoResponse = Field(
        ..., description="Detailed disease information"
    )
    language: str = Field("en", description="Response language")
    processing_time_ms: float = Field(
        ..., description="Total processing time in milliseconds"
    )


class PredictionRequest(BaseModel):
    """Prediction request parameters."""

    language: Optional[str] = Field(
        "en",
        description="Preferred response language (en/hi/mr)",
        pattern="^(en|hi|mr)$",
    )
