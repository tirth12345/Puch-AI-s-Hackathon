#!/usr/bin/env python3
"""
Health Service for analyzing health queries
"""

import os
import logging
from typing import Dict, List

from ..utils.analyzers import HealthAnalyzer
from ..utils.formatters import MessageFormatter

logger = logging.getLogger(__name__)

class HealthService:
    def __init__(self):
        self.health_analyzer = HealthAnalyzer()
        self.message_formatter = MessageFormatter()
        
        # Medical knowledge base - simplified for demo
        self.medical_knowledge = {
            'fever': {
                'symptoms': ['high temperature', 'sweating', 'chills', 'headache'],
                'advice': 'Rest, drink fluids, take paracetamol if needed. See doctor if fever >101°F or persists >3 days.',
                'urgent_signs': ['difficulty breathing', 'severe headache', 'chest pain']
            },
            'cold': {
                'symptoms': ['runny nose', 'cough', 'sore throat', 'sneezing'],
                'advice': 'Rest, warm liquids, honey for cough. Usually resolves in 7-10 days.',
                'urgent_signs': ['high fever', 'severe throat pain', 'breathing difficulty']
            },
            'stomach_pain': {
                'symptoms': ['abdominal pain', 'nausea', 'bloating'],
                'advice': 'Light foods, avoid spicy/oily foods. See doctor if severe or persistent.',
                'urgent_signs': ['severe pain', 'blood in stool', 'persistent vomiting']
            }
        }

    def analyze_health_query(self, text: str, language: str = 'en') -> str:
        """Analyze health-related queries using medical knowledge base"""
        text_lower = text.lower()

        # Analyze symptoms using the health analyzer
        analysis = self.health_analyzer.analyze_symptoms(text)

        # Simple keyword matching for demo
        for condition, info in self.medical_knowledge.items():
            if condition in text_lower or any(symptom in text_lower for symptom in info['symptoms']):
                response = f"🩺 *Health Information - {condition.title()}*\n\n"
                response += f"*Symptoms:* {', '.join(info['symptoms'])}\n\n"
                response += f"*General Advice:* {info['advice']}\n\n"
                response += f"⚠️ *Seek immediate medical help if:* {', '.join(info['urgent_signs'])}\n\n"
                response += "*Disclaimer:* This is general information only. Please consult a healthcare professional for proper diagnosis."

                return response

        # Use advanced analysis for better response
        return self.message_formatter.format_health_response(analysis, language)
