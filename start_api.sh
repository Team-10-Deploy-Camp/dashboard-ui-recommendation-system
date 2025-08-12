#!/bin/bash

# Tourism Recommendation API Startup Script
# ==========================================

set -e  # Exit on any error

echo "🚀 Starting Tourism Recommendation API..."
echo "========================================"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed"
    exit 1
fi

# Install dependencies
echo "📦 Installing API dependencies..."
pip3 install -r api_requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Using default configuration."
fi

# Check if MLflow server is running (optional)
echo "🔍 Checking MLflow connectivity..."
if [ -n "$MLFLOW_TRACKING_URI" ]; then
    echo "MLflow URI configured: $MLFLOW_TRACKING_URI"
else
    echo "⚠️  MLflow URI not configured. Using local MLflow."
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Start the API server
echo "🌐 Starting FastAPI server on http://0.0.0.0:8000"
echo "📚 API Documentation available at: http://localhost:8000/docs"
echo "🔍 Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "================================"

# Start with uvicorn
python3 -m uvicorn tourism_api:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload \
    --log-level info \
    --access-log