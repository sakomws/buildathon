# Visual Memory Search - Complete Startup Guide

This guide will help you run both the FastAPI backend and Next.js frontend for the Visual Memory Search application.

## 🏗️ Architecture Overview

```
p1/
├── app/                    # FastAPI backend modules
│   ├── config/            # Configuration management
│   ├── models/            # Pydantic schemas
│   ├── services/          # Core ML/AI services
│   ├── templates/         # HTML templates (legacy)
│   └── utils/             # Utility functions
├── frontend/              # Next.js frontend
│   ├── src/               # Source code
│   ├── public/            # Static assets
│   └── start.sh           # Frontend startup script
├── main.py                # FastAPI application entry point
├── run_fastapi.py         # Backend startup script
└── test_fastapi.py        # Backend testing script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ with pip
- Node.js 18+ with npm
- At least 4GB RAM (for ML models)

### 1. Start the FastAPI Backend

```bash
# Navigate to the project directory
cd p1

# Install Python dependencies
pip install -r requirements.txt

# Test the backend setup
python test_fastapi.py

# Start the backend server
python run_fastapi.py
```

The backend will be available at `http://localhost:8000`

### 2. Start the Next.js Frontend

```bash
# In a new terminal, navigate to the frontend directory
cd p1/frontend

# Use the startup script (recommended)
./start.sh

# Or manually start
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🔧 Detailed Setup

### Backend Setup

1. **Environment Configuration**
   ```bash
   # Optional: Create .env file for custom settings
   cp .env.example .env
   # Edit .env with your configuration
   ```

2. **Test Backend Setup**
   ```bash
   python test_fastapi.py
   ```

3. **Start Backend Server**
   ```bash
   # Option 1: Using the run script
   python run_fastapi.py
   
   # Option 2: Using uvicorn directly
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Environment Configuration**
   ```bash
   cd frontend
   
   # Create .env.local file
   cat > .env.local << EOF
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NODE_ENV=development
   EOF
   ```

2. **Install Dependencies**
   ```bash
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

## 🌐 Accessing the Application

### Backend API
- **Main API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

### Frontend Application
- **Main Interface**: http://localhost:3000
- **API Endpoints**: http://localhost:3000/api/*

## 🧪 Testing the Setup

### 1. Backend Health Check
```bash
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Visual Memory Search API",
  "timestamp": "2024-01-01T12:00:00"
}
```

### 2. Frontend Connection
- Open http://localhost:3000 in your browser
- Check the browser console for any connection errors
- Verify that the frontend can communicate with the backend

### 3. API Endpoints Test
```bash
# List screenshots
curl http://localhost:8000/api/screenshots

# Search screenshots
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "test", "search_type": "combined", "max_results": 5}'
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8000
   lsof -ti:8000
   
   # Kill the process
   lsof -ti:8000 | xargs kill -9
   ```

2. **ML Models Not Loading**
   - Ensure you have at least 4GB RAM available
   - Check internet connection (models are downloaded on first run)
   - Verify Python dependencies are correctly installed

3. **Frontend Can't Connect to Backend**
   - Ensure backend is running on port 8000
   - Check CORS settings in backend
   - Verify .env.local configuration

4. **Image Display Issues**
   - Check that screenshot files exist in the backend directory
   - Verify Next.js API proxy configuration
   - Check browser console for CORS errors

### Debug Mode

Enable debug logging for both services:

**Backend:**
```bash
export LOG_LEVEL=DEBUG
export DEBUG=true
python run_fastapi.py
```

**Frontend:**
- Check browser console for detailed logs
- Monitor Network tab for API requests
- Verify environment variables are loaded

## 📱 Using the Application

### 1. Upload Screenshots
- Click "Upload Screenshot" button
- Select image files (PNG, JPG, JPEG, GIF, BMP)
- Wait for processing and indexing

### 2. Search Functionality
- Enter natural language queries
- Choose search type (combined, text, or visual)
- View results with relevance scores

### 3. Screenshot Management
- View all uploaded screenshots
- Click on images to open full-screen viewer
- Delete screenshots as needed

## 🚀 Production Deployment

### Backend Deployment
```bash
# Production server
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# With Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend Deployment
```bash
# Build for production
npm run build

# Start production server
npm start

# Deploy to Vercel
vercel --prod
```

## 📊 Monitoring and Logs

### Backend Logs
- Check console output for startup messages
- Monitor for ML model loading progress
- Watch for API request/response logs

### Frontend Logs
- Browser console for client-side errors
- Network tab for API communication
- React DevTools for component state

## 🔒 Security Notes

- Backend runs on localhost by default
- Frontend proxies API requests to avoid CORS issues
- File uploads are restricted to image types
- Consider HTTPS for production deployments

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **Tailwind CSS**: https://tailwindcss.com/
- **API Testing**: Use the Swagger UI at http://localhost:8000/docs

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Verify all prerequisites are met
3. Check console logs and error messages
4. Ensure both services are running
5. Test API endpoints independently

The application is designed to be modular, so you can debug each component separately.
