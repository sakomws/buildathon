# API Test Report

**Generated:** 2025-08-17 13:46:57

## Summary

- **Total Tests:** 12
- **Successful:** 12
- **Failed:** 0
- **Success Rate:** 100.0%
- **Total Time:** 21.94 seconds

## Detailed Results

### Health

- **✅ PASS** GET /api/health
  - Description: Health check endpoint to verify service status
  - Status: 200 (Expected: 200)
  - Response Time: 0.000893s

### List Screenshots

- **✅ PASS** GET /api/screenshots
  - Description: Get list of all indexed screenshots
  - Status: 200 (Expected: 200)
  - Response Time: 0.002546s

### Search

- **✅ PASS** POST /api/search
  - Description: Search with query: test (type: combined)
  - Status: 200 (Expected: 200)
  - Response Time: 0.000618s

- **✅ PASS** POST /api/search
  - Description: Search with query: screenshot (type: text)
  - Status: 200 (Expected: 200)
  - Response Time: 0.000486s

- **✅ PASS** POST /api/search
  - Description: Search with query: image (type: visual)
  - Status: 200 (Expected: 200)
  - Response Time: 0.000518s

### Upload

- **✅ PASS** POST /api/upload
  - Description: Upload a test screenshot file
  - Status: 200 (Expected: 200)
  - Response Time: 1.219966s

### Admin

- **✅ PASS** GET /api/admin/status
  - Description: Get system status and statistics
  - Status: 200 (Expected: 200)
  - Response Time: 0.000828s

- **✅ PASS** POST /api/admin/rebuild-index
  - Description: Rebuild the search index from scratch
  - Status: 200 (Expected: 200)
  - Response Time: 19.575237s

- **✅ PASS** POST /api/admin/generate-test-data
  - Description: Generate test screenshot data
  - Status: 200 (Expected: 200)
  - Response Time: 0.000783s

- **✅ PASS** POST /api/admin/test-openai
  - Description: Test OpenAI API key validity
  - Status: 200 (Expected: 200)
  - Response Time: 0.000824s

### Management

- **✅ PASS** GET /api/screenshot/dashboard_charts.png
  - Description: Get info for screenshot: dashboard_charts.png
  - Status: 200 (Expected: 200)
  - Response Time: 0.000814s

- **✅ PASS** GET /api/screenshots/dashboard_charts.png
  - Description: Serve screenshot image: dashboard_charts.png
  - Status: 200 (Expected: 200)
  - Response Time: 0.002265s

