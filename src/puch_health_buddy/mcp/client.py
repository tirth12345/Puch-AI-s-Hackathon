#!/usr/bin/env python3
"""
MCP Client Example for Puch AI Health Buddy
Demonstrates how to interact with the MCP server
"""

import json
import subprocess
import sys
from typing import Dict, Any

class PuchHealthMCPClient:
    """Simple MCP client for testing the health buddy server"""
    
    def __init__(self):
        self.server_id = "puch-health-buddy-mcp"
        self.server_name = "Puch AI Health Buddy MCP Server"
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "server_id": self.server_id,
            "server_name": self.server_name,
            "version": "1.0.0",
            "description": "AI-powered health assistant and fact-checker",
            "capabilities": {
                "tools": [
                    "analyze_health_symptoms",
                    "fact_check_health_claim",
                    "find_nearby_healthcare", 
                    "translate_health_info",
                    "get_health_emergency_guidance"
                ],
                "prompts": [
                    "health_consultation",
                    "medical_fact_check",
                    "emergency_assessment"
                ]
            },
            "supported_languages": [
                "en", "hi", "gu", "mr", "ta", "te",
                "kn", "ml", "bn", "pa", "or", "as"
            ]
        }
    
    def simulate_health_analysis(self, symptoms: str, language: str = "en") -> Dict[str, Any]:
        """Simulate health symptom analysis"""
        # This simulates what the MCP server would return
        return {
            "tool": "analyze_health_symptoms",
            "request": {
                "symptoms": symptoms,
                "language": language
            },
            "response": {
                "analysis": f"Health analysis for: {symptoms}",
                "urgency_level": "medium",
                "recommendations": [
                    "Rest and stay hydrated",
                    "Monitor symptoms",
                    "Consult healthcare provider if symptoms worsen"
                ],
                "disclaimer": "This is not medical advice. Consult healthcare professionals."
            },
            "server_id": self.server_id
        }
    
    def simulate_fact_check(self, claim: str, language: str = "en") -> Dict[str, Any]:
        """Simulate health fact checking"""
        return {
            "tool": "fact_check_health_claim",
            "request": {
                "claim": claim,
                "language": language
            },
            "response": {
                "verdict": "REQUIRES_VERIFICATION",
                "explanation": f"Fact-checking analysis for: {claim}",
                "sources": ["WHO", "CDC", "PIB Fact Check"],
                "recommendation": "Verify with official health sources"
            },
            "server_id": self.server_id
        }
    
    def simulate_location_search(self, location: str, language: str = "en") -> Dict[str, Any]:
        """Simulate healthcare facility search"""
        return {
            "tool": "find_nearby_healthcare",
            "request": {
                "location": location,
                "language": language
            },
            "response": {
                "facilities": [
                    {
                        "name": f"City Hospital - {location}",
                        "address": f"Main Street, {location}",
                        "rating": 4.2,
                        "services": ["Emergency", "General Medicine"]
                    },
                    {
                        "name": f"Health Clinic - {location}",
                        "address": f"Healthcare Avenue, {location}",
                        "rating": 4.0,
                        "services": ["General Practice", "Pediatrics"]
                    }
                ]
            },
            "server_id": self.server_id
        }
    
    def test_mcp_functionality(self):
        """Test MCP server functionality"""
        print(f"🏥 Testing {self.server_name}")
        print(f"Server ID: {self.server_id}")
        print("-" * 50)
        
        # Test health analysis
        print("1. Health Symptom Analysis:")
        result = self.simulate_health_analysis("I have fever and headache", "en")
        print(json.dumps(result, indent=2))
        print()
        
        # Test fact checking
        print("2. Health Fact Checking:")
        result = self.simulate_fact_check("Garlic prevents COVID-19", "en")
        print(json.dumps(result, indent=2))
        print()
        
        # Test location search
        print("3. Healthcare Facility Search:")
        result = self.simulate_location_search("Mumbai", "en")
        print(json.dumps(result, indent=2))
        print()
        
        # Test multilingual
        print("4. Multilingual Support:")
        result = self.simulate_health_analysis("मुझे बुखार है", "hi")
        print(json.dumps(result, indent=2))

def main():
    """Main function to run MCP client test"""
    client = PuchHealthMCPClient()
    
    print("=" * 60)
    print("🩺 Puch AI Health Buddy - MCP Client Test")
    print("=" * 60)
    
    # Display server info
    server_info = client.get_server_info()
    print("Server Information:")
    print(json.dumps(server_info, indent=2))
    print()
    
    # Test functionality
    client.test_mcp_functionality()
    
    print("\n" + "=" * 60)
    print("✅ MCP Client Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
