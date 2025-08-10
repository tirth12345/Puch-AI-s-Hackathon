#!/usr/bin/env python3
"""
Simplified MCP-Compatible Server for Puch AI Health Buddy
This version works without the official MCP SDK
"""

import asyncio
import json
import logging
import sys
from typing import Dict, Any, List
from datetime import datetime

from ..services.health_service import HealthService
from ..services.fact_check_service import FactCheckService
from ..services.translation_service import TranslationService
from ..services.location_service import LocationService

logger = logging.getLogger(__name__)

class SimpleMCPServer:
    """Simplified MCP-compatible server"""
    
    def __init__(self):
        self.server_id = "puch-health-buddy-mcp"
        self.server_name = "Puch AI Health Buddy MCP Server"
        self.server_version = "1.0.0"
        
        # Initialize services
        self.health_service = HealthService()
        self.fact_check_service = FactCheckService()
        self.translation_service = TranslationService()
        self.location_service = LocationService()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "server_id": self.server_id,
            "name": self.server_name,
            "version": self.server_version,
            "description": "AI-powered health assistant and fact-checker",
            "capabilities": {
                "tools": True,
                "prompts": True,
                "resources": False,
                "logging": True
            },
            "supported_languages": [
                "en", "hi", "gu", "mr", "ta", "te", 
                "kn", "ml", "bn", "pa", "or", "as"
            ],
            "tools": [
                "analyze_health_symptoms",
                "fact_check_health_claim", 
                "find_nearby_healthcare",
                "translate_health_info",
                "get_health_emergency_guidance"
            ]
        }
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """Get available tools"""
        return [
            {
                "name": "analyze_health_symptoms",
                "description": "Analyze health symptoms and provide medical guidance",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symptoms": {
                            "type": "string",
                            "description": "Description of health symptoms"
                        },
                        "language": {
                            "type": "string",
                            "description": "Preferred language for response",
                            "enum": ["en", "hi", "gu", "mr", "ta", "te", "kn", "ml", "bn", "pa", "or", "as"],
                            "default": "en"
                        }
                    },
                    "required": ["symptoms"]
                }
            },
            {
                "name": "fact_check_health_claim",
                "description": "Verify health information and detect misinformation",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "claim": {
                            "type": "string",
                            "description": "Health claim or information to verify"
                        },
                        "language": {
                            "type": "string",
                            "description": "Preferred language for response",
                            "enum": ["en", "hi", "gu", "mr", "ta", "te", "kn", "ml", "bn", "pa", "or", "as"],
                            "default": "en"
                        }
                    },
                    "required": ["claim"]
                }
            },
            {
                "name": "find_nearby_healthcare",
                "description": "Find nearby healthcare facilities",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City or area name to search for healthcare facilities"
                        },
                        "language": {
                            "type": "string",
                            "description": "Preferred language for response",
                            "enum": ["en", "hi", "gu", "mr", "ta", "te", "kn", "ml", "bn", "pa", "or", "as"],
                            "default": "en"
                        }
                    },
                    "required": ["location"]
                }
            },
            {
                "name": "translate_health_info",
                "description": "Translate health information between supported languages",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {
                            "type": "string",
                            "description": "Text to translate"
                        },
                        "target_language": {
                            "type": "string",
                            "description": "Target language for translation",
                            "enum": ["en", "hi", "gu", "mr", "ta", "te", "kn", "ml", "bn", "pa", "or", "as"]
                        },
                        "source_language": {
                            "type": "string",
                            "description": "Source language (auto-detect if not specified)",
                            "default": "auto"
                        }
                    },
                    "required": ["text", "target_language"]
                }
            },
            {
                "name": "get_health_emergency_guidance",
                "description": "Get emergency health guidance and identify urgent situations",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symptoms": {
                            "type": "string",
                            "description": "Emergency symptoms description"
                        },
                        "language": {
                            "type": "string",
                            "description": "Preferred language for response",
                            "enum": ["en", "hi", "gu", "mr", "ta", "te", "kn", "ml", "bn", "pa", "or", "as"],
                            "default": "en"
                        }
                    },
                    "required": ["symptoms"]
                }
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool with given arguments"""
        try:
            if tool_name == "analyze_health_symptoms":
                return await self._analyze_health_symptoms(arguments)
            elif tool_name == "fact_check_health_claim":
                return await self._fact_check_health_claim(arguments)
            elif tool_name == "find_nearby_healthcare":
                return await self._find_nearby_healthcare(arguments)
            elif tool_name == "translate_health_info":
                return await self._translate_health_info(arguments)
            elif tool_name == "get_health_emergency_guidance":
                return await self._get_health_emergency_guidance(arguments)
            else:
                return {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}"
                }
        except Exception as e:
            logger.error(f"Error in tool call {tool_name}: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def _analyze_health_symptoms(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health symptoms"""
        symptoms = arguments.get("symptoms", "")
        language = arguments.get("language", "en")
        
        if not symptoms:
            return {
                "success": False,
                "error": "Please provide symptoms to analyze"
            }
        
        try:
            analysis = self.health_service.analyze_health_query(symptoms, language)
            return {
                "success": True,
                "result": analysis,
                "tool": "analyze_health_symptoms"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error analyzing symptoms: {str(e)}"
            }
    
    async def _fact_check_health_claim(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Fact-check health claim"""
        claim = arguments.get("claim", "")
        language = arguments.get("language", "en")
        
        if not claim:
            return {
                "success": False,
                "error": "Please provide a health claim to verify"
            }
        
        try:
            result = self.fact_check_service.fact_check_query(claim, language)
            return {
                "success": True,
                "result": result,
                "tool": "fact_check_health_claim"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error fact-checking claim: {str(e)}"
            }
    
    async def _find_nearby_healthcare(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Find nearby healthcare facilities"""
        location = arguments.get("location", "")
        language = arguments.get("language", "en")
        
        if not location:
            return {
                "success": False,
                "error": "Please provide a location to search"
            }
        
        try:
            facilities = self.location_service.get_nearby_clinics(location, language)
            return {
                "success": True,
                "result": facilities,
                "tool": "find_nearby_healthcare"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error finding healthcare facilities: {str(e)}"
            }
    
    async def _translate_health_info(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Translate health information"""
        text = arguments.get("text", "")
        target_language = arguments.get("target_language", "en")
        source_language = arguments.get("source_language", "auto")
        
        if not text:
            return {
                "success": False,
                "error": "Please provide text to translate"
            }
        
        try:
            translated = self.translation_service.translate_text(text, target_language, source_language)
            return {
                "success": True,
                "result": translated,
                "tool": "translate_health_info"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Error translating text: {str(e)}"
            }
    
    async def _get_health_emergency_guidance(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get emergency health guidance"""
        symptoms = arguments.get("symptoms", "")
        language = arguments.get("language", "en")
        
        if not symptoms:
            return {
                "success": False,
                "error": "Please describe emergency symptoms"
            }
        
        try:
            # Add urgency check and emergency response
            analysis = self.health_service.analyze_health_query(symptoms, language)
            
            # Check for emergency indicators
            emergency_keywords = [
                'chest pain', 'difficulty breathing', 'unconscious', 'seizure',
                'stroke', 'heart attack', 'severe bleeding', 'poisoning'
            ]
            
            is_emergency = any(keyword in symptoms.lower() for keyword in emergency_keywords)
            
            if is_emergency:
                emergency_response = "🚨 **MEDICAL EMERGENCY DETECTED** 🚨\n\n"
                emergency_response += "CALL EMERGENCY SERVICES IMMEDIATELY:\n"
                emergency_response += "• India: 102 (Ambulance), 108 (Emergency)\n"
                emergency_response += "• Stay calm and follow dispatcher instructions\n"
                emergency_response += "• Do not leave patient alone\n\n"
                emergency_response += analysis
                
                if language != 'en':
                    emergency_response = self.translation_service.translate_text(emergency_response, language)
                
                return {
                    "success": True,
                    "result": emergency_response,
                    "tool": "get_health_emergency_guidance",
                    "emergency": True
                }
            else:
                return {
                    "success": True,
                    "result": analysis,
                    "tool": "get_health_emergency_guidance",
                    "emergency": False
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error processing emergency guidance: {str(e)}"
            }
    
    def start_server(self, port: int = 8000):
        """Start the simplified MCP server"""
        print(f"Starting {self.server_name}")
        print(f"Server ID: {self.server_id}")
        print(f"Version: {self.server_version}")
        print(f"Port: {port}")
        print("-" * 50)
        
        # Display server info
        info = self.get_server_info()
        print("Server Capabilities:")
        for capability, enabled in info["capabilities"].items():
            status = "[OK]" if enabled else "[--]"
            print(f"  {status} {capability}")
        
        print(f"\nSupported Languages: {', '.join(info['supported_languages'])}")
        print(f"Available Tools: {len(info['tools'])}")
        
        # List available tools
        print("\nAvailable Tools:")
        tools = self.get_tools()
        for tool in tools:
            print(f"  [OK] {tool['name']}")
        
        print("\n" + "=" * 50)
        print("MCP Server is ready!")
        print("=" * 50)
        
        # Save server configuration
        config = {
            "server_info": info,
            "tools": tools,
            "status": "running",
            "timestamp": datetime.now().isoformat()
        }
        
        with open("mcp_server_status.json", "w") as f:
            json.dump(config, f, indent=2)
        
        print("[OK] Server configuration saved to mcp_server_status.json")
        return True

def main():
    """Main function to start the server"""
    server = SimpleMCPServer()
    
    try:
        server.start_server()
        print("Server started successfully!")
        print("To test the server, use the test functions in the scripts/ directory")
        
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
