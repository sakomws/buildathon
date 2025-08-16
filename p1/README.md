# Project 1: Visual Memory Search 🔍

A powerful tool to search your screenshot history using natural language queries for both **text content** AND **visual elements**.

## ✨ Features

- **Dual Extraction**: Combines OCR text extraction with AI-powered visual description generation
- **Natural Language Search**: Query screenshots using everyday language like "error message about auth" or "screenshot with blue button"
- **Smart Indexing**: Automatically processes and indexes all screenshots in a directory
- **Confidence Scoring**: Returns top 5 matches with confidence scores
- **Multiple Formats**: Supports PNG, JPG, and JPEG files
- **Interactive Mode**: Command-line interface with interactive search capabilities

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
cd p1

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR (required for text extraction)
# macOS:
brew install tesseract

# Ubuntu/Debian:
sudo apt-get install tesseract-ocr

# Windows:
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
```

### 2. Basic Usage

```bash
# Point to a directory with screenshots
python main.py /path/to/screenshots

# Search for specific content
python main.py ./test_screenshots --query "error message about authentication"

# Add a new screenshot
python main.py /path/to/screenshots --add /path/to/new/screenshot.png

# List all indexed screenshots
python main.py /path/to/screenshots --list

# Rebuild the search index
python main.py /path/to/screenshots --rebuild
```

## 🎯 Usage Examples

### Search Queries

```bash
# Text-based searches
"error message about auth"
"login form"
"404 page not found"
"user profile settings"

# Visual-based searches
"screenshot with blue button"
"dark theme interface"
"mobile app layout"
"dashboard with charts"
"red error icon"
```

### Interactive Mode

Run without arguments to enter interactive mode:

```bash
python main.py /path/to/screenshots
```

Then use commands like:
- `help` - Show available commands
- `list` - List all indexed screenshots
- `add /path/to/image.png` - Add new screenshot
- `rebuild` - Rebuild search index
- `quit` - Exit the application

## 🏗️ Architecture

The system works in three main phases:

### 1. **Processing Phase**
- **OCR Extraction**: Uses Tesseract to extract text from images
- **Visual Description**: AI model generates natural language descriptions of visual elements
- **Metadata Collection**: Gathers file info, dimensions, and timestamps

### 2. **Indexing Phase**
- **Text Embedding**: Converts combined OCR + visual text to vector embeddings
- **Vector Storage**: Stores embeddings for fast similarity search
- **Metadata Storage**: Saves screenshot information in JSON format

### 3. **Search Phase**
- **Query Processing**: Converts natural language queries to embeddings
- **Similarity Calculation**: Uses cosine similarity to find best matches
- **Result Ranking**: Returns top 5 results with confidence scores

## 🔧 Configuration

### Model Selection

The system uses these pre-trained models:
- **Text Embedding**: `all-MiniLM-L6-v2` (fast, accurate semantic search)
- **Vision Description**: `Salesforce/blip-image-captioning-base` (detailed image descriptions)
- **Text Classification**: `facebook/bart-large-mnli` (query understanding)

### Performance Tuning

- **Image Resizing**: Large images are automatically resized to 512px max dimension
- **Batch Processing**: Multiple screenshots are processed efficiently
- **Memory Management**: Embeddings are stored as numpy arrays for fast access

## 📁 File Structure

```
p1/
├── main.py              # Main application
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── screenshots/        # Your screenshot directory
    ├── search_index.json    # Metadata index
    └── embeddings.npy       # Vector embeddings
```

## 🚨 Troubleshooting

### Common Issues

1. **Tesseract not found**
   ```bash
   # Install Tesseract first
   brew install tesseract  # macOS
   sudo apt-get install tesseract-ocr  # Ubuntu
   ```

2. **CUDA/GPU issues**
   ```bash
   # Use CPU-only versions
   pip install faiss-cpu torch
   ```

3. **Memory issues with large images**
   - The system automatically resizes images to 512px max
   - Check available RAM for large screenshot collections

4. **Model download issues**
   ```bash
   # Clear transformers cache
   rm -rf ~/.cache/huggingface/
   ```

### Performance Tips

- **First run**: Initial model downloads may take several minutes
- **Large collections**: Consider processing screenshots in batches
- **Storage**: Index files are stored in the screenshot directory

## 🔮 Future Enhancements

- **Web Interface**: Browser-based search interface
- **Advanced Filters**: Date ranges, file types, dimensions
- **Batch Operations**: Process multiple directories
- **Export Results**: Save search results to various formats
- **API Integration**: REST API for programmatic access

## 📝 License

This project is part of the Buildathon challenge. Feel free to modify and extend for your needs.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Happy Screenshot Searching! 🎉** 