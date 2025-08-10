#!/usr/bin/env python3
"""
MCP Server Verification and Client Setup Script
"""

import json
import os
import sys
import subprocess
from pathlib import Path

def verify_mcp_setup():
    """Verify complete MCP setup"""
    print("🔍 MCP Server Verification")
    print("=" * 60)
    
    project_dir = Path.cwd()
    server_id = "puch-health-buddy-mcp"
    
    print(f"Project Directory: {project_dir}")
    print(f"Server ID: {server_id}")
    print("-" * 60)
    
    # 1. Check server files
    print("\n1. Checking Server Files:")
    files_to_check = [
        "mcp_manifest.json",
        "mcp_server_config.json", 
        "mcp_server_status.json",
        "src/puch_health_buddy/mcp/simple_server.py"
    ]
    
    all_files_exist = True
    for file_path in files_to_check:
        full_path = project_dir / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - MISSING")
            all_files_exist = False
    
    # 2. Check server configuration
    print("\n2. Checking Server Configuration:")
    manifest_file = project_dir / "mcp_manifest.json"
    if manifest_file.exists():
        try:
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
            
            actual_server_id = manifest.get('server_id')
            if actual_server_id == server_id:
                print(f"   ✅ Server ID matches: {actual_server_id}")
            else:
                print(f"   ❌ Server ID mismatch: expected '{server_id}', got '{actual_server_id}'")
            
            tools = manifest.get('tools', [])
            print(f"   ✅ Tools available: {len(tools)}")
            
        except Exception as e:
            print(f"   ❌ Error reading manifest: {e}")
    
    # 3. Test server execution
    print("\n3. Testing Server Execution:")
    try:
        cmd = [
            "C:/Users/Admin/AppData/Local/Microsoft/WindowsApps/python3.12.exe",
            "-c",
            "import sys; sys.path.insert(0, '.'); from src.puch_health_buddy.mcp.simple_server import SimpleMCPServer; server = SimpleMCPServer(); print('Server import successful')"
        ]
        
        result = subprocess.run(cmd, cwd=project_dir, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ Server can be imported and instantiated")
        else:
            print(f"   ❌ Server import failed: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Error testing server: {e}")
    
    # 4. Check Claude Desktop configuration
    print("\n4. Checking Claude Desktop Configuration:")
    claude_config_paths = [
        Path(os.environ.get('APPDATA', '')) / "Claude" / "claude_desktop_config.json",
        project_dir / "claude_desktop_config.json"
    ]
    
    for config_path in claude_config_paths:
        if config_path.exists():
            print(f"   ✅ Found config: {config_path}")
            
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
                
                mcp_servers = config.get('mcpServers', {})
                if server_id in mcp_servers:
                    print(f"   ✅ Server '{server_id}' configured in Claude Desktop")
                    server_config = mcp_servers[server_id]
                    print(f"      Command: {server_config.get('command')}")
                    print(f"      Args: {server_config.get('args')}")
                    print(f"      CWD: {server_config.get('cwd')}")
                else:
                    print(f"   ❌ Server '{server_id}' not found in Claude Desktop config")
                    
            except Exception as e:
                print(f"   ❌ Error reading Claude config: {e}")
        else:
            print(f"   ❌ Config not found: {config_path}")
    
    # 5. Provide troubleshooting steps
    print("\n5. Troubleshooting Steps:")
    print("=" * 60)
    
    if all_files_exist:
        print("✅ All server files are present")
    else:
        print("❌ Some server files are missing - run registration again")
    
    print("\n📋 Next Steps:")
    print("1. Restart Claude Desktop if it's running")
    print("2. Make sure you're in the correct working directory")
    print("3. Check that Python and dependencies are installed")
    print("4. Try starting the server manually:")
    print("   python -m src.puch_health_buddy.mcp.simple_server")
    
    print("\n🔧 Manual Server Start Commands:")
    print("   cd C:\\Users\\Admin\\Desktop\\PuchAi Hackathon")
    print("   python scripts\\mcp_server_manager.py start")
    
    print("\n📞 Testing Server Connection:")
    print("   python scripts\\mcp_server_manager.py test")
    
    print("\n" + "=" * 60)
    print("🩺 Puch AI Health Buddy MCP Server Verification Complete")
    print("=" * 60)

if __name__ == "__main__":
    verify_mcp_setup()
