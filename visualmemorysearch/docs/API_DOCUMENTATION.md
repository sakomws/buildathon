# Visual Memory Search API Documentation

## Overview

The Visual Memory Search API is a FastAPI-based service that provides intelligent search capabilities for screenshot collections using natural language queries, visual features, and AI-powered analysis.

**Base URL:** `http://localhost:8000`  
**API Version:** 1.0.0  
**Documentation:** `http://localhost:8000/docs` (Swagger UI)

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Rate Limiting

No rate limiting is currently implemented. Use responsibly in production environments.

## Response Format

All API responses follow a consistent JSON format:

```json
{
  "status": "success|error",
  "data": {...},
  "message": "Description of the response"
}
```

## Endpoints

### 1. Health Check

#### GET `/api/health`

Check the health status of the API service.

**Response:**
```json
{
  "status": "healthy",
  "service": "Visual Memory Search API"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

### 2. Screenshot Management

#### GET `/api/screenshots`

Retrieve a list of all indexed screenshots.

**Response:**
```json
[
  {
    "filename": "screenshot.png",
    "filepath": "test_screenshots/screenshot.png",
    "timestamp": "2025-08-17T12:00:00",
    "text_content": "Extracted text from image",
    "visual_features": [0.1, 0.2, 0.3, ...],
    "metadata": {
      "file_size": 1024000,
      "dimensions": {
        "width": 1920,
        "height": 1080
      }
    }
  }
]
```

**Status Codes:**
- `200 OK` - Successfully retrieved screenshots
- `500 Internal Server Error` - Server error

---

#### POST `/api/upload`

Upload and index a new screenshot.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:** `file` (image file: PNG, JPG, JPEG, GIF, BMP)

**Response:**
```json
{
  "message": "Screenshot uploaded and indexed successfully",
  "filename": "uploaded_image.png"
}
```

**Status Codes:**
- `200 OK` - Successfully uploaded and indexed
- `400 Bad Request` - Invalid file type or no file provided
- `500 Internal Server Error` - Server error

---

#### POST `/api/upload/folder`

Upload multiple screenshots from a folder.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:** `files` (multiple image files)

**Response:**
```json
[
  {
    "message": "Screenshot uploaded and indexed successfully",
    "filename": "image1.png",
    "indexed": true
  },
  {
    "message": "Screenshot uploaded and indexed successfully",
    "filename": "image2.png",
    "indexed": true
  }
]
```

**Status Codes:**
- `200 OK` - Successfully processed all files
- `500 Internal Server Error` - Server error

---

#### GET `/api/screenshot/{filename}`

Get detailed information about a specific screenshot.

**Parameters:**
- `filename` (string) - Name of the screenshot file

**Response:**
```json
{
  "filename": "screenshot.png",
  "filepath": "test_screenshots/screenshot.png",
  "timestamp": "2025-08-17T12:00:00",
  "text_content": "Extracted text content",
  "visual_features": [0.1, 0.2, 0.3, ...],
  "metadata": {
    "file_size": 1024000,
    "dimensions": {
      "width": 1920,
      "height": 1080
    }
  }
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved screenshot info
- `404 Not Found` - Screenshot not found
- `500 Internal Server Error` - Server error

---

#### GET `/api/screenshots/{filename}`

Serve a screenshot image file.

**Parameters:**
- `filename` (string) - Name of the screenshot file

**Response:**
- **Content-Type:** Image file (PNG, JPG, JPEG, GIF, BMP)
- **Body:** Binary image data

**Status Codes:**
- `200 OK` - Successfully served image
- `404 Not Found` - Image not found
- `500 Internal Server Error` - Server error

---

#### DELETE `/api/screenshot/{filename}`

Delete a screenshot and remove it from the index.

**Parameters:**
- `filename` (string) - Name of the screenshot file

**Response:**
```json
{
  "message": "Screenshot deleted successfully"
}
```

**Status Codes:**
- `200 OK` - Successfully deleted
- `404 Not Found` - Screenshot not found
- `500 Internal Server Error` - Server error

---

### 3. Search

#### POST `/api/search`

Search screenshots using natural language queries.

**Request Body:**
```json
{
  "query": "dashboard with charts",
  "search_type": "combined",
  "max_results": 10
}
```

**Parameters:**
- `query` (string, required) - Natural language search query
- `search_type` (string, optional) - Search type: `"text"`, `"visual"`, or `"combined"` (default: `"combined"`)
- `max_results` (integer, optional) - Maximum number of results to return (default: 10)

**Response:**
```json
[
  {
    "screenshot": {
      "filename": "dashboard.png",
      "filepath": "test_screenshots/dashboard.png",
      "timestamp": "2025-08-17T12:00:00",
      "text_content": "Analytics Dashboard with Charts",
      "visual_features": [0.1, 0.2, 0.3, ...],
      "metadata": {...}
    },
    "score": 0.95,
    "match_type": "combined",
    "highlights": ["dashboard", "charts"]
  }
]
```

**Search Types:**
- **`text`** - Search only in extracted text content
- **`visual`** - Search only using visual features
- **`combined`** - Combine both text and visual search for best results

**Status Codes:**
- `200 OK` - Successfully performed search
- `500 Internal Server Error` - Server error

---

### 4. Admin Endpoints

#### GET `/api/admin/status`

Get system status and statistics.

**Response:**
```json
{
  "total_screenshots": 15,
  "index_size": 15,
  "embeddings_loaded": true,
  "models_ready": true
}
```

**Status Codes:**
- `200 OK` - Successfully retrieved status
- `500 Internal Server Error` - Server error

---

#### POST `/api/admin/rebuild-index`

Rebuild the search index from scratch.

**Response:**
```json
{
  "message": "Search index rebuilt successfully"
}
```

**Status Codes:**
- `200 OK` - Successfully rebuilt index
- `500 Internal Server Error` - Server error

**Note:** This operation may take some time depending on the number of screenshots.

---

#### POST `/api/admin/generate-test-data`

Generate test screenshot data.

**Response:**
```json
{
  "message": "Test data generation not implemented yet"
}
```

**Status Codes:**
- `200 OK` - Endpoint accessible
- `500 Internal Server Error` - Server error

---

#### POST `/api/admin/test-openai`

Test OpenAI API key validity.

**Request Body:**
```json
{
  "api_key": "your-openai-api-key-here"
}
```

**Response:**
```json
{
  "valid": true,
  "message": "OpenAI API key is valid"
}
```

**Status Codes:**
- `200 OK` - Successfully tested API key
- `400 Bad Request` - API key not provided
- `500 Internal Server Error` - Server error

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error description",
  "status_code": 400,
  "timestamp": "2025-08-17T12:00:00"
}
```

### Common Error Codes

- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

---

## Data Models

### ScreenshotInfo

```json
{
  "filename": "string",
  "filepath": "string",
  "timestamp": "datetime | null",
  "text_content": "string | null",
  "visual_features": "array[float] | null",
  "metadata": "object | null"
}
```

### SearchQuery

```json
{
  "query": "string",
  "search_type": "string",
  "max_results": "integer"
}
```

### SearchResult

```json
{
  "screenshot": "ScreenshotInfo",
  "score": "float",
  "match_type": "string",
  "highlights": "array[string] | null"
}
```

---

## Usage Examples

### Python Client Example

```python
import requests

# Base URL
base_url = "http://localhost:8000"

# Health check
response = requests.get(f"{base_url}/api/health")
print(f"Health: {response.json()}")

# Search screenshots
search_data = {
    "query": "dashboard with charts",
    "search_type": "combined",
    "max_results": 5
}
response = requests.post(f"{base_url}/api/search", json=search_data)
results = response.json()
print(f"Found {len(results)} results")

# Upload screenshot
with open("screenshot.png", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{base_url}/api/upload", files=files)
    print(f"Upload result: {response.json()}")
```

### cURL Examples

```bash
# Health check
curl http://localhost:8000/api/health

# List screenshots
curl http://localhost:8000/api/screenshots

# Search screenshots
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "dashboard", "search_type": "combined", "max_results": 5}'

# Upload screenshot
curl -X POST http://localhost:8000/api/upload \
  -F "file=@screenshot.png"

# Get admin status
curl http://localhost:8000/api/admin/status
```

---

## Performance Considerations

- **Search Performance:** Text search is fastest, visual search is slower, combined search provides best results but takes longer
- **Index Rebuilding:** Can take several minutes for large collections
- **File Uploads:** Large images may take time to process and index
- **Model Loading:** Initial startup includes loading ML models which may take time

---

## Configuration

The API can be configured using environment variables:

- `SCREENSHOT_DIR` - Directory to store screenshots (default: "test_screenshots")
- `OPENAI_API_KEY` - OpenAI API key for enhanced search
- `EMBEDDING_MODEL` - Text embedding model (default: "all-MiniLM-L6-v2")
- `VISION_MODEL` - Visual feature extraction model (default: "microsoft/git-base")
- `MAX_FILE_SIZE` - Maximum file size in bytes (default: 16MB)
- `SIMILARITY_THRESHOLD` - Search similarity threshold (default: 0.7)

---

## Testing

Run the comprehensive API test suite:

```bash
python test_api_endpoints.py
```

This will test all endpoints and generate detailed reports:
- `api_test_results.json` - Detailed test results in JSON format
- `API_TEST_REPORT.md` - Human-readable test report

---

## Support

For issues or questions:
1. Check the generated test reports
2. Review the FastAPI auto-generated documentation at `/docs`
3. Check server logs for detailed error information
4. Verify all required dependencies are installed

---

*Last Updated: 2025-08-17*
*API Version: 1.0.0*
