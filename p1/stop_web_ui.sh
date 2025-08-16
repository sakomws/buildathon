#!/bin/bash

# Visual Memory Search - Web UI Stopper
# This script stops any running web UI server

echo "🛑 Stopping Visual Memory Search Web UI..."
echo "=========================================="

# Function to find and kill existing Python processes on ports 8000-8099
stop_existing_server() {
    echo "🔍 Checking for existing servers..."
    
    found_server=false
    
    # Find Python processes using ports 8000-8099
    for port in {8000..8099}; do
        if lsof -ti:$port > /dev/null 2>&1; then
            echo "🔄 Found server on port $port, stopping it..."
            lsof -ti:$port | xargs kill -9 2>/dev/null
            found_server=true
        fi
    done
    
    # Also check for any Python processes running app.py
    if pgrep -f "python.*app.py" > /dev/null; then
        echo "🔄 Found app.py process, stopping it..."
        pkill -f "python.*app.py"
        found_server=true
    fi
    
    if [ "$found_server" = true ]; then
        echo "✅ All servers stopped successfully"
    else
        echo "ℹ️  No running servers found"
    fi
}

# Stop any existing server
stop_existing_server

echo ""
echo "🎉 Done! All Visual Memory Search servers have been stopped." 