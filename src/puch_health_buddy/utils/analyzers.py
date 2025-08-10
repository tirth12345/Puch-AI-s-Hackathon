#!/usr/bin/env python3
"""
Analysis utilities for health and fact-checking
"""

import re
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class HealthAnalyzer:
    """Advanced health query analysis"""

    def __init__(self):
        self.symptom_patterns = {
            'fever': ['fever', 'high temperature', 'hot', 'burning', 'chills'],
            'cold': ['cold', 'cough', 'runny nose', 'sneezing', 'congestion'],
            'headache': ['headache', 'head pain', 'migraine', 'head ache'],
            'stomach': ['stomach', 'belly', 'abdominal', 'nausea', 'vomit'],
            'chest': ['chest pain', 'breathing', 'shortness of breath', 'cough'],
            'skin': ['rash', 'itching', 'skin', 'allergy', 'hives'],
            'joint': ['joint pain', 'arthritis', 'stiff', 'swelling']
        }

        self.urgency_indicators = [
            'severe', 'intense', 'unbearable', 'emergency', 'urgent',
            'chest pain', 'difficulty breathing', 'blood', 'unconscious',
            'seizure', 'stroke', 'heart attack'
        ]

    def analyze_symptoms(self, text: str) -> Dict:
        """Analyze symptoms from user input"""
        text_lower = text.lower()

        detected_symptoms = []
        urgency_level = 'low'

        # Check for symptom patterns
        for category, patterns in self.symptom_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                detected_symptoms.append(category)

        # Check urgency
        if any(indicator in text_lower for indicator in self.urgency_indicators):
            urgency_level = 'high'
        elif len(detected_symptoms) > 2:
            urgency_level = 'medium'

        return {
            'symptoms': detected_symptoms,
            'urgency': urgency_level,
            'requires_immediate_attention': urgency_level == 'high',
            'timestamp': datetime.now().isoformat()
        }

class FactChecker:
    """Advanced fact-checking functionality"""

    def __init__(self):
        self.misinformation_patterns = {
            'covid_myths': [
                'covid vaccine infertility',
                'garlic prevents covid',
                '5g causes covid',
                'drinking cow urine cures covid'
            ],
            'home_remedies': [
                'hot water kills virus',
                'alcohol disinfects body',
                'vitamin c prevents all diseases'
            ],
            'general_health': [
                'sugar causes diabetes directly',
                'all bacteria are harmful',
                'natural means safe'
            ]
        }

    def check_claim(self, text: str) -> Dict:
        """Check if text contains potential misinformation"""
        text_lower = text.lower()

        for category, patterns in self.misinformation_patterns.items():
            for pattern in patterns:
                if any(word in text_lower for word in pattern.split()):
                    return {
                        'potentially_false': True,
                        'category': category,
                        'confidence': 'high',
                        'recommendation': 'verify_with_official_sources'
                    }

        return {
            'potentially_false': False,
            'category': 'general',
            'confidence': 'low',
            'recommendation': 'general_verification'
        }
