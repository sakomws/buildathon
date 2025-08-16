#!/bin/bash

# Visual Memory Search - Minimal Web UI Launcher
# This script launches the web UI with only upload functionality - instant startup

echo "⚡ Launching Visual Memory Search Web UI (Minimal Mode)..."
echo "=========================================================="

# Function to find and kill existing Python processes on ports 8000-8099
kill_existing_server() {
    echo "🔍 Checking for existing servers..."
    
    # Find Python processes using ports 8000-8099
    for port in {8000..8099}; do
        if lsof -ti:$port > /dev/null 2>&1; then
            echo "🔄 Found existing server on port $port, stopping it..."
            lsof -ti:$port | xargs kill -9 2>/dev/null
            sleep 2
        fi
    done
    
    # Also check for any Python processes running app files
    if pgrep -f "python.*app" > /dev/null; then
        echo "🔄 Found existing app process, stopping it..."
        pkill -f "python.*app"
        sleep 2
    fi
    
    echo "✅ Existing servers stopped"
}

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Kill any existing server
kill_existing_server

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

# Install only essential dependencies for minimal mode
echo "📚 Installing minimal dependencies..."
pip install flask werkzeug

# Create uploads directory
mkdir -p uploads

echo ""
echo "✅ Setup complete! Starting minimal web server..."
echo "🌐 The web UI will automatically find an available port"
echo "📱 Check the terminal output for the exact URL"
echo "⚡ Minimal mode: Upload functionality only - instant startup"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Launch the minimal web application
python app_minimal.py 