#!/usr/bin/env python3
"""
Main application entry point for Puch AI + Health Buddy
"""

import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.puch_health_buddy.core.app import create_app
    
    # Create the app instance for Vercel
    app = create_app()
    
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
