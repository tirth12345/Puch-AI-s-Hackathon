#!/usr/bin/env python3
"""
Message formatting utilities
"""

from typing import Dict

class MessageFormatter:
    """Message formatting utilities"""

    @staticmethod
    def format_health_response(analysis: Dict, language: str = 'en') -> str:
        """Format health analysis into user-friendly message"""
        symptoms = analysis.get('symptoms', [])
        urgency = analysis.get('urgency', 'low')

        if urgency == 'high':
            response = "🚨 *URGENT MEDICAL ATTENTION NEEDED*\n\n"
            response += "Based on your symptoms, please seek immediate medical care or call emergency services.\n\n"
        elif urgency == 'medium':
            response = "⚠️ *Medical Consultation Recommended*\n\n"
            response += "Your symptoms suggest you should consult a healthcare professional soon.\n\n"
        else:
            response = "🩺 *General Health Guidance*\n\n"

        if symptoms:
            response += f"*Detected concerns:* {', '.join(symptoms).title()}\n\n"

        response += "*General advice:*\n"
        response += "• Stay hydrated and rest\n"
        response += "• Monitor your symptoms\n"
        response += "• Consult a doctor if symptoms worsen\n\n"

        response += "*Disclaimer:* This is not a medical diagnosis. Please consult healthcare professionals for proper evaluation."

        return response

    @staticmethod
    def format_fact_check_response(check_result: Dict, claim: str) -> str:
        """Format fact-check result"""
        potentially_false = check_result.get('potentially_false', False)
        category = check_result.get('category', 'general')

        if potentially_false:
            response = "🔍 *Fact Check Alert*\n\n"
            response += "⚠️ This claim may contain misinformation\n"
            response += f"*Category:* {category.replace('_', ' ').title()}\n\n"
            response += "*Recommendation:* Please verify this information with official health sources\n\n"
        else:
            response = "🔍 *Fact Check*\n\n"
            response += "✅ No obvious misinformation detected\n\n"
            response += "*Recommendation:* Always cross-reference health information with reliable sources\n\n"

        response += "*Trusted sources:*\n• WHO (World Health Organization)\n• PIB Fact Check\n• Your local health department"

        return response
