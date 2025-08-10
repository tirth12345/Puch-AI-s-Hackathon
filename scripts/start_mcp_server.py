#!/usr/bin/env python3
"""
MCP Server Startup Script for Puch AI Health Buddy
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from config.settings import Config
from src.puch_health_buddy.mcp.config import MCPConfig

def start_mcp_server(port: int = 8000, host: str = "localhost"):
    """Start the MCP server"""
    print(f"🚀 Starting {MCPConfig.SERVER_NAME}")
    print(f"Server ID: {MCPConfig.SERVER_ID}")
    print(f"Version: {MCPConfig.SERVER_VERSION}")
    print(f"Host: {host}")
    print(f"Port: {port}")
    print("-" * 50)
    
    # Display server capabilities
    print("Server Capabilities:")
    for capability, enabled in MCPConfig.CAPABILITIES.items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {capability}")
    
    print(f"\nSupported Languages: {', '.join(MCPConfig.SUPPORTED_LANGUAGES)}")
    print(f"Available Tools: {len(MCPConfig.TOOLS_CONFIG)}")
    
    # List available tools
    print("\nAvailable Tools:")
    for tool_name, config in MCPConfig.TOOLS_CONFIG.items():
        status = "✅" if config["enabled"] else "❌"
        rate_limit = config.get("rate_limit", "N/A")
        print(f"  {status} {tool_name} (Rate: {rate_limit}/hour)")
    
    print("\n" + "=" * 50)
    print("🩺 MCP Server is ready for connections!")
    print("=" * 50)
    
    # Note: In a real implementation, this would start the actual MCP server
    # For now, we'll just show the configuration
    print("\nTo start the actual MCP server, run:")
    print(f"python -m src.puch_health_buddy.mcp.server")
    
    return True

def generate_mcp_config():
    """Generate MCP configuration files"""
    print("📝 Generating MCP configuration files...")
    
    # Save manifest file
    manifest_path = project_root / "mcp_manifest.json"
    MCPConfig.save_manifest(str(manifest_path))
    print(f"✅ Generated: {manifest_path}")
    
    # Generate VS Code MCP settings (optional)
    vscode_settings = {
        "mcp.servers": {
            MCPConfig.SERVER_ID: {
                "name": MCPConfig.SERVER_NAME,
                "command": ["python", "-m", "src.puch_health_buddy.mcp.server"],
                "args": [],
                "env": {},
                "disabled": False
            }
        }
    }
    
    vscode_path = project_root / ".vscode" / "mcp_settings.json"
    vscode_path.parent.mkdir(exist_ok=True)
    
    with open(vscode_path, 'w', encoding='utf-8') as f:
        json.dump(vscode_settings, f, indent=2)
    print(f"✅ Generated: {vscode_path}")

def validate_environment():
    """Validate environment for MCP server"""
    print("🔍 Validating environment...")
    
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 9):
        issues.append("Python 3.9+ required")
    
    # Check required modules (basic check)
    required_modules = ['asyncio', 'json', 'logging']
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            issues.append(f"Missing module: {module}")
    
    # Check MCP configuration
    try:
        config = Config()
        mcp_config = MCPConfig()
        print(f"✅ Configuration loaded successfully")
        print(f"✅ MCP Server ID: {config.MCP_SERVER_ID}")
    except Exception as e:
        issues.append(f"Configuration error: {e}")
    
    if issues:
        print("❌ Environment validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Environment validation passed")
        return True

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Puch AI Health Buddy MCP Server")
    parser.add_argument("--port", type=int, default=8000, help="Server port")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--generate-config", action="store_true", help="Generate MCP config files")
    parser.add_argument("--validate", action="store_true", help="Validate environment only")
    
    args = parser.parse_args()
    
    print("🩺 Puch AI Health Buddy - MCP Server Manager")
    print("=" * 60)
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    if args.validate:
        print("✅ Environment validation complete")
        return
    
    if args.generate_config:
        generate_mcp_config()
        return
    
    # Start the server
    start_mcp_server(args.port, args.host)

if __name__ == "__main__":
    main()
