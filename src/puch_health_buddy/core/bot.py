#!/usr/bin/env python3
"""
WhatsApp Bot Core Logic
"""

import os
import json
import re
import logging
import requests
from datetime import datetime
from urllib.parse import quote
import hashlib
import hmac

from ..services.health_service import HealthService
from ..services.fact_check_service import FactCheckService
from ..services.translation_service import TranslationService
from ..services.location_service import LocationService
from ..utils.helpers import sanitize_phone_number, log_interaction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WhatsAppBot:
    def __init__(self):
        self.access_token = os.environ.get('WHATSAPP_ACCESS_TOKEN')
        self.phone_number_id = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
        self.verify_token = os.environ.get('WHATSAPP_VERIFY_TOKEN')
        self.webhook_secret = os.environ.get('WEBHOOK_SECRET')

        # Initialize services
        self.health_service = HealthService()
        self.fact_check_service = FactCheckService()
        self.translation_service = TranslationService()
        self.location_service = LocationService()

    def process_message(self, phone_number, message_text):
        """Process incoming WhatsApp messages"""
        # Detect language
        detected_language = self.translation_service.detect_language(message_text)

        message_lower = message_text.lower()

        # Welcome message
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'start', 'help']):
            response = "🙏 Welcome to Puch AI + Health Buddy!\n\n"
            response += "I can help you with:\n"
            response += "🏥 Health advice & guidance\n"
            response += "🔍 Fact-checking health information\n"
            response += "📍 Finding nearby clinics\n"
            response += "🌐 Support in multiple Indian languages\n\n"
            response += "Just describe your health concern or share any health information you want me to verify!"

        # Health-related queries
        elif any(word in message_lower for word in ['fever', 'cold', 'pain', 'sick', 'health', 'doctor', 'medicine']):
            response = self.health_service.analyze_health_query(message_text, detected_language)

        # Fact-checking queries
        elif any(word in message_lower for word in ['true', 'false', 'fact', 'check', 'verify', 'correct', 'myth']):
            response = self.fact_check_service.fact_check_query(message_text, detected_language)

        # Location-based clinic search
        elif any(word in message_lower for word in ['clinic', 'hospital', 'near', 'location', 'doctor near']):
            response = "📍 Please share your city name or area so I can find nearby healthcare facilities."
            if any(city in message_lower for city in ['ahmedabad', 'mumbai', 'delhi', 'bangalore', 'pune']):
                city_match = next(city for city in ['ahmedabad', 'mumbai', 'delhi', 'bangalore', 'pune'] if city in message_lower)
                response = self.location_service.get_nearby_clinics(city_match, detected_language)

        else:
            response = "🤔 I didn't quite understand. You can ask me about:\n"
            response += "• Health symptoms or concerns\n"
            response += "• Fact-checking health information\n"
            response += "• Finding nearby clinics\n\n"
            response += "Try saying: 'I have a fever' or 'Is this health news true?'"

        # Translate response if needed
        if detected_language != 'en':
            response = self.translation_service.translate_text(response, detected_language)

        # Log interaction
        log_interaction(phone_number, message_text, response)

        return response

    def send_message(self, phone_number, message_text):
        """Send WhatsApp message"""
        url = f"https://graph.facebook.com/v17.0/{self.phone_number_id}/messages"

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
        }

        data = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": message_text}
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False

def verify_signature(payload, signature, secret):
    """Verify webhook signature"""
    if not signature:
        return False

    try:
        signature = signature.replace('sha256=', '')
        expected_signature = hmac.new(
            secret.encode('utf-8'),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)
    except Exception as e:
        logger.error(f"Signature verification error: {e}")
        return False
