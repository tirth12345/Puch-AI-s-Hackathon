#!/usr/bin/env python3
"""
Vercel serverless function entry point with MCP support
"""

import sys
import os
import asyncio
import secrets
from datetime import datetime

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.puch_health_buddy.core.app import create_app
    from src.puch_health_buddy.mcp.simple_server import SimpleMCPServer
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    
    # Create the Flask app
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
    
    # This is the handler that Vercel will call
    def handler(request, response):
        return app(request, response)

except Exception as e:
    # Fallback app in case of import errors
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({
            "error": "Application failed to initialize",
            "message": str(e),
            "status": "error"
        }), 500
    
    def handler(request, response):
        return app(request, response)
