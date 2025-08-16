#!/bin/bash

# Visual Memory Search - Quick Start Script
# Automates the setup process for Project 1

echo "🚀 Visual Memory Search - Quick Start"
echo "====================================="
echo

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "💡 Please install Python 3.8+ and try again"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed or not in PATH"
    echo "💡 Please install pip3 and try again"
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"
echo

# Create virtual environment
echo "🔧 Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "🔧 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "🔧 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo "💡 Check the error messages above"
    exit 1
fi

echo

# Check for Tesseract
echo "🔍 Checking for Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    echo "✅ Tesseract found: $(tesseract --version | head -n1)"
else
    echo "⚠️  Tesseract not found"
    echo "💡 Installing Tesseract..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install tesseract
        else
            echo "❌ Homebrew not found. Please install Homebrew first:"
            echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y tesseract-ocr
        elif command -v yum &> /dev/null; then
            sudo yum install -y tesseract
        else
            echo "❌ Package manager not supported. Please install Tesseract manually."
            exit 1
        fi
    else
        echo "❌ Operating system not supported. Please install Tesseract manually."
        exit 1
    fi
fi

echo

# Create example screenshots directory
echo "📁 Creating example directory..."
mkdir -p example_screenshots
echo "✅ Created: example_screenshots/"

# Test installation
echo "🧪 Testing installation..."
python3 test_installation.py

echo
echo "🎉 Setup complete!"
echo
echo "🚀 Next steps:"
echo "   1. Add some screenshots to the 'example_screenshots' directory"
echo "   2. Run: python3 main.py example_screenshots"
echo "   3. Or try the demo: python3 demo.py"
echo
echo "📚 For more information, see README.md"
echo
echo "🔍 Happy screenshot searching!" 