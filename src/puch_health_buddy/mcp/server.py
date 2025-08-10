#!/usr/bin/env python3
"""
MCP Server for Puch AI Health Buddy
Model Context Protocol server implementation for health assistance
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime

# Note: MCP imports will be available after installing the mcp package
# Uncomment these imports after running: pip install mcp
# from mcp.server import Server
# from mcp.server.models import InitializationOptions
# from mcp.server.stdio import stdio_server
# from mcp.types import (
#     CallToolRequest,
#     CallToolResult,
#     ListToolsRequest,
#     ListToolsResult,
#     Tool,
#     TextContent,
#     GetPromptRequest,
#     GetPromptResult,
#     ListPromptsRequest,
#     ListPromptsResult,
#     Prompt,
#     PromptArgument
# )

from ..services.health_service import HealthService
from ..services.fact_check_service import FactCheckService
from ..services.translation_service import TranslationService
from ..services.location_service import LocationService

logger = logging.getLogger(__name__)

class PuchHealthMCPServer:
    """MCP Server for Puch AI Health Buddy"""
    
    def __init__(self):
        self.server_id = "puch-health-buddy-mcp-server"
        self.server_name = "Puch AI Health Buddy MCP Server"
        self.server_version = "1.0.0"
        
        # Initialize services
        self.health_service = HealthService()
        self.fact_check_service = FactCheckService()
        self.translation_service = TranslationService()
        self.location_service = LocationService()
        
        # Create MCP server instance
        self.server = Server(self.server_name)
        
        # Register handlers
        self._register_handlers()
    
    def _register_handlers(self):
        """Register MCP server handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> ListToolsResult:
            """List available tools"""
            tools = [
                Tool(
                    name="analyze_health_symptoms",
                    description="Analyze health symptoms and provide medical guidance",
                    inputSchema={
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
                ),
                Tool(
                    name="fact_check_health_claim",
                    description="Verify health information and detect misinformation",
                    inputSchema={
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
                ),
                Tool(
                    name="find_nearby_healthcare",
                    description="Find nearby healthcare facilities",
                    inputSchema={
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
                ),
                Tool(
                    name="translate_health_info",
                    description="Translate health information between supported languages",
                    inputSchema={
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
                ),
                Tool(
                    name="get_health_emergency_guidance",
                    description="Get emergency health guidance and identify urgent situations",
                    inputSchema={
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
                )
            ]
            return ListToolsResult(tools=tools)
        
        @self.server.call_tool()
        async def handle_call_tool(request: CallToolRequest) -> CallToolResult:
            """Handle tool calls"""
            try:
                if request.name == "analyze_health_symptoms":
                    return await self._analyze_health_symptoms(request.arguments)
                elif request.name == "fact_check_health_claim":
                    return await self._fact_check_health_claim(request.arguments)
                elif request.name == "find_nearby_healthcare":
                    return await self._find_nearby_healthcare(request.arguments)
                elif request.name == "translate_health_info":
                    return await self._translate_health_info(request.arguments)
                elif request.name == "get_health_emergency_guidance":
                    return await self._get_health_emergency_guidance(request.arguments)
                else:
                    raise ValueError(f"Unknown tool: {request.name}")
            except Exception as e:
                logger.error(f"Error in tool call {request.name}: {e}")
                return CallToolResult(
                    content=[TextContent(type="text", text=f"Error: {str(e)}")],
                    isError=True
                )
        
        @self.server.list_prompts()
        async def handle_list_prompts() -> ListPromptsResult:
            """List available prompts"""
            prompts = [
                Prompt(
                    name="health_consultation",
                    description="Interactive health consultation prompt",
                    arguments=[
                        PromptArgument(
                            name="patient_query",
                            description="Patient's health query or symptoms",
                            required=True
                        ),
                        PromptArgument(
                            name="language",
                            description="Preferred language for consultation",
                            required=False
                        )
                    ]
                ),
                Prompt(
                    name="medical_fact_check",
                    description="Medical fact-checking prompt",
                    arguments=[
                        PromptArgument(
                            name="health_claim",
                            description="Health claim to verify",
                            required=True
                        ),
                        PromptArgument(
                            name="language",
                            description="Preferred language for response",
                            required=False
                        )
                    ]
                ),
                Prompt(
                    name="emergency_assessment",
                    description="Emergency health assessment prompt",
                    arguments=[
                        PromptArgument(
                            name="emergency_symptoms",
                            description="Emergency symptoms description",
                            required=True
                        ),
                        PromptArgument(
                            name="language",
                            description="Preferred language for response",
                            required=False
                        )
                    ]
                )
            ]
            return ListPromptsResult(prompts=prompts)
        
        @self.server.get_prompt()
        async def handle_get_prompt(request: GetPromptRequest) -> GetPromptResult:
            """Handle prompt requests"""
            if request.name == "health_consultation":
                return await self._get_health_consultation_prompt(request.arguments)
            elif request.name == "medical_fact_check":
                return await self._get_medical_fact_check_prompt(request.arguments)
            elif request.name == "emergency_assessment":
                return await self._get_emergency_assessment_prompt(request.arguments)
            else:
                raise ValueError(f"Unknown prompt: {request.name}")
    
    async def _analyze_health_symptoms(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Analyze health symptoms"""
        symptoms = arguments.get("symptoms", "")
        language = arguments.get("language", "en")
        
        if not symptoms:
            return CallToolResult(
                content=[TextContent(type="text", text="Please provide symptoms to analyze")],
                isError=True
            )
        
        try:
            analysis = self.health_service.analyze_health_query(symptoms, language)
            return CallToolResult(
                content=[TextContent(type="text", text=analysis)]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error analyzing symptoms: {str(e)}")],
                isError=True
            )
    
    async def _fact_check_health_claim(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Fact-check health claim"""
        claim = arguments.get("claim", "")
        language = arguments.get("language", "en")
        
        if not claim:
            return CallToolResult(
                content=[TextContent(type="text", text="Please provide a health claim to verify")],
                isError=True
            )
        
        try:
            result = self.fact_check_service.fact_check_query(claim, language)
            return CallToolResult(
                content=[TextContent(type="text", text=result)]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error fact-checking claim: {str(e)}")],
                isError=True
            )
    
    async def _find_nearby_healthcare(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Find nearby healthcare facilities"""
        location = arguments.get("location", "")
        language = arguments.get("language", "en")
        
        if not location:
            return CallToolResult(
                content=[TextContent(type="text", text="Please provide a location to search")],
                isError=True
            )
        
        try:
            facilities = self.location_service.get_nearby_clinics(location, language)
            return CallToolResult(
                content=[TextContent(type="text", text=facilities)]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error finding healthcare facilities: {str(e)}")],
                isError=True
            )
    
    async def _translate_health_info(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Translate health information"""
        text = arguments.get("text", "")
        target_language = arguments.get("target_language", "en")
        source_language = arguments.get("source_language", "auto")
        
        if not text:
            return CallToolResult(
                content=[TextContent(type="text", text="Please provide text to translate")],
                isError=True
            )
        
        try:
            translated = self.translation_service.translate_text(text, target_language, source_language)
            return CallToolResult(
                content=[TextContent(type="text", text=translated)]
            )
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error translating text: {str(e)}")],
                isError=True
            )
    
    async def _get_health_emergency_guidance(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Get emergency health guidance"""
        symptoms = arguments.get("symptoms", "")
        language = arguments.get("language", "en")
        
        if not symptoms:
            return CallToolResult(
                content=[TextContent(type="text", text="Please describe emergency symptoms")],
                isError=True
            )
        
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
                
                return CallToolResult(
                    content=[TextContent(type="text", text=emergency_response)]
                )
            else:
                return CallToolResult(
                    content=[TextContent(type="text", text=analysis)]
                )
                
        except Exception as e:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Error processing emergency guidance: {str(e)}")],
                isError=True
            )
    
    async def _get_health_consultation_prompt(self, arguments: Dict[str, Any]) -> GetPromptResult:
        """Get health consultation prompt"""
        patient_query = arguments.get("patient_query", "")
        language = arguments.get("language", "en")
        
        prompt_text = f"""
You are Puch AI Health Buddy, an AI-powered health assistant designed to help users with health-related queries and fact-checking.

Patient Query: {patient_query}
Preferred Language: {language}

Please provide:
1. A thorough analysis of the symptoms or health concern
2. General medical advice and recommendations
3. When to seek professional medical attention
4. Appropriate disclaimers about not replacing professional medical advice

Respond in the specified language ({language}) and maintain a compassionate, helpful tone while being medically responsible.
"""
        
        return GetPromptResult(
            description="Health consultation prompt for patient query",
            messages=[
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt_text
                    }
                }
            ]
        )
    
    async def _get_medical_fact_check_prompt(self, arguments: Dict[str, Any]) -> GetPromptResult:
        """Get medical fact-check prompt"""
        health_claim = arguments.get("health_claim", "")
        language = arguments.get("language", "en")
        
        prompt_text = f"""
You are Puch AI Health Buddy's fact-checking system. Analyze the following health claim for accuracy:

Health Claim: {health_claim}
Response Language: {language}

Please provide:
1. Verification status (TRUE/FALSE/PARTIALLY TRUE/UNCLEAR)
2. Detailed explanation of the claim's accuracy
3. Scientific evidence or lack thereof
4. Trusted sources for accurate information
5. Why misinformation can be harmful

Base your response on trusted medical sources like WHO, CDC, PIB Fact Check, and peer-reviewed research.
"""
        
        return GetPromptResult(
            description="Medical fact-checking prompt",
            messages=[
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt_text
                    }
                }
            ]
        )
    
    async def _get_emergency_assessment_prompt(self, arguments: Dict[str, Any]) -> GetPromptResult:
        """Get emergency assessment prompt"""
        emergency_symptoms = arguments.get("emergency_symptoms", "")
        language = arguments.get("language", "en")
        
        prompt_text = f"""
You are Puch AI Health Buddy's emergency assessment system. Evaluate these symptoms for emergency severity:

Emergency Symptoms: {emergency_symptoms}
Response Language: {language}

CRITICAL: If this appears to be a medical emergency, IMMEDIATELY advise calling emergency services (102/108 in India).

Assess:
1. Emergency severity level (LOW/MEDIUM/HIGH/CRITICAL)
2. Immediate actions to take
3. Emergency contact information
4. What NOT to do
5. When to seek immediate medical attention

Prioritize patient safety above all else.
"""
        
        return GetPromptResult(
            description="Emergency health assessment prompt",
            messages=[
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": prompt_text
                    }
                }
            ]
        )

async def main():
    """Main function to run the MCP server"""
    server_instance = PuchHealthMCPServer()
    
    # Run the server with stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server_instance.server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=server_instance.server_name,
                server_version=server_instance.server_version,
                capabilities=server_instance.server.get_capabilities()
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
