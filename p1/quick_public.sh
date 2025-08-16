#!/bin/bash

echo "🚀 Visual Memory Search - Quick Public URL Generator"
echo "=================================================="

# Check if ngrok is installed
if ! command -v ngrok &> /dev/null; then
    echo "❌ ngrok not found. Installing..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install ngrok/ngrok/ngrok
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo apt-key add -
        echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
        sudo apt update && sudo apt install ngrok
    else
        echo "❌ Please install ngrok manually from: https://ngrok.com/download"
        exit 1
    fi
fi

# Find available port
PORT=8000
while ! lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    PORT=$((PORT + 1))
    if [ $PORT -gt 8100 ]; then
        echo "❌ No available ports found"
        exit 1
    fi
done

echo "🔍 Using port: $PORT"

# Start Flask app in background
echo "🚀 Starting Flask app..."
python3 app.py &
FLASK_PID=$!

# Wait for Flask to start
sleep 5

# Start ngrok tunnel
echo "🌐 Starting ngrok tunnel..."
ngrok http $PORT > /dev/null 2>&1 &
NGROK_PID=$!

# Wait for ngrok to start
sleep 3

# Get public URL
PUBLIC_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"[^"]*"' | cut -d'"' -f4)

if [ ! -z "$PUBLIC_URL" ]; then
    echo ""
    echo "🎉 SUCCESS! Your app is now publicly accessible!"
    echo "🌐 Public URL: $PUBLIC_URL"
    echo "🔐 Login: admin / password123"
    echo "📱 Local URL: http://localhost:$PORT"
    echo "🔧 ngrok Dashboard: http://localhost:4040"
    echo ""
    echo "⏹️  Press Ctrl+C to stop both services"
    
    # Wait for interrupt
    trap 'echo ""; echo "🛑 Stopping services..."; kill $FLASK_PID $NGROK_PID 2>/dev/null; echo "✅ Services stopped"; echo "👋 Goodbye!"; exit 0' INT
    
    # Keep running
    while true; do
        sleep 1
    done
else
    echo "❌ Failed to get public URL"
    kill $FLASK_PID $NGROK_PID 2>/dev/null
    exit 1
fi 