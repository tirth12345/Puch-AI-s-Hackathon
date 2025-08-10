#!/usr/bin/env python3
"""
Location service for finding nearby healthcare facilities
"""

import os
import requests
import logging

from ..services.translation_service import TranslationService

logger = logging.getLogger(__name__)

class LocationService:
    def __init__(self):
        self.google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        self.translation_service = TranslationService()

    def get_nearby_clinics(self, location: str, language: str = 'en') -> str:
        """Get nearby clinics using Google Maps API"""
        if not self.google_maps_api_key:
            return "Location services temporarily unavailable"

        search_query = f"hospitals near {location}"
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            'key': self.google_maps_api_key,
            'query': search_query,
            'type': 'hospital'
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                result = response.json()
                clinics = []
                for place in result.get('results', [])[:3]:  # Top 3 results
                    clinic_info = f"🏥 {place['name']}\n📍 {place['formatted_address']}\n⭐ Rating: {place.get('rating', 'N/A')}"
                    clinics.append(clinic_info)

                clinic_text = "🏥 *Nearby Healthcare Facilities:*\n\n" + "\n\n".join(clinics)
                return self.translation_service.translate_text(clinic_text, language)
        except Exception as e:
            logger.error(f"Maps API error: {e}")

        return self.translation_service.translate_text("Unable to fetch nearby clinics. Please contact local emergency services.", language)
