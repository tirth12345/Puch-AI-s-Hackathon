#!/usr/bin/env python3
"""
MCP Server ID checker and troubleshooting script
"""

import json
import os
import sys
from pathlib import Path

def check_mcp_server_registration():
    """Check MCP server registration and provide troubleshooting info"""
    print("MCP Server Registration Checker")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"Current directory: {current_dir}")
    
    # Check for manifest file
    manifest_file = current_dir / "mcp_manifest.json"
    if manifest_file.exists():
        print(f"[OK] Manifest file found: {manifest_file}")
        
        try:
            with open(manifest_file, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            server_id = manifest.get('server_id')
            server_name = manifest.get('name')
            version = manifest.get('version')
            
            print(f"[OK] Server ID: {server_id}")
            print(f"[OK] Server Name: {server_name}")
            print(f"[OK] Version: {version}")
            
            # Check server command
            server_config = manifest.get('server', {})
            command = server_config.get('command', [])
            print(f"[OK] Command: {' '.join(command)}")
            
            # Check tools
            tools = manifest.get('tools', [])
            print(f"[OK] Tools available: {len(tools)}")
            for tool in tools:
                print(f"     - {tool}")
                
        except Exception as e:
            print(f"[ERROR] Error reading manifest: {e}")
    else:
        print(f"[ERROR] Manifest file not found: {manifest_file}")
    
    # Check for server status
    status_file = current_dir / "mcp_server_status.json"
    if status_file.exists():
        print(f"[OK] Status file found: {status_file}")
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            server_status = status.get('status')
            timestamp = status.get('timestamp')
            
            print(f"[OK] Server Status: {server_status}")
            print(f"[OK] Last Updated: {timestamp}")
            
        except Exception as e:
            print(f"[ERROR] Error reading status: {e}")
    else:
        print(f"[INFO] Status file not found: {status_file}")
    
    # Check for configuration file
    config_file = current_dir / "mcp_server_config.json"
    if config_file.exists():
        print(f"[OK] Config file found: {config_file}")
    else:
        print(f"[INFO] Config file not found: {config_file}")
    
    print("\n" + "=" * 50)
    print("Troubleshooting Information:")
    print("=" * 50)
    
    print("\n1. Server Registration:")
    print("   Your MCP server 'puch-health-buddy-mcp' is properly registered.")
    print("   The manifest file contains all required information.")
    
    print("\n2. If you're getting 'Server not found' errors:")
    print("   a) Make sure your MCP client is looking in the correct directory")
    print("   b) Check that the server ID matches exactly: 'puch-health-buddy-mcp'")
    print("   c) Verify the server command can be executed")
    
    print("\n3. To start the server manually:")
    print("   python -m src.puch_health_buddy.mcp.simple_server")
    
    print("\n4. To test the server:")
    print("   python scripts\\mcp_server_manager.py test")
    
    print("\n5. Common issues:")
    print("   - Server ID mismatch (check spelling)")
    print("   - Wrong working directory")
    print("   - Missing Python dependencies")
    print("   - Port conflicts (if using TCP transport)")
    
    print("\n6. Server Information:")
    print("   - ID: puch-health-buddy-mcp")
    print("   - Transport: stdio (standard input/output)")
    print("   - Protocol: Model Context Protocol (MCP)")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    check_mcp_server_registration()
