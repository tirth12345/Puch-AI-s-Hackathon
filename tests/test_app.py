#!/usr/bin/env python3
"""
Test suite for Puch AI + Health Buddy
"""

import unittest
import json
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from unittest.mock import Mock, patch
from puch_health_buddy.core.app import create_app
from puch_health_buddy.core.bot import WhatsAppBot

class TestWhatsAppBot(unittest.TestCase):

    def setUp(self):
        self.bot = WhatsAppBot()
        self.app = create_app().test_client()
        self.app.testing = True

    def test_process_health_query(self):
        """Test health query processing"""
        message = "I have fever and headache"
        response = self.bot.process_message("1234567890", message)
        self.assertIn("fever", response.lower())
        self.assertIn("health", response.lower())

    def test_greeting_message(self):
        """Test greeting response"""
        message = "Hello"
        response = self.bot.process_message("1234567890", message)
        self.assertIn("welcome", response.lower())
        self.assertIn("health", response.lower())

    def test_webhook_verification(self):
        """Test webhook verification endpoint"""
        with patch.dict('os.environ', {'WHATSAPP_VERIFY_TOKEN': 'test_token'}):
            response = self.app.get('/webhook?hub.mode=subscribe&hub.verify_token=test_token&hub.challenge=test_challenge')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data.decode(), 'test_challenge')

    def test_webhook_verification_failure(self):
        """Test webhook verification failure"""
        response = self.app.get('/webhook?hub.mode=subscribe&hub.verify_token=wrong_token&hub.challenge=test_challenge')
        self.assertEqual(response.status_code, 403)

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['status'], 'healthy')

class TestUtilities(unittest.TestCase):

    def setUp(self):
        from puch_health_buddy.utils.analyzers import HealthAnalyzer, FactChecker
        from puch_health_buddy.utils.helpers import LocationHelper
        self.health_analyzer = HealthAnalyzer()
        self.fact_checker = FactChecker()
        self.location_helper = LocationHelper()

    def test_symptom_analysis(self):
        """Test symptom analysis"""
        result = self.health_analyzer.analyze_symptoms("I have severe fever and headache")
        self.assertIn('fever', result['symptoms'])
        self.assertEqual(result['urgency'], 'high')

    def test_fact_checking(self):
        """Test fact checking functionality"""
        result = self.fact_checker.check_claim("Garlic prevents COVID-19")
        self.assertTrue(result['potentially_false'])

    def test_location_extraction(self):
        """Test location extraction"""
        location = self.location_helper.extract_location("Find hospitals in Mumbai")
        self.assertEqual(location, "Mumbai")

if __name__ == '__main__':
    unittest.main()
