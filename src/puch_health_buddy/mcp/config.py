#!/usr/bin/env python3
"""
MCP Configuration for Puch AI Health Buddy
"""

import json
from typing import Dict, Any

class MCPConfig:
    """MCP Server Configuration"""
    
    # Server identification
    SERVER_ID = "puch-health-buddy-mcp"
    SERVER_NAME = "Puch AI Health Buddy MCP Server"
    SERVER_VERSION = "1.0.0"
    SERVER_DESCRIPTION = "AI-powered health assistant and fact-checker via MCP"
    
    # Server capabilities
    CAPABILITIES = {
        "tools": True,
        "prompts": True,
        "resources": False,
        "logging": True
    }
    
    # Supported languages
    SUPPORTED_LANGUAGES = [
        "en", "hi", "gu", "mr", "ta", "te", 
        "kn", "ml", "bn", "pa", "or", "as"
    ]
    
    # Tool configurations
    TOOLS_CONFIG = {
        "analyze_health_symptoms": {
            "enabled": True,
            "rate_limit": 100,  # requests per hour
            "requires_auth": False
        },
        "fact_check_health_claim": {
            "enabled": True,
            "rate_limit": 50,
            "requires_auth": False
        },
        "find_nearby_healthcare": {
            "enabled": True,
            "rate_limit": 30,
            "requires_auth": False
        },
        "translate_health_info": {
            "enabled": True,
            "rate_limit": 200,
            "requires_auth": False
        },
        "get_health_emergency_guidance": {
            "enabled": True,
            "rate_limit": 50,
            "requires_auth": False
        }
    }
    
    @classmethod
    def get_mcp_manifest(cls) -> Dict[str, Any]:
        """Generate MCP server manifest"""
        return {
            "schema_version": "0.1.0",
            "name": cls.SERVER_NAME,
            "version": cls.SERVER_VERSION,
            "description": cls.SERVER_DESCRIPTION,
            "author": "Puch AI Team",
            "license": "MIT",
            "homepage": "https://github.com/tirth12345/Puch-AI-s-Hackathon",
            "capabilities": cls.CAPABILITIES,
            "supported_languages": cls.SUPPORTED_LANGUAGES,
            "tools": list(cls.TOOLS_CONFIG.keys()),
            "server": {
                "command": ["python", "-m", "src.puch_health_buddy.mcp.server"],
                "args": [],
                "env": {}
            }
        }
    
    @classmethod
    def save_manifest(cls, filepath: str):
        """Save MCP manifest to file"""
        manifest = cls.get_mcp_manifest()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    @classmethod
    def get_server_info(cls) -> Dict[str, Any]:
        """Get server information for registration"""
        return {
            "server_id": cls.SERVER_ID,
            "name": cls.SERVER_NAME,
            "version": cls.SERVER_VERSION,
            "description": cls.SERVER_DESCRIPTION,
            "capabilities": cls.CAPABILITIES,
            "endpoint": "stdio",  # Using stdio transport
            "supported_languages": cls.SUPPORTED_LANGUAGES
        }
