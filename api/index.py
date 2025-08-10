#!/usr/bin/env python3
"""
Vercel serverless function entry point
"""

import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from src.puch_health_buddy.core.app import create_app
    
    # Create the Flask app
    app = create_app()
    
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
