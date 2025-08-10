#!/usr/bin/env python3
"""
Configuration management for Puch AI + Health Buddy
"""

import os
from typing import Optional

class Config:
    """Application configuration"""

    # WhatsApp Business API
    WHATSAPP_ACCESS_TOKEN: Optional[str] = os.environ.get('WHATSAPP_ACCESS_TOKEN')
    WHATSAPP_PHONE_NUMBER_ID: Optional[str] = os.environ.get('WHATSAPP_PHONE_NUMBER_ID')
    WHATSAPP_VERIFY_TOKEN: Optional[str] = os.environ.get('WHATSAPP_VERIFY_TOKEN')
    WEBHOOK_SECRET: Optional[str] = os.environ.get('WEBHOOK_SECRET')

    # Google APIs
    GOOGLE_TRANSLATE_API_KEY: Optional[str] = os.environ.get('GOOGLE_TRANSLATE_API_KEY')
    GOOGLE_MAPS_API_KEY: Optional[str] = os.environ.get('GOOGLE_MAPS_API_KEY')

    # MCP Server Configuration
    MCP_SERVER_ID: str = "puch-health-buddy-mcp"
    MCP_SERVER_NAME: str = "Puch AI Health Buddy MCP Server"
    MCP_SERVER_VERSION: str = "1.0.0"
    MCP_SERVER_PORT: int = int(os.environ.get('MCP_PORT', 8000))

    # Application settings
    PORT: int = int(os.environ.get('PORT', 5000))
    DEBUG: bool = os.environ.get('DEBUG', 'False').lower() == 'true'

    # Language support
    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'hi': 'हिंदी',
        'gu': 'ગુજરાતી', 
        'mr': 'मराठी',
        'ta': 'தமிழ்',
        'te': 'తెలుగు',
        'kn': 'ಕನ್ನಡ',
        'ml': 'മലയാളം',
        'bn': 'বাংলা',
        'pa': 'ਪੰਜਾਬੀ',
        'or': 'ଓଡ଼ିଆ',
        'as': 'অসমীয়া'
    }

    # Health categories
    HEALTH_CATEGORIES = [
        'general_health',
        'fever_symptoms', 
        'respiratory_issues',
        'digestive_problems',
        'pain_management',
        'mental_health',
        'emergency_care'
    ]

    # Fact-check sources
    FACT_CHECK_SOURCES = [
        'PIB Fact Check',
        'WHO',
        'CDC',
        'Ministry of Health India',
        'ICMR',
        'AIIMS'
    ]

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Configuration selector
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
