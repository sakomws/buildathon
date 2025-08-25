

import React from 'react';
import { Code, Database, Search, Upload, Shield, Users, Settings, Zap, BarChart3, Globe, Lock, Eye, CheckCircle, AlertTriangle, Info, HelpCircle } from 'lucide-react';

export default function APIReference() {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-8">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="flex justify-center mb-4">
              <Code className="h-16 w-16 text-purple-600 dark:text-purple-400" />
            </div>
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              API Reference
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Complete API documentation for integrating Visual Memory Search into your applications
            </p>
          </div>

          {/* Quick Navigation */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-12">
            <a href="#authentication" className="group">
              <div className="p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-700 hover:border-purple-300 dark:hover:border-purple-600 transition-all duration-200 group-hover:shadow-md text-center">
                <Code className="h-6 w-6 text-purple-600 dark:text-purple-400 mx-auto mb-2" />
                <span className="text-sm font-medium text-purple-900 dark:text-purple-100">Authentication</span>
              </div>
            </a>

            <a href="#endpoints" className="group">
              <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700 hover:border-blue-300 dark:hover:border-blue-600 transition-all duration-200 group-hover:shadow-md text-center">
                <Database className="h-6 w-6 text-blue-600 dark:text-blue-400 mx-auto mb-2" />
                <span className="text-sm font-medium text-blue-900 dark:text-blue-100">Endpoints</span>
              </div>
            </a>

            <a href="#models" className="group">
              <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700 hover:border-green-300 dark:hover:border-green-600 transition-all duration-200 group-hover:shadow-md text-center">
                <Code className="h-6 w-6 text-green-600 dark:text-green-400 mx-auto mb-2" />
                <span className="text-sm font-medium text-green-900 dark:text-green-100">Data Models</span>
              </div>
            </a>

            <a href="#examples" className="group">
              <div className="p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-700 hover:border-orange-300 dark:hover:border-orange-600 transition-all duration-200 group-hover:shadow-md text-center">
                <Zap className="h-6 w-6 text-orange-600 dark:text-orange-400 mx-auto mb-2" />
                <span className="text-sm font-medium text-orange-900 dark:text-orange-100">Examples</span>
              </div>
            </a>
          </div>

          {/* Content Sections */}
          <div className="space-y-12">
            {/* Base URL */}
            <section className="scroll-mt-20">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                <Globe className="h-6 w-6 mr-2 text-blue-600" />
                Base URL
              </h2>
              <div className="space-y-4">
                <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Production</p>
                  <code className="text-lg font-mono text-gray-900 dark:text-white">https://api.visualmemorysearch.com</code>
                </div>
                <div className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Development</p>
                  <code className="text-lg font-mono text-gray-900 dark:text-white">http://localhost:8000</code>
                </div>
              </div>
            </section>

            {/* Authentication */}
            <section id="authentication" className="scroll-mt-20">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                <Code className="h-6 w-6 mr-2 text-purple-600" />
                Authentication
              </h2>
              <div className="prose prose-lg dark:prose-invert max-w-none">
                <p>
                  All API requests require authentication using Bearer tokens. You can obtain a token 
                  by signing in through our OAuth providers or traditional authentication.
                </p>
                
                <h3>Bearer Token</h3>
                <p>Include your access token in the Authorization header:</p>
                <pre className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg overflow-x-auto">
                  <code>Authorization: Bearer YOUR_ACCESS_TOKEN</code>
                </pre>

                <h3>Token Expiration</h3>
                <p>
                  Access tokens expire after 30 minutes. Use the refresh token endpoint to obtain 
                  a new access token without requiring user re-authentication.
                </p>

                <h3>OAuth 2.0 Flow</h3>
                <p>
                  We support OAuth 2.0 with Google and GitHub providers. The flow follows the 
                  standard authorization code grant type.
                </p>
              </div>
            </section>

            {/* Endpoints */}
            <section id="endpoints" className="scroll-mt-20">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Database className="h-6 w-6 mr-2 text-blue-600" />
                API Endpoints
              </h2>
              
              <div className="space-y-6">
                {/* Upload Endpoint */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <div className="flex items-center mb-4">
                    <Upload className="h-5 w-5 text-green-600 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Upload Screenshot</h3>
                    <span className="ml-auto px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-200 text-xs font-medium rounded">POST</span>
                  </div>
                  <code className="text-sm font-mono text-gray-600 dark:text-gray-400">/api/upload</code>
                  <p className="text-gray-700 dark:text-gray-300 mt-2">
                    Upload a new screenshot file. The file will be automatically processed, indexed, and made searchable.
                  </p>
                  
                  <div className="mt-4">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-2">Request Body</h4>
                    <pre className="bg-gray-100 dark:bg-gray-700 p-3 rounded text-sm overflow-x-auto">
                      <code>FormData with 'file' field</code>
                    </pre>
                  </div>

                  <div className="mt-4">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-2">Response</h4>
                    <pre className="bg-gray-100 dark:bg-gray-700 p-3 rounded text-sm overflow-x-auto">
                      <code>{`{
  "message": "Screenshot uploaded and indexed successfully",
  "filename": "screenshot.png"
}`}</code>
                    </pre>
                  </div>
                </div>

                {/* Search Endpoint */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <div className="flex items-center mb-4">
                    <Search className="h-5 w-5 text-blue-600 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Search Screenshots</h3>
                    <span className="ml-auto px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 text-xs font-medium rounded">POST</span>
                  </div>
                  <code className="text-sm font-mono text-gray-600 dark:text-gray-400">/api/search</code>
                  <p className="text-gray-700 dark:text-gray-300 mt-2">
                    Search for screenshots using natural language queries, visual similarity, or combined search.
                  </p>
                  
                  <div className="mt-4">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-2">Request Body</h4>
                    <pre className="bg-gray-100 dark:bg-gray-700 p-3 rounded text-sm overflow-x-auto">
                      <code>{`{
  "query": "dashboard with charts",
  "search_type": "combined",
  "max_results": 10
}`}</code>
                    </pre>
                  </div>

                  <div className="mt-4">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-2">Response</h4>
                    <pre className="bg-gray-100 dark:bg-gray-700 p-3 rounded text-sm overflow-x-auto">
                      <code>{`[
  {
    "screenshot": { ... },
    "score": 0.95,
    "match_type": "combined",
    "highlights": ["dashboard", "charts"]
  }
]`}</code>
                    </pre>
                  </div>
                </div>

                {/* List Screenshots Endpoint */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <div className="flex items-center mb-4">
                    <Database className="h-5 w-5 text-purple-600 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">List Screenshots</h3>
                    <span className="ml-auto px-2 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-800 dark:text-purple-200 text-xs font-medium rounded">GET</span>
                  </div>
                  <code className="text-sm font-mono text-gray-600 dark:text-gray-400">/api/screenshots</code>
                  <p className="text-gray-700 dark:text-gray-300 mt-2">
                    Retrieve a list of all screenshots in your account with metadata and processing status.
                  </p>
                  
                  <div className="mt-4">
                    <h4 className="font-medium text-gray-900 dark:text-white mb-2">Query Parameters</h4>
                    <ul className="text-sm text-gray-700 dark:text-gray-300 space-y-1">
                      <li><code>page</code> - Page number (default: 1)</li>
                      <li><code>limit</code> - Items per page (default: 20, max: 100)</li>
                      <li><code>sort</code> - Sort order (created_at, filename, size)</li>
                    </ul>
                  </div>
                </div>

                {/* Get Screenshot Endpoint */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <div className="flex items-center mb-4">
                    <Search className="h-5 w-5 text-indigo-600 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Get Screenshot</h3>
                    <span className="ml-auto px-2 py-1 bg-indigo-100 dark:bg-indigo-900/30 text-indigo-800 dark:text-indigo-200 text-xs font-medium rounded">GET</span>
                  </div>
                  <code className="text-sm font-mono text-gray-600 dark:text-gray-400">/api/screenshots/&#123;filename&#125;</code>
                  <p className="text-gray-700 dark:text-gray-300 mt-2">
                    Retrieve detailed information about a specific screenshot including metadata, text content, and visual features.
                  </p>
                </div>

                {/* Delete Screenshot Endpoint */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <div className="flex items-center mb-4">
                    <AlertTriangle className="h-5 w-5 text-red-600 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Delete Screenshot</h3>
                    <span className="ml-auto px-2 py-1 bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-200 text-xs font-medium rounded">DELETE</span>
                  </div>
                  <code className="text-sm font-mono text-gray-600 dark:text-gray-400">/api/screenshots/&#123;filename&#125;</code>
                  <p className="text-gray-700 dark:text-gray-300 mt-2">
                    Permanently delete a screenshot and remove it from the search index.
                  </p>
                </div>

                {/* Admin Endpoints */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <div className="flex items-center mb-4">
                    <Shield className="h-5 w-5 text-yellow-600 mr-2" />
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Admin Endpoints</h3>
                    <span className="ml-auto px-2 py-1 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-200 text-xs font-medium rounded">ADMIN</span>
                  </div>
                  
                  <div className="space-y-3">
                    <div>
                      <code className="text-sm font-mono text-gray-600 dark:text-gray-400">GET /api/admin/status</code>
                      <p className="text-gray-700 dark:text-gray-300 text-sm">Get system status and statistics</p>
                    </div>
                    <div>
                      <code className="text-sm font-mono text-gray-600 dark:text-gray-400">POST /api/admin/rebuild-index</code>
                      <p className="text-gray-700 dark:text-gray-300 text-sm">Rebuild the search index from scratch</p>
                    </div>
                    <div>
                      <code className="text-sm font-mono text-gray-600 dark:text-gray-400">POST /api/admin/generate-test-data</code>
                      <p className="text-gray-700 dark:text-gray-300 text-sm">Generate sample screenshots for testing</p>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Data Models */}
            <section id="models" className="scroll-mt-20">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Code className="h-6 w-6 mr-2 text-green-600" />
                Data Models
              </h2>
              
              <div className="space-y-6">
                {/* Search Query Model */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">SearchQuery</h3>
                  <pre className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{`{
  "query": "string",           // Search query text
  "search_type": "text" | "visual" | "combined",
  "max_results": number        // Max results to return (1-100)
}`}</code>
                  </pre>
                </div>

                {/* Screenshot Info Model */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">ScreenshotInfo</h3>
                  <pre className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{`{
  "filename": "string",
  "filepath": "string",
  "text_content": "string",    // Extracted text via OCR
  "visual_features": number[], // AI-generated visual features
  "metadata": {
    "file_size": number,
    "dimensions": {
      "width": number,
      "height": number
    },
    "mime_type": "string",
    "created_at": "datetime",
    "modified_at": "datetime"
  }
}`}</code>
                  </pre>
                </div>

                {/* Search Result Model */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">SearchResult</h3>
                  <pre className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{`{
  "screenshot": ScreenshotInfo,
  "score": number,             // Relevance score (0.0-1.0)
  "base_score": number,        // Base similarity score
  "openai_score": number,      // OpenAI-enhanced score (if available)
  "match_type": "text" | "visual" | "combined",
  "highlights": string[]       // Matching terms
}`}</code>
                  </pre>
                </div>
              </div>
            </section>

            {/* Examples */}
            <section id="examples" className="scroll-mt-20">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Zap className="h-6 w-6 mr-2 text-orange-600" />
                Code Examples
              </h2>
              
              <div className="space-y-6">
                {/* JavaScript Example */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">JavaScript/Node.js</h3>
                  <pre className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{`const API_BASE = 'https://api.visualmemorysearch.com';
const TOKEN = 'your_access_token';

// Search screenshots
async function searchScreenshots(query) {
  const response = await fetch(\`\${API_BASE}/api/search\`, {
    method: 'POST',
    headers: {
      'Authorization': \`Bearer \${TOKEN}\`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      query: query,
      search_type: 'combined',
      max_results: 10
    })
  });
  
  return await response.json();
}

// Upload screenshot
async function uploadScreenshot(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch(\`\${API_BASE}/api/upload\`, {
    method: 'POST',
    headers: {
      'Authorization': \`Bearer \${TOKEN}\`
    },
    body: formData
  });
  
  return await response.json();
}`}</code>
                  </pre>
                </div>

                {/* Python Example */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Python</h3>
                  <pre className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{`import requests

API_BASE = 'https://api.visualmemorysearch.com'
TOKEN = 'your_access_token'

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# Search screenshots
def search_screenshots(query):
    response = requests.post(
        f'{API_BASE}/api/search',
        headers=headers,
        json={
            'query': query,
            'search_type': 'combined',
            'max_results': 10
        }
    )
    return response.json()

# Upload screenshot
def upload_screenshot(file_path):
    with open(file_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(
            f'{API_BASE}/api/upload',
            headers={'Authorization': f'Bearer {TOKEN}'},
            files=files
        )
    return response.json()

# List all screenshots
def list_screenshots():
    response = requests.get(
        f'{API_BASE}/api/screenshots',
        headers=headers
    )
    return response.json()`}</code>
                  </pre>
                </div>

                {/* cURL Example */}
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">cURL</h3>
                  <pre className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg overflow-x-auto text-sm">
                    <code>{`# Search screenshots
curl -X POST "https://api.visualmemorysearch.com/api/search" \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "query": "dashboard with charts",
    "search_type": "combined",
    "max_results": 10
  }'

# Upload screenshot
curl -X POST "https://api.visualmemorysearch.com/api/upload" \\
  -H "Authorization: Bearer YOUR_TOKEN" \\
  -F "file=@screenshot.png"

# List screenshots
curl -X GET "https://api.visualmemorysearch.com/api/screenshots" \\
  -H "Authorization: Bearer YOUR_TOKEN"`}</code>
                  </pre>
                </div>
              </div>
            </section>

            {/* Rate Limits & Errors */}
            <section className="scroll-mt-20">
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Shield className="h-6 w-6 mr-2 text-red-600" />
                Rate Limits & Error Handling
              </h2>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Rate Limits</h3>
                  <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                    <li>• <strong>Authenticated users:</strong> 1000 requests/hour</li>
                    <li>• <strong>File uploads:</strong> 100 files/hour</li>
                    <li>• <strong>Search queries:</strong> 5000 queries/hour</li>
                    <li>• <strong>Admin operations:</strong> 100 operations/hour</li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Common Error Codes</h3>
                  <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                    <li>• <strong>400:</strong> Bad Request - Invalid parameters</li>
                    <li>• <strong>401:</strong> Unauthorized - Invalid or expired token</li>
                    <li>• <strong>403:</strong> Forbidden - Insufficient permissions</li>
                    <li>• <strong>404:</strong> Not Found - Resource doesn't exist</li>
                    <li>• <strong>429:</strong> Too Many Requests - Rate limit exceeded</li>
                    <li>• <strong>500:</strong> Internal Server Error - Server issue</li>
                  </ul>
                </div>
              </div>
            </section>

            {/* Support */}
            <section className="scroll-mt-20">
              <div className="p-6 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700">
                <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">Need Help?</h3>
                <p className="text-blue-800 dark:text-blue-200 mb-4">
                  If you need assistance with the API or have questions about integration, 
                  our developer support team is here to help.
                </p>
                <div className="flex flex-wrap gap-3">
                  <a
                    href="/docs"
                    className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                  >
                    View Documentation
                    <Code className="w-4 h-4 ml-2" />
                  </a>
                  <a
                    href="/support"
                    className="inline-flex items-center px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors"
                  >
                    Contact Support
                    <Users className="w-4 h-4 ml-2" />
                  </a>
                </div>
              </div>
            </section>
          </div>
        </div>
      </main>
    </div>
  );
}
