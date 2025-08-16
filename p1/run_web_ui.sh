#!/bin/bash

# Visual Memory Search - Web UI Launcher
# This script sets up and launches the web interface

echo "🚀 Launching Visual Memory Search Web UI..."
echo "=============================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if test data exists
if [ ! -d "test_screenshots" ] || [ -z "$(ls -A test_screenshots 2>/dev/null)" ]; then
    echo "🖼️ No test screenshots found. Generating test dataset..."
    python generate_test_dataset.py
fi

# Create uploads directory
mkdir -p uploads

echo ""
echo "✅ Setup complete! Starting web server..."
echo "🌐 Open your browser and go to: http://localhost:8000"
echo "📱 The web UI will be available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Launch the web application
python app.py 