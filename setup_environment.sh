#!/bin/bash
# Tourism Recommendation System - Environment Setup
# =================================================

echo "🚀 Setting up Tourism Recommendation System Environment..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing required packages..."
pip install -r requirements.txt

echo "✅ Environment setup complete!"
echo "🎯 To activate the environment, run: source venv/bin/activate"
echo "🚀 To run the pipeline, use: python tourism_recommendation_pipeline.py"