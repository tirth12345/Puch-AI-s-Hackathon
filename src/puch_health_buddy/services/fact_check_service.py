#!/usr/bin/env python3
"""
Fact-checking service for health information
"""

import os
import logging
from typing import Dict

from ..utils.analyzers import FactChecker
from ..utils.formatters import MessageFormatter

logger = logging.getLogger(__name__)

class FactCheckService:
    def __init__(self):
        self.fact_checker = FactChecker()
        self.message_formatter = MessageFormatter()
        
        # Fact-check database - simplified
        self.fact_check_db = {
            'covid vaccine causes infertility': {
                'verdict': 'FALSE',
                'explanation': 'Multiple studies confirm COVID-19 vaccines do not affect fertility',
                'sources': 'WHO, CDC, PIB India'
            },
            'eating garlic prevents covid': {
                'verdict': 'FALSE',
                'explanation': 'No scientific evidence supports garlic as COVID-19 prevention',
                'sources': 'WHO, PIB Fact Check'
            }
        }

    def fact_check_query(self, text: str, language: str = 'en') -> str:
        """Check for misinformation using fact-check database"""
        text_lower = text.lower()

        for claim, info in self.fact_check_db.items():
            if any(word in text_lower for word in claim.split()):
                response = f"🔍 *Fact Check Result*\n\n"
                response += f"*Claim:* {claim.title()}\n"
                response += f"*Verdict:* {info['verdict']} ❌\n"
                response += f"*Explanation:* {info['explanation']}\n"
                response += f"*Sources:* {info['sources']}\n\n"
                response += "ℹ️ Always verify health information from official sources like WHO, CDC, or government health departments."

                return response

        # Use advanced fact checking
        check_result = self.fact_checker.check_claim(text)
        return self.message_formatter.format_fact_check_response(check_result, text)
