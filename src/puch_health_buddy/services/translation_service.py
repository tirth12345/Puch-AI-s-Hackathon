#!/usr/bin/env python3
"""
Translation service using Google Translate API
"""

import os
import requests
import logging

logger = logging.getLogger(__name__)

class TranslationService:
    def __init__(self):
        self.google_translate_api_key = os.environ.get('GOOGLE_TRANSLATE_API_KEY')

    def detect_language(self, text: str) -> str:
        """Detect language using Google Translate API"""
        if not self.google_translate_api_key:
            return 'en'  # Default to English

        url = f"https://translation.googleapis.com/language/translate/v2/detect"
        params = {
            'key': self.google_translate_api_key,
            'q': text
        }

        try:
            response = requests.post(url, params=params)
            if response.status_code == 200:
                result = response.json()
                return result['data']['detections'][0][0]['language']
        except Exception as e:
            logger.error(f"Language detection error: {e}")

        return 'en'  # Default to English

    def translate_text(self, text: str, target_lang: str, source_lang: str = 'auto') -> str:
        """Translate text using Google Translate API"""
        if not self.google_translate_api_key or target_lang == 'en':
            return text

        url = f"https://translation.googleapis.com/language/translate/v2"
        params = {
            'key': self.google_translate_api_key,
            'q': text,
            'target': target_lang,
            'source': source_lang
        }

        try:
            response = requests.post(url, params=params)
            if response.status_code == 200:
                result = response.json()
                return result['data']['translations'][0]['translatedText']
        except Exception as e:
            logger.error(f"Translation error: {e}")

        return text
