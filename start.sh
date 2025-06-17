#!/bin/bash

# Quick start script for the Document Comparison Tool
# Use this after running ./setup.sh for the first time

echo "🚀 Starting Document Comparison Tool..."

# Check if virtual environment exists
if [ ! -d "doc-env" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first to set up the tool."
    exit 1
fi

# Activate virtual environment
source doc-env/bin/activate

echo "🌐 Starting web interface at http://localhost:8501"
echo "   (Press Ctrl+C to stop)"

# Start Streamlit
streamlit run streamlit_app.py \
    --server.port 8501 \
    --server.headless false \
    --server.fileWatcherType none \
    --browser.gatherUsageStats false 