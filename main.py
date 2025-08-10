#!/usr/bin/env python3
"""
Main application entry point for Puch AI + Health Buddy
"""

import os
import sys
import asyncio

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.puch_health_buddy.core.app import create_app
    from src.puch_health_buddy.mcp.simple_server import SimpleMCPServer
    from flask import request, jsonify
    from flask_cors import CORS
    
    # Create the app instance for Vercel
    app = create_app()
    CORS(app)
    
    # Initialize MCP server
    mcp_server = SimpleMCPServer()
    
    # Generate a fixed bearer token for production
    BEARER_TOKEN = "mcp_token_puch_ai_production_vercel_2025"
    
    def verify_token(token: str) -> bool:
        """Verify bearer token"""
        return token == BEARER_TOKEN
    
    def require_auth():
        """Check authentication for MCP endpoints"""
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Authorization header required"}), 401
        
        try:
            scheme, token = auth_header.split(' ', 1)
            if scheme.lower() != 'bearer':
                return jsonify({"error": "Bearer token required"}), 401
            
            if not verify_token(token):
                return jsonify({"error": "Invalid token"}), 401
                
        except ValueError:
            return jsonify({"error": "Invalid authorization format"}), 401
        
        return None
    
    # Add MCP routes
    @app.route('/mcp/info', methods=['GET'])
    def get_server_info():
        """Get MCP server information (public endpoint)"""
        info = mcp_server.get_server_info()
        return jsonify(info)
    
    @app.route('/mcp/tools', methods=['GET'])
    def get_tools():
        """Get available tools"""
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        tools = mcp_server.get_tools()
        return jsonify({"tools": tools})
    
    @app.route('/mcp/call', methods=['POST'])
    def call_tool():
        """Call a tool"""
        auth_error = require_auth()
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
                    mcp_server.call_tool(tool_name, arguments)
                )
            finally:
                loop.close()
            
            return jsonify(result)
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @app.route('/mcp/connect', methods=['POST'])
    def mcp_connect():
        """MCP connection endpoint - returns connection info"""
        return jsonify({
            "status": "connected",
            "server_id": mcp_server.server_id,
            "server_name": mcp_server.server_name,
            "version": mcp_server.server_version,
            "message": "Successfully connected to MCP server",
            "endpoints": {
                "info": "https://puch-ai-s-hackathon.vercel.app/mcp/info",
                "tools": "https://puch-ai-s-hackathon.vercel.app/mcp/tools",
                "call": "https://puch-ai-s-hackathon.vercel.app/mcp/call"
            }
        })
    
except Exception as e:
    # Fallback in case of import errors
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def error_handler():
        return jsonify({
            "error": "Application initialization failed",
            "message": str(e),
            "status": "error"
        }), 500
    
    @app.route('/health')
    def health():
        return jsonify({
            "status": "error",
            "message": "App failed to initialize properly"
        }), 500

def main():
    """Main application entry point for local development"""
    # Get port and debug settings
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=debug)

# For Vercel serverless functions, the app variable must be available at module level
if __name__ == '__main__':
    main()
