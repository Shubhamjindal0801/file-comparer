#!/bin/bash

# Enhanced Document Comparison Tool - Automated Setup Script
# This script sets up everything needed for the web interface

set -e  # Exit on any error

echo "🚀 Setting up Enhanced Document Comparison Tool - Web Interface..."
echo "=================================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "doc-env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv doc-env
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source doc-env/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip --quiet

# Install requirements
echo "📚 Installing dependencies..."
echo "   This may take a few minutes..."
pip install -r requirements.txt --quiet

echo ""
echo "🧹 Cleaning up cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

echo ""
echo "✅ Setup completed successfully!"
echo "=================================================================="
echo ""
echo "🌐 Starting the web interface..."
echo "📍 The app will be available at: http://localhost:8501"
echo ""
echo "🔧 Features available:"
echo "   • Upload and compare DOCX, PDF, and TXT files"
echo "   • Multiple comparison algorithms"
echo "   • Interactive visualizations and statistics"
echo "   • Export results in various formats"
echo ""
echo "⚡ Starting Streamlit server..."
echo "   (Press Ctrl+C to stop the server)"
echo ""

# Start Streamlit with optimized settings
streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.headless false \
    --server.fileWatcherType none \
    --browser.gatherUsageStats false 