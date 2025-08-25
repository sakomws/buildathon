# Visual Memory Search - FastAPI Version

A modern, modular FastAPI application for searching screenshot history using natural language queries for both text and visual content.

## 🚀 Features

- **FastAPI Backend**: Modern, fast web framework with automatic API documentation
- **Modular Architecture**: Clean separation of concerns with dedicated modules
- **AI-Powered Search**: Combines text, visual, and AI-enhanced search capabilities
- **Real-time Processing**: Upload and index screenshots on-the-fly
- **Modern UI**: Responsive web interface with Tailwind CSS
- **RESTful API**: Full API endpoints for integration with other applications

## 🏗️ Architecture

The application follows a clean, modular architecture:

```
p1/
├── app/
│   ├── config/          # Configuration management
│   ├── models/          # Pydantic schemas and data models
│   ├── services/        # Business logic and core services
│   ├── templates/       # HTML templates
│   ├── static/          # Static assets (CSS, JS, images)
│   └── utils/           # Utility functions and helpers
├── main.py              # FastAPI application entry point
├── run_fastapi.py       # Simple run script
├── test_fastapi.py      # Test script to verify setup
└── requirements.txt     # Python dependencies
```

### Core Modules

- **`app.config.settings`**: Environment-based configuration using Pydantic
- **`app.models.schemas`**: API request/response models and data validation
- **`app.services.visual_search_service`**: Core ML/AI functionality
- **`app.utils.logger`**: Centralized logging configuration
- **`app.templates`**: Web interface templates

## 🛠️ Installation

1. **Clone and navigate to the project directory:**
   ```bash
   cd p1
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables (optional):**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Test the setup:**
   ```bash
   python test_fastapi.py
   ```

## 🚀 Running the Application

### Option 1: Using the run script
```bash
python run_fastapi.py
```

### Option 2: Using uvicorn directly
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Production deployment
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🌐 API Endpoints

The application provides the following RESTful API endpoints:

### Core Endpoints
- `GET /` - Main web interface
- `GET /api/health` - Health check
- `GET /api/screenshots` - List all indexed screenshots
- `POST /api/search` - Search screenshots
- `POST /api/upload` - Upload and index new screenshot
- `GET /api/screenshot/{filename}` - Get screenshot details
- `DELETE /api/screenshot/{filename}` - Delete screenshot

### Search API
```bash
POST /api/search
Content-Type: application/json

{
  "query": "search for text or visual content",
  "search_type": "combined",  # "text", "visual", or "combined"
  "max_results": 10
}
```

### Upload API
```bash
POST /api/upload
Content-Type: multipart/form-data

file: [screenshot file]
```

## 🔧 Configuration

Configuration is managed through environment variables and the `app/config/settings.py` file:

### Key Settings
- `SCREENSHOT_DIR`: Directory for storing screenshots (default: "test_screenshots")
- `OPENAI_API_KEY`: OpenAI API key for enhanced search (optional)
- `EMBEDDING_MODEL`: Sentence transformer model for text embeddings
- `VISION_MODEL`: Vision model for image processing
- `MAX_SEARCH_RESULTS`: Maximum number of search results (default: 10)
- `SIMILARITY_THRESHOLD`: Minimum similarity score for results (default: 0.7)

### Environment Variables
```bash
# Required
SCREENSHOT_DIR=test_screenshots

# Optional
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=all-MiniLM-L6-v2
VISION_MODEL=microsoft/git-base
DEBUG=false
LOG_LEVEL=INFO
```

## 🧠 AI/ML Features

### Text Search
- OCR text extraction using Tesseract
- Semantic search using sentence transformers
- Cosine similarity scoring

### Visual Search
- Color histogram features
- Vision model processing
- Feature vector comparison

### AI Enhancement
- OpenAI GPT integration for improved relevance
- Context-aware scoring
- Natural language understanding

## 🎨 Web Interface

The application includes a modern, responsive web interface:

- **Search Interface**: Natural language query input with search type selection
- **Results Display**: Grid layout with relevance scores and match types
- **Screenshot Management**: Upload, view, and delete screenshots
- **Responsive Design**: Works on desktop and mobile devices

## 🔍 Usage Examples

### 1. Basic Search
```bash
curl -X POST "http://localhost:8000/api/search" \
     -H "Content-Type: application/json" \
     -d '{"query": "login form", "search_type": "combined"}'
```

### 2. Upload Screenshot
```bash
curl -X POST "http://localhost:8000/api/upload" \
     -F "file=@screenshot.png"
```

### 3. List Screenshots
```bash
curl "http://localhost:8000/api/screenshots"
```

## 🧪 Testing

Run the test suite to verify your setup:

```bash
python test_fastapi.py
```

This will test:
- Module imports
- Configuration loading
- Basic functionality

## 🚀 Deployment

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker (if needed)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 📚 API Documentation

Once the application is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed and the Python path is correct
2. **Model Loading**: Check that the ML models can be downloaded (internet connection required)
3. **OpenAI API**: Verify your API key and quota if using OpenAI features
4. **File Permissions**: Ensure the screenshot directory is writable

### Debug Mode
Enable debug mode for detailed logging:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Sentence Transformers for text embeddings
- OpenAI for AI enhancement capabilities
- Tesseract for OCR functionality
