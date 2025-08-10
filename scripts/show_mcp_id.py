#!/usr/bin/env python3
"""
Display MCP Server ID for Puch AI Health Buddy
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Import configuration
try:
    from config.settings import Config
    
    def display_mcp_info():
        """Display MCP server information"""
        print("🩺 Puch AI Health Buddy - MCP Server Information")
        print("=" * 55)
        print(f"Server ID: {Config.MCP_SERVER_ID}")
        print(f"Server Name: {Config.MCP_SERVER_NAME}")
        print(f"Version: {Config.MCP_SERVER_VERSION}")
        print(f"Port: {Config.MCP_SERVER_PORT}")
        print("=" * 55)
        print()
        print("Available MCP Tools:")
        print("  ✅ analyze_health_symptoms")
        print("  ✅ fact_check_health_claim") 
        print("  ✅ find_nearby_healthcare")
        print("  ✅ translate_health_info")
        print("  ✅ get_health_emergency_guidance")
        print()
        print("Supported Languages:")
        languages = ["en", "hi", "gu", "mr", "ta", "te", "kn", "ml", "bn", "pa", "or", "as"]
        print(f"  {', '.join(languages)}")
        print()
        print("🎯 YOUR MCP SERVER ID IS:")
        print(f"    {Config.MCP_SERVER_ID}")
        print("=" * 55)
    
    if __name__ == "__main__":
        display_mcp_info()

except ImportError as e:
    print(f"Error importing configuration: {e}")
    print("Using default values:")
    print("Server ID: puch-health-buddy-mcp")
    print("Server Name: Puch AI Health Buddy MCP Server")
    print("Version: 1.0.0")
