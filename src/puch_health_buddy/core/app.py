#!/usr/bin/env python3
"""
Flask Application Factory
"""

import os
import json
import logging
from flask import Flask, request, jsonify
from datetime import datetime

from .bot import WhatsAppBot, verify_signature

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """Create Flask application"""
    app = Flask(__name__)
    
    # Initialize bot
    bot = WhatsAppBot()

    @app.route('/', methods=['GET'])
    def home():
        return jsonify({
            "status": "running",
            "service": "Puch AI + Health Buddy",
            "version": "1.0.0"
        })

    @app.route('/webhook', methods=['GET'])
    def verify_webhook():
        """Verify webhook for WhatsApp Business API"""
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode and token:
            if mode == 'subscribe' and token == bot.verify_token:
                logger.info("Webhook verified successfully")
                return challenge
            else:
                logger.warning("Webhook verification failed")
                return "Verification token mismatch", 403

        return "Bad request", 400

    @app.route('/webhook', methods=['POST'])
    def handle_webhook():
        """Handle incoming WhatsApp messages"""
        try:
            # Verify webhook signature if secret is provided
            if bot.webhook_secret:
                signature = request.headers.get('X-Hub-Signature-256')
                if not verify_signature(request.data, signature, bot.webhook_secret):
                    return "Invalid signature", 401

            data = request.get_json()

            # Extract message data
            if 'entry' in data:
                for entry in data['entry']:
                    if 'changes' in entry:
                        for change in entry['changes']:
                            if change.get('field') == 'messages':
                                value = change.get('value', {})
                                if 'messages' in value:
                                    for message in value['messages']:
                                        # Extract phone number and message text
                                        phone_number = message.get('from')
                                        message_text = message.get('text', {}).get('body', '')

                                        if phone_number and message_text:
                                            logger.info(f"Received message from {phone_number}: {message_text}")

                                            # Process message and generate response
                                            response = bot.process_message(phone_number, message_text)

                                            # Send response
                                            if bot.send_message(phone_number, response):
                                                logger.info(f"Response sent to {phone_number}")
                                            else:
                                                logger.error(f"Failed to send response to {phone_number}")

            return jsonify({"status": "success"}), 200

        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        })

    return app
