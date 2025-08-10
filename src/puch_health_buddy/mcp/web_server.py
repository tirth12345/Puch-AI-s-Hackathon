#!/usr/bin/env python3
"""
Web Server Wrapper for MCP Server
Enables remote connections via HTTP API with bearer token authentication
"""

import asyncio
import json
import logging
import secrets
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time

from .simple_server import SimpleMCPServer

logger = logging.getLogger(__name__)

class MCPWebServer:
    """Web server wrapper for MCP server with authentication"""
    
    def __init__(self, port: int = 8000, host: str = "localhost"):
        self.port = port
        self.host = host
        self.bearer_token = self.generate_bearer_token()
        self.mcp_server = SimpleMCPServer()
        
        # Create Flask app
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Setup routes
        self.setup_routes()
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    def generate_bearer_token(self) -> str:
        """Generate a secure bearer token"""
        return f"mcp_token_{secrets.token_urlsafe(32)}"
    
    def verify_token(self, token: str) -> bool:
        """Verify bearer token"""
        return token == self.bearer_token
    
    def require_auth(self):
        """Decorator to require authentication"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header required"}), 401
        
        try:
            scheme, token = auth_header.split(' ', 1)
            if scheme.lower() != 'bearer':
                return jsonify({"error": "Bearer token required"}), 401
            
            if not self.verify_token(token):
                return jsonify({"error": "Invalid token"}), 401
                
        except ValueError:
            return jsonify({"error": "Invalid authorization format"}), 401
        
        return None
    
    def setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint"""
            return jsonify({
                "status": "healthy",
                "server": "MCP Web Server",
                "timestamp": datetime.now().isoformat(),
                "mcp_server_id": self.mcp_server.server_id
            })
        
        @self.app.route('/mcp/info', methods=['GET'])
        def get_server_info():
            """Get MCP server information (public endpoint)"""
            info = self.mcp_server.get_server_info()
            return jsonify(info)
        
        @self.app.route('/mcp/tools', methods=['GET'])
        def get_tools():
            """Get available tools"""
            auth_error = self.require_auth()
            if auth_error:
                return auth_error
            
            tools = self.mcp_server.get_tools()
            return jsonify({"tools": tools})
        
        @self.app.route('/mcp/call', methods=['POST'])
        def call_tool():
            """Call a tool"""
            auth_error = self.require_auth()
            if auth_error:
                return auth_error
            
            try:
                data = request.get_json()
                if not data:
                    return jsonify({"error": "JSON body required"}), 400
                
                tool_name = data.get('tool')
                arguments = data.get('arguments', {})
                
                if not tool_name:
                    return jsonify({"error": "Tool name required"}), 400
                
                # Call the tool asynchronously
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    result = loop.run_until_complete(
                        self.mcp_server.call_tool(tool_name, arguments)
                    )
                finally:
                    loop.close()
                
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Error in tool call: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/mcp/connect', methods=['POST'])
        def mcp_connect():
            """MCP connection endpoint - returns connection info"""
            return jsonify({
                "status": "connected",
                "server_id": self.mcp_server.server_id,
                "server_name": self.mcp_server.server_name,
                "version": self.mcp_server.server_version,
                "message": "Successfully connected to MCP server",
                "endpoints": {
                    "info": f"http://{self.host}:{self.port}/mcp/info",
                    "tools": f"http://{self.host}:{self.port}/mcp/tools",
                    "call": f"http://{self.host}:{self.port}/mcp/call"
                }
            })
        
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Endpoint not found"}), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({"error": "Internal server error"}), 500
    
    def save_connection_info(self):
        """Save connection information to file"""
        connection_info = {
            "server_url": f"http://{self.host}:{self.port}",
            "bearer_token": self.bearer_token,
            "mcp_connect_command": f"/mcp connect http://{self.host}:{self.port} {self.bearer_token}",
            "server_info": {
                "id": self.mcp_server.server_id,
                "name": self.mcp_server.server_name,
                "version": self.mcp_server.server_version
            },
            "endpoints": {
                "health": f"http://{self.host}:{self.port}/health",
                "info": f"http://{self.host}:{self.port}/mcp/info",
                "tools": f"http://{self.host}:{self.port}/mcp/tools",
                "call": f"http://{self.host}:{self.port}/mcp/call",
                "connect": f"http://{self.host}:{self.port}/mcp/connect"
            },
            "created_at": datetime.now().isoformat()
        }
        
        with open("mcp_connection_info.json", "w") as f:
            json.dump(connection_info, f, indent=2)
        
        return connection_info
    
    def start_server(self):
        """Start the web server"""
        print("🌐 Starting MCP Web Server")
        print("=" * 60)
        print(f"Host: {self.host}")
        print(f"Port: {self.port}")
        print(f"Server ID: {self.mcp_server.server_id}")
        print(f"Bearer Token: {self.bearer_token}")
        print("-" * 60)
        
        # Save connection info
        connection_info = self.save_connection_info()
        
        print("🔗 Connection Information:")
        print(f"Server URL: {connection_info['server_url']}")
        print(f"Bearer Token: {connection_info['bearer_token']}")
        print()
        print("📋 MCP Connect Command:")
        print(f"   {connection_info['mcp_connect_command']}")
        print()
        print("🔍 Available Endpoints:")
        for name, url in connection_info['endpoints'].items():
            print(f"   {name}: {url}")
        
        print()
        print("=" * 60)
        print("🩺 Puch AI Health Buddy MCP Web Server Ready!")
        print("=" * 60)
        
        try:
            # Start Flask server
            self.app.run(
                host=self.host,
                port=self.port,
                debug=False,
                threaded=True
            )
        except Exception as e:
            print(f"❌ Error starting server: {e}")
            raise

def main():
    """Main function to start the web server"""
    import argparse
    
    parser = argparse.ArgumentParser(description="MCP Web Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run server on")
    parser.add_argument("--host", type=str, default="localhost", help="Host to bind to")
    
    args = parser.parse_args()
    
    server = MCPWebServer(port=args.port, host=args.host)
    server.start_server()

if __name__ == "__main__":
    main()
