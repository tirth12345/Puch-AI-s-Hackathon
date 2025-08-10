#!/usr/bin/env python3
"""
MCP Server Manager for Puch AI Health Buddy
Manages the registration and startup of the MCP server
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class MCPServerManager:
    """MCP Server Manager"""
    
    def __init__(self):
        self.server_id = "puch-health-buddy-mcp"
        self.project_root = project_root
        self.config_file = self.project_root / "mcp_server_config.json"
        self.status_file = self.project_root / "mcp_server_status.json"
        
    def get_server_config(self) -> Dict[str, Any]:
        """Get server configuration"""
        return {
            "server_id": self.server_id,
            "name": "Puch AI Health Buddy MCP Server",
            "version": "1.0.0",
            "description": "AI-powered health assistant and fact-checker via MCP",
            "command": [
                "python", 
                "-m", 
                "src.puch_health_buddy.mcp.simple_server"
            ],
            "cwd": str(self.project_root),
            "env": {},
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
    
    def save_config(self):
        """Save server configuration"""
        config = self.get_server_config()
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"✅ Server configuration saved to {self.config_file}")
    
    def load_config(self) -> Optional[Dict[str, Any]]:
        """Load server configuration"""
        if not self.config_file.exists():
            return None
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return None
    
    def get_server_status(self) -> Dict[str, Any]:
        """Get current server status"""
        if not self.status_file.exists():
            return {"status": "not_found", "message": "Server status file not found"}
        
        try:
            with open(self.status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            return status
        except Exception as e:
            return {"status": "error", "message": f"Error reading status: {e}"}
    
    def register_server(self):
        """Register the MCP server"""
        print(f"📝 Registering MCP server: {self.server_id}")
        
        # Save configuration
        self.save_config()
        
        # Create manifest file
        config = self.get_server_config()
        manifest = {
            "schema_version": "0.1.0",
            "name": config["name"],
            "version": config["version"],
            "description": config["description"],
            "author": "Puch AI Team",
            "license": "MIT",
            "homepage": "https://github.com/tirth12345/Puch-AI-s-Hackathon",
            "capabilities": config["capabilities"],
            "supported_languages": config["supported_languages"],
            "tools": config["tools"],
            "server": {
                "command": config["command"],
                "args": [],
                "env": config["env"]
            },
            "server_id": self.server_id
        }
        
        manifest_file = self.project_root / "mcp_manifest.json"
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Server manifest saved to {manifest_file}")
        print(f"✅ Server {self.server_id} registered successfully")
    
    def start_server(self):
        """Start the MCP server"""
        print(f"🚀 Starting MCP server: {self.server_id}")
        
        config = self.load_config()
        if not config:
            print("❌ Server not configured. Please register first.")
            return False
        
        try:
            # Change to project directory
            os.chdir(self.project_root)
            
            # Start the server
            cmd = ["python", "-m", "src.puch_health_buddy.mcp.simple_server"]
            print(f"Running command: {' '.join(cmd)}")
            
            # Run the server in the current process for now
            result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Server started successfully")
                print("Output:", result.stdout)
                return True
            else:
                print("❌ Error starting server")
                print("Error:", result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            return False
    
    def test_server(self):
        """Test the server functionality"""
        print(f"🧪 Testing MCP server: {self.server_id}")
        
        try:
            # Import the server module to test it
            sys.path.insert(0, str(self.project_root))
            from src.puch_health_buddy.mcp.simple_server import SimpleMCPServer
            
            # Create server instance
            server = SimpleMCPServer()
            
            # Test server info
            info = server.get_server_info()
            print(f"✅ Server info retrieved: {info['name']}")
            
            # Test tools
            tools = server.get_tools()
            print(f"✅ Tools available: {len(tools)}")
            
            # Test a simple tool call
            import asyncio
            async def test_tool():
                result = await server.call_tool("analyze_health_symptoms", {
                    "symptoms": "headache and fever",
                    "language": "en"
                })
                return result
            
            result = asyncio.run(test_tool())
            if result.get("success"):
                print("✅ Tool test successful")
            else:
                print(f"❌ Tool test failed: {result.get('error')}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error testing server: {e}")
            return False
    
    def status(self):
        """Show server status"""
        print(f"📊 MCP Server Status: {self.server_id}")
        print("=" * 50)
        
        # Check configuration
        config = self.load_config()
        if config:
            print("✅ Server configuration: Found")
            print(f"   Name: {config['name']}")
            print(f"   Version: {config['version']}")
            print(f"   Tools: {len(config['tools'])}")
        else:
            print("❌ Server configuration: Not found")
        
        # Check status file
        status = self.get_server_status()
        print(f"📋 Status: {status.get('status', 'unknown')}")
        if 'message' in status:
            print(f"   Message: {status['message']}")
        if 'timestamp' in status:
            print(f"   Last updated: {status['timestamp']}")
        
        # Check manifest file
        manifest_file = self.project_root / "mcp_manifest.json"
        if manifest_file.exists():
            print("✅ Manifest file: Found")
        else:
            print("❌ Manifest file: Not found")
        
        print("=" * 50)
    
    def unregister_server(self):
        """Unregister the MCP server"""
        print(f"🗑️  Unregistering MCP server: {self.server_id}")
        
        files_to_remove = [
            self.config_file,
            self.status_file,
            self.project_root / "mcp_manifest.json"
        ]
        
        for file_path in files_to_remove:
            if file_path.exists():
                file_path.unlink()
                print(f"✅ Removed: {file_path}")
            else:
                print(f"⚠️  Not found: {file_path}")
        
        print(f"✅ Server {self.server_id} unregistered")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="MCP Server Manager for Puch AI Health Buddy")
    parser.add_argument(
        "action", 
        choices=["register", "start", "test", "status", "unregister"],
        help="Action to perform"
    )
    
    args = parser.parse_args()
    
    manager = MCPServerManager()
    
    print("🩺 Puch AI Health Buddy - MCP Server Manager")
    print("=" * 60)
    
    if args.action == "register":
        manager.register_server()
    elif args.action == "start":
        manager.start_server()
    elif args.action == "test":
        manager.test_server()
    elif args.action == "status":
        manager.status()
    elif args.action == "unregister":
        manager.unregister_server()

if __name__ == "__main__":
    main()
