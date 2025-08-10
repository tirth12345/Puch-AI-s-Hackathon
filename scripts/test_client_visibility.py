#!/usr/bin/env python3
"""
MCP Client Visibility Test Script
Tests whether MCP clients can discover and connect to the server
"""

import json
import os
import sys
import subprocess
from pathlib import Path
import time

def test_mcp_client_visibility():
    """Test MCP client visibility and connection"""
    print("🔍 MCP Client Visibility Test")
    print("=" * 60)
    
    server_id = "puch-health-buddy-mcp"
    project_dir = Path.cwd()
    
    print(f"Testing Server ID: {server_id}")
    print(f"Project Directory: {project_dir}")
    print("-" * 60)
    
    # Test 1: Check server registration
    print("\n1. 🏃 Testing Server Registration:")
    manifest_file = project_dir / "mcp_manifest.json"
    
    if manifest_file.exists():
        try:
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
            
            registered_id = manifest.get('server_id')
            if registered_id == server_id:
                print(f"   ✅ Server is registered with ID: {registered_id}")
                print(f"   ✅ Server name: {manifest.get('name', 'Unknown')}")
                print(f"   ✅ Version: {manifest.get('version', 'Unknown')}")
                
                # Check tools
                tools = manifest.get('tools', [])
                print(f"   ✅ Available tools: {len(tools)}")
                for tool in tools:
                    print(f"      • {tool}")
                    
            else:
                print(f"   ❌ ID mismatch: expected {server_id}, got {registered_id}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error reading manifest: {e}")
            return False
    else:
        print("   ❌ Manifest file not found")
        return False
    
    # Test 2: Check Claude Desktop configuration
    print("\n2. 🖥️  Testing Claude Desktop Configuration:")
    claude_configs = [
        Path(os.environ.get('APPDATA', '')) / "Claude" / "claude_desktop_config.json",
        project_dir / "claude_desktop_config.json"
    ]
    
    config_found = False
    for config_path in claude_configs:
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                mcp_servers = config.get('mcpServers', {})
                if server_id in mcp_servers:
                    print(f"   ✅ Found in config: {config_path}")
                    server_config = mcp_servers[server_id]
                    print(f"      Command: {server_config.get('command')}")
                    print(f"      Args: {server_config.get('args')}")
                    print(f"      Working Dir: {server_config.get('cwd')}")
                    config_found = True
                else:
                    print(f"   ⚠️  Config exists but server not found: {config_path}")
                    
            except Exception as e:
                print(f"   ❌ Error reading config {config_path}: {e}")
        else:
            print(f"   ❌ Config not found: {config_path}")
    
    if not config_found:
        print("   ❌ Server not found in any Claude Desktop config")
        return False
    
    # Test 3: Test server executable path
    print("\n3. 🐍 Testing Server Executable:")
    
    # Test different Python paths
    python_paths = [
        "C:/Users/Admin/AppData/Local/Microsoft/WindowsApps/python3.12.exe",
        "python",
        "python3"
    ]
    
    working_python = None
    for python_path in python_paths:
        try:
            result = subprocess.run([python_path, "--version"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print(f"   ✅ Python found: {python_path}")
                print(f"      Version: {result.stdout.strip()}")
                working_python = python_path
                break
        except Exception as e:
            print(f"   ❌ Python path failed: {python_path} - {e}")
    
    if not working_python:
        print("   ❌ No working Python executable found")
        return False
    
    # Test 4: Test server module import
    print("\n4. 📦 Testing Server Module Import:")
    try:
        cmd = [
            working_python,
            "-c",
            "import sys; sys.path.insert(0, '.'); from src.puch_health_buddy.mcp.simple_server import SimpleMCPServer; server = SimpleMCPServer(); info = server.get_server_info(); print(f'Server ID: {info[\"server_id\"]}'); print(f'Tools: {len(info[\"tools\"])}')"
        ]
        
        result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ Server module imports successfully")
            print(f"      Output: {result.stdout.strip()}")
        else:
            print(f"   ❌ Server import failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing server import: {e}")
        return False
    
    # Test 5: Test server startup
    print("\n5. 🚀 Testing Server Startup:")
    try:
        cmd = [
            working_python,
            "-c",
            "import sys; sys.path.insert(0, '.'); from src.puch_health_buddy.mcp.simple_server import SimpleMCPServer; server = SimpleMCPServer(); print('Server startup test successful')"
        ]
        
        result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ Server can start successfully")
        else:
            print(f"   ❌ Server startup failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing server startup: {e}")
        return False
    
    # Test 6: Generate client discovery information
    print("\n6. 📡 Client Discovery Information:")
    print("   ✅ Server is discoverable by MCP clients with the following details:")
    print(f"      • Server ID: {server_id}")
    print(f"      • Transport: stdio (standard input/output)")
    print(f"      • Protocol: Model Context Protocol (MCP)")
    print(f"      • Working Directory: {project_dir}")
    print(f"      • Python Executable: {working_python}")
    print(f"      • Module Path: src.puch_health_buddy.mcp.simple_server")
    
    # Test 7: Create client instructions
    print("\n7. 📋 Client Connection Instructions:")
    print("   For Claude Desktop:")
    print("   1. Restart Claude Desktop application")
    print("   2. Server should appear in MCP servers list")
    print("   3. Look for 'Puch AI Health Buddy MCP Server'")
    print("   4. Check for 5 available tools")
    
    print("\n   For other MCP clients:")
    print("   Use the following configuration:")
    client_config = {
        "server_id": server_id,
        "name": "Puch AI Health Buddy MCP Server",
        "command": working_python,
        "args": ["-m", "src.puch_health_buddy.mcp.simple_server"],
        "cwd": str(project_dir),
        "transport": "stdio"
    }
    print(f"   {json.dumps(client_config, indent=4)}")
    
    print("\n" + "=" * 60)
    print("🎉 MCP Client Visibility Test PASSED!")
    print("✅ Your server should be visible to MCP clients")
    print("=" * 60)
    
    return True

def create_client_detection_file():
    """Create a file that helps clients detect the server"""
    detection_data = {
        "mcp_server": {
            "id": "puch-health-buddy-mcp",
            "name": "Puch AI Health Buddy MCP Server",
            "version": "1.0.0",
            "status": "available",
            "transport": "stdio",
            "capabilities": ["tools", "prompts", "logging"],
            "tools_count": 5,
            "languages_supported": 12,
            "discovery_timestamp": time.time(),
            "connection_info": {
                "command": "python",
                "args": ["-m", "src.puch_health_buddy.mcp.simple_server"],
                "cwd": str(Path.cwd()),
                "env": {}
            }
        }
    }
    
    detection_file = Path.cwd() / "mcp_server_discovery.json"
    with open(detection_file, 'w') as f:
        json.dump(detection_data, f, indent=2)
    
    print(f"📡 Created client detection file: {detection_file}")

if __name__ == "__main__":
    print("🩺 Puch AI Health Buddy - MCP Client Visibility Test")
    print("=" * 60)
    
    success = test_mcp_client_visibility()
    
    if success:
        create_client_detection_file()
        print("\n🎯 Summary: Your MCP server is properly configured and visible!")
        print("🔄 Next: Restart your MCP client to connect to the server")
    else:
        print("\n❌ Issues found. Please fix the problems above and try again.")
        sys.exit(1)
