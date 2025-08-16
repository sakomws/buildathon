#!/usr/bin/env python3
"""
Quick Public URL Generator for Visual Memory Search
This script helps you get a public URL for your app using ngrok or similar services.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_ngrok():
    """Check if ngrok is installed and available."""
    try:
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def install_ngrok():
    """Install ngrok if not available."""
    print("🔧 Installing ngrok...")
    
    if sys.platform == "darwin":  # macOS
        try:
            subprocess.run(['brew', 'install', 'ngrok/ngrok/ngrok'], check=True)
            print("✅ ngrok installed successfully via Homebrew")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install via Homebrew")
            return False
    elif sys.platform == "linux":  # Linux
        try:
            # Download and install ngrok
            subprocess.run(['curl', '-s', 'https://ngrok-agent.s3.amazonaws.com/ngrok.asc'], 
                         stdout=open('/tmp/ngrok.asc', 'w'), check=True)
            subprocess.run(['sudo', 'apt-key', 'add', '/tmp/ngrok.asc'], check=True)
            subprocess.run(['echo', '"deb https://ngrok-agent.s3.amazonaws.com buster main"'], 
                         stdout=open('/tmp/ngrok.list', 'w'), check=True)
            subprocess.run(['sudo', 'mv', '/tmp/ngrok.list', '/etc/apt/sources.list.d/'], check=True)
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', 'ngrok'], check=True)
            print("✅ ngrok installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install via apt")
            return False
    else:
        print("❌ Automatic installation not supported for this platform")
        print("Please install ngrok manually from: https://ngrok.com/download")
        return False

def start_ngrok(port):
    """Start ngrok tunnel on specified port."""
    try:
        print(f"🚀 Starting ngrok tunnel on port {port}...")
        
        # Start ngrok in background
        process = subprocess.Popen(
            ['ngrok', 'http', str(port), '--log=stdout'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for ngrok to start
        time.sleep(3)
        
        # Get the public URL
        try:
            response = requests.get('http://localhost:4040/api/tunnels', timeout=5)
            if response.status_code == 200:
                tunnels = response.json()['tunnels']
                if tunnels:
                    public_url = tunnels[0]['public_url']
                    print(f"✅ Public URL generated: {public_url}")
                    print(f"🔐 Login with: admin / password123")
                    print(f"⏹️  Press Ctrl+C to stop ngrok")
                    return public_url, process
        except requests.exceptions.RequestException:
            print("⚠️  Could not fetch ngrok status, but tunnel may be running")
            print("Check http://localhost:4040 for tunnel status")
            return None, process
        
    except Exception as e:
        print(f"❌ Failed to start ngrok: {e}")
        return None, None

def check_port_available(port):
    """Check if a port is available."""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=8000):
    """Find an available port starting from start_port."""
    port = start_port
    while port < start_port + 100:
        if check_port_available(port):
            return port
        port += 1
    return None

def main():
    """Main function to generate public URL."""
    print("🌐 Visual Memory Search - Public URL Generator")
    print("=" * 50)
    
    # Check if ngrok is available
    if not check_ngrok():
        print("❌ ngrok not found. Installing...")
        if not install_ngrok():
            print("\n📋 Manual Installation Required:")
            print("1. Go to https://ngrok.com/download")
            print("2. Download and install ngrok for your platform")
            print("3. Sign up for a free account")
            print("4. Run: ngrok config add-authtoken YOUR_TOKEN")
            print("5. Run this script again")
            return
        else:
            print("✅ ngrok installed successfully!")
    
    # Find available port
    port = find_available_port()
    if not port:
        print("❌ No available ports found")
        return
    
    print(f"🔍 Found available port: {port}")
    
    # Start Flask app in background
    print("🚀 Starting Flask app...")
    flask_process = subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=Path(__file__).parent,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for Flask to start
    time.sleep(5)
    
    # Start ngrok tunnel
    public_url, ngrok_process = start_ngrok(port)
    
    if public_url:
        print("\n🎉 SUCCESS! Your app is now publicly accessible!")
        print(f"🌐 Public URL: {public_url}")
        print(f"🔐 Login: admin / password123")
        print(f"📱 Local URL: http://localhost:{port}")
        print(f"🔧 ngrok Dashboard: http://localhost:4040")
        print("\n⏹️  Press Ctrl+C to stop both services")
        
        try:
            # Keep running until interrupted
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping services...")
            
            # Stop ngrok
            if ngrok_process:
                ngrok_process.terminate()
                print("✅ ngrok stopped")
            
            # Stop Flask
            if flask_process:
                flask_process.terminate()
                print("✅ Flask app stopped")
            
            print("👋 Goodbye!")
    else:
        print("❌ Failed to generate public URL")
        if flask_process:
            flask_process.terminate()
        if ngrok_process:
            ngrok_process.terminate()

if __name__ == "__main__":
    main() 