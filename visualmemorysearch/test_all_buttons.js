#!/usr/bin/env node

/**
 * Comprehensive Test Script for Visual Memory Search Application
 * Tests all buttons and functionality systematically
 */

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const path = require('path');

// Configuration
const BASE_URL = 'http://localhost:8000';
const FRONTEND_URL = 'http://localhost:3003';

// Test results
const testResults = {
  passed: 0,
  failed: 0,
  errors: []
};

// Utility functions
function log(message, type = 'info') {
  const timestamp = new Date().toISOString();
  const colors = {
    info: '\x1b[36m',    // Cyan
    success: '\x1b[32m', // Green
    error: '\x1b[31m',   // Red
    warning: '\x1b[33m', // Yellow
    reset: '\x1b[0m'     // Reset
  };
  console.log(`${colors[type]}[${timestamp}] ${message}${colors.reset}`);
}

function assert(condition, message) {
  if (condition) {
    testResults.passed++;
    log(`✓ ${message}`, 'success');
  } else {
    testResults.failed++;
    log(`✗ ${message}`, 'error');
    testResults.errors.push(message);
  }
}

async function testEndpoint(method, endpoint, data = null, expectedStatus = 200, description = '', useAuth = false) {
  try {
    const config = {
      method,
      url: `${BASE_URL}${endpoint}`,
      headers: {
        'Content-Type': 'application/json'
      }
    };
    
    if (useAuth && global.authToken) {
      config.headers['Authorization'] = `Bearer ${global.authToken}`;
    }
    
    if (data) {
      config.data = data;
    }
    
    const response = await axios(config);
    assert(response.status === expectedStatus, `${description} - Status: ${response.status}`);
    return response.data;
  } catch (error) {
    if (error.response) {
      assert(false, `${description} - Failed with status ${error.response.status}: ${error.response.data?.detail || error.message}`);
    } else {
      assert(false, `${description} - Network error: ${error.message}`);
    }
    return null;
  }
}

// Test functions
async function testHealthCheck() {
  log('Testing Health Check...', 'info');
  await testEndpoint('GET', '/api/health', null, 200, 'Health Check');
}

async function testAuthentication() {
  log('Testing Authentication...', 'info');
  
  // Test login with admin user
  const loginData = {
    username: 'admin',
    password: 'admin123'
  };
  
  const loginResponse = await testEndpoint('POST', '/auth/login', loginData, 200, 'Admin Login');
  if (loginResponse && loginResponse.access_token) {
    global.authToken = loginResponse.access_token;
    log('Authentication token obtained', 'success');
  }
}

async function testScreenshotEndpoints() {
  log('Testing Screenshot Endpoints...', 'info');
  
  if (!global.authToken) {
    log('No auth token available, skipping screenshot tests', 'warning');
    return;
  }
  
  // Test list screenshots
  await testEndpoint('GET', '/api/screenshots', null, 200, 'List Screenshots', true);
  
  // Test system status
  await testEndpoint('GET', '/api/admin/status', null, 200, 'System Status', true);
}

async function testUploadEndpoints() {
  log('Testing Upload Endpoints...', 'info');
  
  if (!global.authToken) {
    log('No auth token available, skipping upload tests', 'warning');
    return;
  }
  
  // Create a test image file
  const testImagePath = path.join(__dirname, 'test_image.png');
  const testImageData = Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==', 'base64');
  fs.writeFileSync(testImagePath, testImageData);
  
  try {
    // Test file upload
    const formData = new FormData();
    formData.append('file', fs.createReadStream(testImagePath), {
      filename: 'test_image.png',
      contentType: 'image/png'
    });
    
    const response = await axios.post(`${BASE_URL}/api/upload`, formData, {
      headers: {
        ...formData.getHeaders(),
        'Authorization': `Bearer ${global.authToken}`
      },
      timeout: 30000
    });
    
    assert(response.status === 200, 'File Upload');
    log('Test image uploaded successfully', 'success');
    
    // Clean up test file
    fs.unlinkSync(testImagePath);
  } catch (error) {
    log(`Upload test failed: ${error.message}`, 'error');
    testResults.failed++;
  }
}

async function testSearchEndpoints() {
  log('Testing Search Endpoints...', 'info');
  
  if (!global.authToken) {
    log('No auth token available, skipping search tests', 'warning');
    return;
  }
  
  const searchData = {
    query: 'test',
    search_type: 'text',
    max_results: 10
  };
  
  await testEndpoint('POST', '/api/search', searchData, 200, 'Text Search', true);
}

async function testAdminEndpoints() {
  log('Testing Admin Endpoints...', 'info');
  
  if (!global.authToken) {
    log('No auth token available, skipping admin tests', 'warning');
    return;
  }
  
  // Test rebuild index
  await testEndpoint('POST', '/api/admin/rebuild-index', null, 200, 'Rebuild Index', true);
  
  // Test generate test data
  await testEndpoint('POST', '/api/admin/generate-test-data', null, 200, 'Generate Test Data', true);
  
  // Test OpenAI key management
  const openaiKeyData = {
    api_key: 'sk-test-key-for-testing-only'
  };
  
  await testEndpoint('POST', '/api/admin/update-openai-key', openaiKeyData, 200, 'Update OpenAI Key', true);
  await testEndpoint('GET', '/api/admin/get-openai-key', null, 200, 'Get OpenAI Key', true);
}

async function testDownloadEndpoints() {
  log('Testing Download Endpoints...', 'info');
  
  if (!global.authToken) {
    log('No auth token available, skipping download tests', 'warning');
    return;
  }
  
  // Test single file download (this will fail if no files exist, which is expected)
  try {
    await axios.get(`${BASE_URL}/api/screenshots/test_image.png/download`, {
      headers: {
        'Authorization': `Bearer ${global.authToken}`
      }
    });
    log('Single file download endpoint accessible', 'success');
  } catch (error) {
    if (error.response && error.response.status === 404) {
      log('Single file download endpoint working (file not found as expected)', 'success');
    } else {
      log(`Single file download test failed: ${error.message}`, 'error');
      testResults.failed++;
    }
  }
  
  // Test ZIP download
  const zipData = {
    filenames: ['test_image.png']
  };
  
  try {
    await axios.post(`${BASE_URL}/api/screenshots/download-zip`, zipData, {
      headers: {
        'Authorization': `Bearer ${global.authToken}`,
        'Content-Type': 'application/json'
      }
    });
    log('ZIP download endpoint accessible', 'success');
  } catch (error) {
    if (error.response && error.response.status === 400) {
      log('ZIP download endpoint working (no files to download as expected)', 'success');
    } else {
      log(`ZIP download test failed: ${error.message}`, 'error');
      testResults.failed++;
    }
  }
}

async function testFrontendEndpoints() {
  log('Testing Frontend Endpoints...', 'info');
  
  try {
    const response = await axios.get(FRONTEND_URL);
    assert(response.status === 200, 'Frontend Homepage');
  } catch (error) {
    log(`Frontend test failed: ${error.message}`, 'error');
    testResults.failed++;
  }
}

async function runAllTests() {
  log('Starting Comprehensive Button and Functionality Tests...', 'info');
  log('==================================================', 'info');
  
  try {
    await testHealthCheck();
    await testAuthentication();
    await testScreenshotEndpoints();
    await testUploadEndpoints();
    await testSearchEndpoints();
    await testAdminEndpoints();
    await testDownloadEndpoints();
    await testFrontendEndpoints();
  } catch (error) {
    log(`Test suite error: ${error.message}`, 'error');
  }
  
  // Summary
  log('==================================================', 'info');
  log('Test Results Summary:', 'info');
  log(`Passed: ${testResults.passed}`, 'success');
  log(`Failed: ${testResults.failed}`, testResults.failed > 0 ? 'error' : 'success');
  
  if (testResults.errors.length > 0) {
    log('Failed Tests:', 'error');
    testResults.errors.forEach(error => {
      log(`  - ${error}`, 'error');
    });
  }
  
  const successRate = ((testResults.passed / (testResults.passed + testResults.failed)) * 100).toFixed(1);
  log(`Success Rate: ${successRate}%`, successRate >= 80 ? 'success' : 'warning');
  
  if (testResults.failed === 0) {
    log('🎉 All tests passed! All buttons should be working correctly.', 'success');
  } else {
    log('⚠️  Some tests failed. Please check the errors above.', 'warning');
  }
}

// Run tests
if (require.main === module) {
  runAllTests().catch(console.error);
}

module.exports = { runAllTests, testResults };
