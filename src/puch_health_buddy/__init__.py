#!/usr/bin/env python3
"""
Puch AI + Health Buddy - WhatsApp Health & Fact-Checking Bot
A comprehensive WhatsApp bot that provides health assistance and fact-checking services
"""

__version__ = "1.0.0"
__author__ = "Puch AI Team"
__email__ = "contact@puchai.com"
__description__ = "AI-powered WhatsApp health assistant and fact-checker"

from .core.app import create_app
from .core.bot import WhatsAppBot

__all__ = ['create_app', 'WhatsAppBot']
