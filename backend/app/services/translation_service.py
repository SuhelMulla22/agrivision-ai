"""
Translation Service — handles multilingual content for disease information.

Supports: English (en), Hindi (hi), Marathi (mr)
"""

import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {"en", "hi", "mr"}
DEFAULT_LANGUAGE = "en"


class TranslationService:
    """Provides localized disease information."""

    def __init__(self):
        self._cache: Dict[str, Dict] = {}
        logger.info("Translation service initialized (EN/HI/MR)")

    def get_localized_content(
        self, content: Dict[str, Any], language: str = DEFAULT_LANGUAGE
    ) -> Any:
        """
        Extract the correct language version from a multilingual content dict.

        Args:
            content: Dict with language keys like {"en": "...", "hi": "...", "mr": "..."}
            language: Target language code

        Returns:
            Localized content for the requested language, falling back to English.
        """
        if not isinstance(content, dict):
            return content

        # Try requested language
        if language in content:
            return content[language]

        # Fallback to English
        if DEFAULT_LANGUAGE in content:
            return content[DEFAULT_LANGUAGE]

        # Return first available
        if content:
            return next(iter(content.values()))

        return None

    def localize_disease_info(
        self, disease_info: Dict, language: str = DEFAULT_LANGUAGE
    ) -> Dict:
        """
        Localize an entire disease info object.

        Translates all multilingual fields (name, description, symptoms, etc.)
        to the target language.
        """
        if not disease_info:
            return disease_info

        localized = {}

        for key, value in disease_info.items():
            if isinstance(value, dict):
                # Check if it's a language dict (has 'en', 'hi', 'mr' keys)
                if any(lang in value for lang in SUPPORTED_LANGUAGES):
                    localized[key] = self.get_localized_content(value, language)
                else:
                    # Nested dict (like treatment.organic, treatment.chemical)
                    localized[key] = self.localize_disease_info(value, language)
            elif isinstance(value, list):
                # Check if list items are language dicts
                if value and isinstance(value[0], dict) and any(
                    lang in value[0] for lang in SUPPORTED_LANGUAGES
                ):
                    localized[key] = [
                        self.get_localized_content(item, language) for item in value
                    ]
                else:
                    localized[key] = value
            else:
                localized[key] = value

        return localized

    @staticmethod
    def validate_language(language: str) -> str:
        """Validate and normalize language code."""
        if not language:
            return DEFAULT_LANGUAGE
        lang = language.lower().strip()[:2]
        if lang in SUPPORTED_LANGUAGES:
            return lang
        return DEFAULT_LANGUAGE
