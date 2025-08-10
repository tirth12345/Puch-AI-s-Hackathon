#!/bin/bash
# Deployment script for Puch AI + Health Buddy

set -e

echo "🚀 Starting deployment of Puch AI + Health Buddy..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.template to .env and fill in your API keys"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Validate required environment variables
required_vars=("WHATSAPP_ACCESS_TOKEN" "WHATSAPP_PHONE_NUMBER_ID" "WHATSAPP_VERIFY_TOKEN")

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Error: Required environment variable $var is not set"
        exit 1
    fi
done

echo "✅ Environment variables validated"

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Run health check
echo "🔧 Running application health check..."
python -c "
import sys
sys.path.append('.')
from utils import validate_api_keys
validation = validate_api_keys()
required = ['WHATSAPP_ACCESS_TOKEN', 'WHATSAPP_PHONE_NUMBER_ID', 'WHATSAPP_VERIFY_TOKEN']
if not all(validation[key] for key in required):
    print('❌ Critical API keys missing')
    sys.exit(1)
print('✅ API validation passed')
"

# Start the application
echo "🏁 Starting Puch AI + Health Buddy..."

if [ "$1" == "docker" ]; then
    echo "🐳 Starting with Docker Compose..."
    docker-compose up --build -d
    echo "✅ Application started with Docker!"
    echo "📝 Check logs with: docker-compose logs -f"
elif [ "$1" == "production" ]; then
    echo "🌐 Starting in production mode..."
    gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app
else
    echo "🛠️ Starting in development mode..."
    python app.py
fi

echo "🎉 Deployment completed successfully!"
echo "Application running on port $PORT"
