# Project 1: Visual Memory Search 🖼️

A sophisticated screenshot search system that combines OCR, computer vision, and AI to enable natural language queries for visual content.

## 🚀 **Quick Start**

### **Option 1: Web UI (Recommended for Testing)**
```bash
cd p1
chmod +x run_web_ui.sh
./run_web_ui.sh
```
Then open your browser to: **http://localhost:8000**

### **Option 2: Command Line Interface**
```bash
cd p1
chmod +x quick_start.sh
./quick_start.sh
python main.py test_screenshots --query "blue button"
```

## 🌐 **Web Interface Features**

The web UI provides an intuitive way to test the Visual Memory Search system:

- **🔍 Search Interface**: Natural language query input with real-time results
- **📤 File Upload**: Drag & drop screenshot uploads with automatic indexing
- **🖼️ Test Data Generation**: One-click generation of 12 diverse screenshot types
- **📊 Results Display**: Detailed results with confidence scores, OCR text, and visual descriptions
- **⚙️ System Controls**: Index rebuilding and system status monitoring
- **📱 Responsive Design**: Works on desktop, tablet, and mobile devices

### **Web UI Screenshots**
- **Main Search**: Clean, modern interface with gradient background
- **Results View**: Detailed cards showing confidence scores, semantic tags, and metadata
- **Upload Area**: Drag & drop file upload with visual feedback
- **Control Panel**: System management and test data generation

## 🎯 **Key Features**

- **OCR Text Extraction**: Extract text from screenshots using Tesseract
- **AI-Powered Visual Analysis**: Generate detailed descriptions using OpenAI GPT-4 Vision
- **Semantic Search**: Find images using natural language queries
- **Smart Scoring**: AI-validated confidence scores with explainable results
- **Comprehensive Testing**: 12 diverse screenshot types for thorough validation

## 🛠️ **Installation**

### **Prerequisites**
- Python 3.8+
- Tesseract OCR
- OpenAI API key (optional, for enhanced features)

### **System Dependencies**
```bash
# macOS (using Homebrew)
brew install tesseract

# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# Windows
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### **Python Dependencies**
```bash
cd p1
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 📖 **Usage Examples**

### **Basic Search Queries**
```bash
# Search for UI elements
python main.py test_screenshots --query "blue button"
python main.py test_screenshots --query "login form"
python main.py test_screenshots --query "error message"

# Search for content types
python main.py test_screenshots --query "dashboard"
python main.py test_screenshots --query "e-commerce"
python main.py test_screenshots --query "social media"

# Search for visual characteristics
python main.py test_screenshots --query "dark theme"
python main.py test_screenshots --query "mobile interface"
python main.py test_screenshots --query "card layout"
```

### **Web UI Usage**
1. **Launch the web interface**: `./run_web_ui.sh`
2. **Generate test data**: Click "Generate Test Data" button
3. **Search for images**: Type queries like "blue button" or "error message"
4. **Upload new screenshots**: Drag & drop images to add them to the index
5. **View detailed results**: See confidence scores, OCR text, and AI descriptions

## 🏗️ **Architecture**

The system consists of several key components:

- **Image Processing**: OpenCV for UI element detection and color analysis
- **Text Extraction**: Tesseract OCR for extracting text content
- **AI Vision**: OpenAI GPT-4 Vision for detailed visual descriptions
- **Semantic Search**: Sentence Transformers for text embedding and similarity
- **Scoring Engine**: Multi-factor confidence scoring with AI validation
- **Web Interface**: Flask-based responsive web application

## 🔧 **Configuration**

### **Environment Variables**
Create a `.env` file in the `p1` directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_for_web_ui
```

### **OpenAI Setup**
```bash
cd p1
python setup_openai.py
```

## 🧪 **Testing**

### **Automated Testing**
```bash
**Web UI won't start**
```bash
# Check dependencies
pip install -r requirements.txt

# Check port availability
lsof -i :8000
```