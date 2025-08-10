#!/usr/bin/env python3
"""
MCP Integration for Puch AI Health Buddy
Provides MCP server information and utilities
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import Config
from .config import MCPConfig

def get_mcp_server_id() -> str:
    """Get the MCP server ID"""
    return Config.MCP_SERVER_ID

def get_mcp_server_info() -> dict:
    """Get complete MCP server information"""
    return {
        "server_id": Config.MCP_SERVER_ID,
        "server_name": Config.MCP_SERVER_NAME,
        "version": Config.MCP_SERVER_VERSION,
        "port": Config.MCP_SERVER_PORT,
        "capabilities": MCPConfig.CAPABILITIES,
        "supported_languages": MCPConfig.SUPPORTED_LANGUAGES,
        "tools": list(MCPConfig.TOOLS_CONFIG.keys()),
        "status": "configured"
    }

def print_mcp_info():
    """Print MCP server information"""
    info = get_mcp_server_info()
    print(f"🩺 Puch AI Health Buddy - MCP Server Information")
    print(f"=" * 50)
    print(f"Server ID: {info['server_id']}")
    print(f"Server Name: {info['server_name']}")
    print(f"Version: {info['version']}")
    print(f"Port: {info['port']}")
    print(f"Status: {info['status']}")
    print(f"Available Tools: {len(info['tools'])}")
    print(f"Supported Languages: {len(info['supported_languages'])}")
    print(f"=" * 50)

if __name__ == "__main__":
    # When run directly, show MCP server information
    print_mcp_info()
    print(f"\nMCP Server ID: {get_mcp_server_id()}")
