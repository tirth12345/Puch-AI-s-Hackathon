#!/usr/bin/env python3
"""
Helper utilities for Puch AI + Health Buddy
"""

import re
import json
import logging
import os
from typing import Dict
from datetime import datetime

logger = logging.getLogger(__name__)

def sanitize_phone_number(phone: str) -> str:
    """Sanitize and format phone number"""
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)

    # Handle Indian numbers
    if digits.startswith('91') and len(digits) == 12:
        return digits
    elif len(digits) == 10:
        return f"91{digits}"

    return digits

def log_interaction(phone_number: str, message: str, response: str, analysis: Dict = None):
    """Log user interactions for analytics"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'phone': sanitize_phone_number(phone_number),
        'message_length': len(message),
        'response_length': len(response),
        'analysis': analysis or {}
    }

    logger.info(f"User interaction logged: {json.dumps(log_entry)}")

def validate_api_keys() -> Dict[str, bool]:
    """Validate that required API keys are present"""
    required_keys = [
        'WHATSAPP_ACCESS_TOKEN',
        'WHATSAPP_PHONE_NUMBER_ID',
        'WHATSAPP_VERIFY_TOKEN'
    ]

    optional_keys = [
        'GOOGLE_TRANSLATE_API_KEY',
        'GOOGLE_MAPS_API_KEY'
    ]

    validation = {}

    for key in required_keys:
        validation[key] = bool(os.environ.get(key))

    for key in optional_keys:
        validation[key] = bool(os.environ.get(key))

    return validation

class LocationHelper:
    """Location and mapping utilities"""

    @staticmethod
    def extract_location(text: str) -> str:
        """Extract location from user message"""
        # Indian cities pattern
        indian_cities = [
            'mumbai', 'delhi', 'bangalore', 'hyderabad', 'ahmedabad',
            'chennai', 'kolkata', 'pune', 'jaipur', 'lucknow',
            'kanpur', 'nagpur', 'indore', 'thane', 'bhopal',
            'patna', 'vadodara', 'ghaziabad', 'ludhiana', 'agra'
        ]

        text_lower = text.lower()
        for city in indian_cities:
            if city in text_lower:
                return city.title()

        # Extract potential location using regex
        location_pattern = r'(?:in|at|near|from)\s+([a-zA-Z\s]{2,20})'
        matches = re.findall(location_pattern, text_lower)
        if matches:
            return matches[0].strip().title()

        return None

    @staticmethod
    def format_clinic_info(clinic_data: Dict) -> str:
        """Format clinic information for display"""
        name = clinic_data.get('name', 'Unknown')
        address = clinic_data.get('formatted_address', 'Address not available')
        rating = clinic_data.get('rating', 'N/A')

        return f"🏥 *{name}*\n📍 {address}\n⭐ Rating: {rating}"
