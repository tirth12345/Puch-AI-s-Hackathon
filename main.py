#!/usr/bin/env python3
"""
Main application entry point for Puch AI + Health Buddy
"""

import os
from src.puch_health_buddy.core.app import create_app

# Create the app instance for Gunicorn
app = create_app()

def main():
    """Main application entry point"""
    # Get port and debug settings
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Run the application
    app.run(host='0.0.0.0', port=port, debug=debug)

if __name__ == '__main__':
    main()
