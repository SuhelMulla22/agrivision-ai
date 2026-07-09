"""
TensorFlow Model Service — handles model loading, preprocessing, and inference.

This is the heart of AgriVision AI. It loads a fine-tuned MobileNetV2 model
and provides fast, reliable predictions for crop disease detection.
"""

import json
import logging
import time
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
from PIL import Image

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class ModelService:
    """Manages the TensorFlow model lifecycle and inference."""

    def __init__(self):
        self._model = None
        self._class_names: List[str] = []
        self._class_mapping: Dict[int, Dict] = {}
        self._is_loaded = False
        self._model_version = settings.MODEL_VERSION

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded

    def load_model(self) -> None:
        """Load the TensorFlow model and class mapping from disk."""
        try:
            import tensorflow as tf

            model_path = settings.MODEL_DIR / settings.MODEL_NAME
            class_mapping_path = Path("data/class_mapping.json")

            if not model_path.exists():
                logger.warning(
                    f"Model file not found at {model_path}. "
                    "Running in DEMO mode with random predictions."
                )
                self._load_demo_mode()
                return

            # Load model with optimized settings
            self._model = tf.keras.models.load_model(
                str(model_path),
                compile=False,  # No need to compile for inference
            )

            # Warm up the model with a dummy prediction
            dummy_input = np.random.rand(1, settings.IMAGE_SIZE, settings.IMAGE_SIZE, 3).astype(np.float32)
            self._model.predict(dummy_input, verbose=0)

            # Load class mapping
            if class_mapping_path.exists():
                with open(class_mapping_path, "r") as f:
                    raw_mapping = json.load(f)
                    self._class_mapping = {
                        int(k): v for k, v in raw_mapping.items()
                    }
                    self._class_names = [
                        self._class_mapping[i]["name"]
                        for i in sorted(self._class_mapping.keys())
                    ]
            else:
                # Fallback: generate generic class names
                num_classes = self._model.output_shape[-1]
                self._class_names = [f"class_{i}" for i in range(num_classes)]

            self._is_loaded = True
            logger.info(
                f"Model loaded successfully. "
                f"Classes: {len(self._class_names)}, "
                f"Input shape: {self._model.input_shape}"
            )

        except ImportError:
            logger.error("TensorFlow not installed. Running in demo mode.")
            self._load_demo_mode()
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self._load_demo_mode()

    def _load_demo_mode(self) -> None:
        """Initialize demo mode — returns random predictions without a real model."""
        logger.info("Running in DEMO MODE — predictions will be simulated.")
        # Load class names from mapping if available
        class_mapping_path = Path("data/class_mapping.json")
        if class_mapping_path.exists():
            with open(class_mapping_path, "r") as f:
                raw_mapping = json.load(f)
                self._class_mapping = {
                    int(k): v for k, v in raw_mapping.items()
                }
                self._class_names = [
                    self._class_mapping[i]["name"]
                    for i in sorted(self._class_mapping.keys())
                ]
        else:
            # Minimal fallback
            self._class_names = [
                "Tomato___Early_blight",
                "Tomato___Late_blight",
                "Tomato___Healthy",
                "Potato___Early_blight",
                "Potato___Late_blight",
                "Potato___Healthy",
                "Corn___Common_rust",
                "Corn___Healthy",
                "Rice___Bacterial_leaf_blight",
                "Rice___Healthy",
            ]
        self._is_loaded = True

    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess a PIL image for model inference.

        Steps:
        1. Resize to model input size (224x224)
        2. Convert to RGB (handles RGBA, grayscale, etc.)
        3. Normalize pixel values to [0, 1]
        4. Add batch dimension
        """
        # Ensure RGB
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Resize with high-quality resampling
        image = image.resize(
            (settings.IMAGE_SIZE, settings.IMAGE_SIZE),
            Image.Resampling.LANCZOS,
        )

        # Convert to numpy array (keep raw pixel values [0, 255])
        # The model's internal layers (Rescaling) handle normalization.
        img_array = np.array(image, dtype=np.float32)

        # Add batch dimension: (H, W, C) → (1, H, W, C)
        img_array = np.expand_dims(img_array, axis=0)

        return img_array

    def predict_gemini(self, image: Image.Image, language: str = "en") -> Optional[Dict]:
        """
        Run inference using Gemini 1.5 Flash Vision API.
        """
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not configured. Skipping Gemini prediction.")
            return None

        try:
            import google.generativeai as genai
            genai.configure(api_key=api_key)

            # Keep image size reasonable for API transmission
            # Resize image to max 800x800 if larger
            img_copy = image.copy()
            if img_copy.width > 800 or img_copy.height > 800:
                img_copy.thumbnail((800, 800), Image.Resampling.LANCZOS)

            model = genai.GenerativeModel("gemini-2.5-flash")

            lang_map = {
                "en": "English",
                "hi": "Hindi",
                "mr": "Marathi"
            }
            lang_name = lang_map.get(language, "English")

            prompt = f"""
You are a world-class agronomy AI assistant and crop disease expert.
Analyze this image of a crop plant (it could be a leaf, fruit, stem, or root).
Identify the crop name, the specific disease (if any), and determine if the plant is healthy.
You must return a structured JSON object in {lang_name} language.
All text fields (crop, disease, description, symptoms, causes, treatments, prevention, severity_info) must be localized in {lang_name}.

The JSON response must follow this schema exactly:
{{
  "crop": "Name of the crop (e.g. Mango, Tomato, Wheat)",
  "disease": "Name of the disease (e.g. Anthracnose, Early Blight, Healthy)",
  "disease_id": "lowercase_snake_case_id (e.g. mango_anthracnose, healthy)",
  "confidence": 0.95,
  "is_healthy": false,
  "severity": "high", // one of "high", "moderate", "low", or null
  "description": "Detailed description of the disease...",
  "symptoms": ["symptom 1", "symptom 2"],
  "causes": ["cause 1", "cause 2"],
  "treatment": {{
    "organic": ["organic method 1"],
    "chemical": ["chemical method 1"]
  }},
  "prevention": ["prevention tip 1"],
  "severity_info": "instructions based on severity..."
}}
"""

            logger.info(f"Sending image to Gemini 2.5 Flash (lang: {language})...")
            start_time = time.perf_counter()
            response = model.generate_content(
                [img_copy, prompt],
                generation_config={"response_mime_type": "application/json"}
            )

            processing_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            data = json.loads(response.text.strip())
            
            predicted_class = data.get("disease_id", "unknown")
            if data.get("is_healthy", False):
                predicted_class = f"{data.get('crop', 'unknown').lower()}_healthy"

            top_predictions = [
                {
                    "class": predicted_class,
                    "confidence": float(data.get("confidence", 0.95))
                }
            ]

            return {
                "predicted_class": predicted_class,
                "confidence": float(data.get("confidence", 0.95)),
                "crop": data.get("crop", "Unknown"),
                "is_healthy": bool(data.get("is_healthy", False)),
                "severity": data.get("severity"),
                "top_predictions": top_predictions,
                "processing_time_ms": processing_time_ms,
                "model_version": "gemini-2.5-flash",
                "gemini_rich_info": {
                    "name": data.get("disease", "Unknown"),
                    "crop": data.get("crop", "Unknown"),
                    "description": data.get("description", ""),
                    "symptoms": data.get("symptoms", []),
                    "causes": data.get("causes", []),
                    "treatment": data.get("treatment", {}),
                    "prevention": data.get("prevention", []),
                    "severity_info": data.get("severity_info")
                }
            }

        except Exception as e:
            logger.error(f"Gemini prediction failed, falling back to OpenRouter/Local model: {e}", exc_info=True)
            return None

    def predict_openrouter(self, image: Image.Image, language: str = "en") -> Optional[Dict]:
        """
        Run inference using OpenRouter Vision API (meta-llama/llama-3.2-11b-vision-instruct or google/gemini-2.5-flash).
        """
        api_key = settings.OPENROUTER_API_KEY or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            logger.warning("OPENROUTER_API_KEY not configured. Skipping OpenRouter prediction.")
            return None

        try:
            import httpx
            import base64
            from io import BytesIO

            # Keep image size reasonable
            img_copy = image.copy()
            if img_copy.width > 800 or img_copy.height > 800:
                img_copy.thumbnail((800, 800), Image.Resampling.LANCZOS)

            # Convert to base64
            buffered = BytesIO()
            img_copy.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

            lang_map = {
                "en": "English",
                "hi": "Hindi",
                "mr": "Marathi"
            }
            lang_name = lang_map.get(language, "English")

            prompt = f"""
You are a world-class agronomy AI assistant and crop disease expert.
Analyze this image of a crop plant (it could be a leaf, fruit, stem, or root).
Identify the crop name, the specific disease (if any), and determine if the plant is healthy.
You must return a structured JSON object in {lang_name} language.
All text fields (crop, disease, description, symptoms, causes, treatments, prevention, severity_info) must be localized in {lang_name}.

The JSON response must follow this schema exactly:
{{
  "crop": "Name of the crop (e.g. Mango, Tomato, Wheat)",
  "disease": "Name of the disease (e.g. Anthracnose, Early Blight, Healthy)",
  "disease_id": "lowercase_snake_case_id (e.g. mango_anthracnose, healthy)",
  "confidence": 0.95,
  "is_healthy": false,
  "severity": "high", // one of "high", "moderate", "low", or null
  "description": "Detailed description of the disease...",
  "symptoms": ["symptom 1", "symptom 2"],
  "causes": ["cause 1", "cause 2"],
  "treatment": {{
    "organic": ["organic method 1"],
    "chemical": ["chemical method 1"]
  }},
  "prevention": ["prevention tip 1"],
  "severity_info": "instructions based on severity..."
}}
"""

            logger.info(f"Sending image to OpenRouter Vision API (lang: {language})...")
            start_time = time.perf_counter()

            model_name = "google/gemini-2.5-flash"
            
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://agrivision.ai",
                "X-Title": "AgriVision AI"
            }
            
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{img_str}"
                                }
                            }
                        ]
                    }
                ],
                "response_format": {"type": "json_object"},
                "max_tokens": 1000
            }

            res = httpx.post(url, headers=headers, json=payload, timeout=40.0)
            if res.status_code != 200:
                logger.warning(f"OpenRouter {model_name} failed ({res.status_code}: {res.text}). Trying Llama 3.2 Vision...")
                payload["model"] = "meta-llama/llama-3.2-11b-vision-instruct"
                res = httpx.post(url, headers=headers, json=payload, timeout=40.0)
                
            res.raise_for_status()
            response_data = res.json()
            
            # Extract content
            content_text = response_data["choices"][0]["message"]["content"]
            processing_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            data = json.loads(content_text.strip())
            
            predicted_class = data.get("disease_id", "unknown")
            if data.get("is_healthy", False):
                predicted_class = f"{data.get('crop', 'unknown').lower()}_healthy"

            top_predictions = [
                {
                    "class": predicted_class,
                    "confidence": float(data.get("confidence", 0.95))
                }
            ]

            return {
                "predicted_class": predicted_class,
                "confidence": float(data.get("confidence", 0.95)),
                "crop": data.get("crop", "Unknown"),
                "is_healthy": bool(data.get("is_healthy", False)),
                "severity": data.get("severity"),
                "top_predictions": top_predictions,
                "processing_time_ms": processing_time_ms,
                "model_version": f"openrouter-{response_data.get('model', 'gemini-2.5-flash')}",
                "gemini_rich_info": {
                    "name": data.get("disease", "Unknown"),
                    "crop": data.get("crop", "Unknown"),
                    "description": data.get("description", ""),
                    "symptoms": data.get("symptoms", []),
                    "causes": data.get("causes", []),
                    "treatment": data.get("treatment", {}),
                    "prevention": data.get("prevention", []),
                    "severity_info": data.get("severity_info")
                }
            }

        except Exception as e:
            logger.error(f"OpenRouter prediction failed, falling back to local model: {e}", exc_info=True)
            return None

    def predict(self, image: Image.Image, language: str = "en") -> Dict:
        """
        Run hybrid inference: try Gemini API first, then OpenRouter (Universal Fallback), and finally local TensorFlow.
        """
        # 1. Try Gemini
        gemini_result = self.predict_gemini(image, language)
        if gemini_result is not None:
            return gemini_result

        # 2. Try OpenRouter (Universal Secondary Engine)
        openrouter_result = self.predict_openrouter(image, language)
        if openrouter_result is not None:
            return openrouter_result

        # 3. Failover to Local model (Tertiary Offline Engine)
        return self.predict_local(image)

    def predict_local(self, image: Image.Image) -> Dict:
        """
        Run inference on an image and return predictions.

        Returns:
            {
                "predicted_class": str,
                "confidence": float,
                "top_predictions": [{"class": str, "confidence": float}, ...],
                "processing_time_ms": float,
            }
        """
        start_time = time.perf_counter()

        # Preprocess
        processed = self.preprocess_image(image)

        # Inference
        if self._model is not None:
            predictions = self._model.predict(processed, verbose=0)[0]
        else:
            # Demo mode — generate realistic random predictions
            predictions = self._demo_predictions()

        # Get top predictions
        top_indices = np.argsort(predictions)[::-1][:3]
        top_predictions = []
        for idx in top_indices:
            class_name = (
                self._class_mapping.get(idx, {}).get("name", f"class_{idx}")
                if self._class_mapping
                else self._class_names[idx] if idx < len(self._class_names) else f"class_{idx}"
            )
            top_predictions.append({
                "class": class_name,
                "confidence": round(float(predictions[idx]), 4),
            })

        # Best prediction
        best_idx = top_indices[0]
        best_class = top_predictions[0]["class"]
        best_confidence = top_predictions[0]["confidence"]

        # Determine if healthy
        is_healthy = "healthy" in best_class.lower()

        # Determine severity (only for diseased)
        severity = self._assess_severity(best_confidence, is_healthy)

        processing_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

        # Extract crop name from class
        crop_name = self._extract_crop_name(best_class)

        return {
            "predicted_class": best_class,
            "confidence": best_confidence,
            "crop": crop_name,
            "is_healthy": is_healthy,
            "severity": severity,
            "top_predictions": top_predictions,
            "processing_time_ms": processing_time_ms,
            "model_version": self._model_version,
        }

    def _demo_predictions(self) -> np.ndarray:
        """Generate realistic-looking random predictions for demo mode."""
        num_classes = len(self._class_names)
        # Create weighted random predictions
        raw = np.random.dirichlet(np.ones(num_classes) * 0.5)
        # Make one class dominant
        dominant_idx = np.random.randint(0, num_classes)
        raw[dominant_idx] = np.random.uniform(0.7, 0.98)
        # Normalize
        raw = raw / raw.sum()
        return raw

    @staticmethod
    def _assess_severity(confidence: float, is_healthy: bool) -> Optional[str]:
        """Assess disease severity based on confidence score."""
        if is_healthy:
            return None
        if confidence >= 0.85:
            return "high"
        elif confidence >= 0.60:
            return "moderate"
        else:
            return "low"

    @staticmethod
    def _extract_crop_name(class_name: str) -> str:
        """Extract crop name from class string like 'Tomato___Early_blight'."""
        if "___" in class_name:
            return class_name.split("___")[0]
        return class_name.split("_")[0] if "_" in class_name else class_name
