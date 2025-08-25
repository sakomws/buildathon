

import React from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { BookOpen, Search, Database, Upload, Shield, Code, Zap, Settings, Users, Globe, BarChart3, FileText, Lock, Eye, Cookie, Info, HelpCircle, DollarSign } from 'lucide-react';

// Disable static generation for this page
export const dynamic = 'force-dynamic';

export default function Documentation() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Header />
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl rounded-3xl shadow-2xl p-10 border border-gray-200/50 dark:border-gray-700/50">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="flex justify-center mb-6">
              <div className="w-20 h-20 bg-gradient-to-br from-emerald-400 to-blue-500 rounded-2xl flex items-center justify-center shadow-2xl">
                <BookOpen className="h-12 w-12 text-white" />
              </div>
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-emerald-400 to-blue-400 bg-clip-text text-transparent mb-6">
              Documentation
            </h1>
            <p className="text-xl text-gray-700 dark:text-gray-300 max-w-3xl mx-auto">
              Complete guide to using Visual Memory Search - from getting started to advanced features
            </p>
          </div>

          {/* Quick Navigation */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
            <a href="#getting-started" className="group">
              <div className="p-6 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700 hover:border-blue-300 dark:hover:border-blue-600 transition-all duration-200 group-hover:shadow-md hover:shadow-lg">
                <Zap className="h-8 w-8 text-blue-600 dark:text-blue-400 mb-3" />
                <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">Getting Started</h3>
                <p className="text-blue-700 dark:text-blue-300 text-sm">Quick setup and first steps</p>
              </div>
            </a>

            <a href="#development-setup" className="group">
              <div className="p-6 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg border border-indigo-200 dark:border-indigo-700 hover:border-indigo-300 dark:hover:border-indigo-600 transition-all duration-200 group-hover:shadow-md hover:shadow-lg">
                <Code className="h-8 w-8 text-indigo-600 dark:text-indigo-400 mb-3" />
                <h3 className="text-lg font-semibold text-indigo-900 dark:text-indigo-100 mb-2">Development Setup</h3>
                <p className="text-indigo-700 dark:text-indigo-300 text-sm">Backend and frontend setup</p>
              </div>
            </a>

            <a href="#features" className="group">
              <div className="p-6 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-700 hover:border-green-300 dark:hover:border-green-600 transition-all duration-200 group-hover:shadow-md hover:shadow-lg">
                <Search className="h-8 w-8 text-green-600 dark:text-green-400 mb-3" />
                <h3 className="text-lg font-semibold text-green-900 dark:text-green-100 mb-2">Features</h3>
                <p className="text-green-700 dark:text-green-300 text-sm">Core functionality overview</p>
              </div>
            </a>

            <a href="#api" className="group">
              <div className="p-6 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-700 hover:border-purple-300 dark:hover:border-purple-600 transition-all duration-200 group-hover:shadow-md hover:shadow-lg">
                <Code className="h-8 w-8 text-purple-600 dark:text-purple-400 mb-3" />
                <h3 className="text-lg font-semibold text-purple-900 dark:text-purple-100 mb-2">API Reference</h3>
                <p className="text-purple-700 dark:text-purple-300 text-sm">Developer documentation</p>
              </div>
            </a>

            <a href="#upload" className="group">
              <div className="p-6 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-700 hover:border-orange-300 dark:hover:border-orange-600 transition-all duration-200 group-hover:shadow-md hover:shadow-lg">
                <Upload className="h-8 w-8 text-orange-600 dark:text-orange-400 mb-3" />
                <h3 className="text-lg font-semibold text-orange-900 dark:text-orange-100 mb-2">Upload Guide</h3>
                <p className="text-orange-700 dark:text-orange-300 text-sm">Managing your screenshots</p>
              </div>
            </a>

            <a href="#security" className="group">
              <div className="p-6 bg-red-50 dark:bg-red-900/20 rounded-lg border border-red-200 dark:border-red-700 hover:border-red-300 dark:hover:border-red-600 transition-all duration-200 group-hover:shadow-md hover:shadow-lg">
                <Shield className="h-8 w-8 text-red-600 dark:text-red-400 mb-3" />
                <h3 className="text-lg font-semibold text-red-900 dark:text-red-100 mb-2">Security</h3>
                <p className="text-red-700 dark:text-red-300 text-sm">Privacy and data protection</p>
              </div>
            </a>

            <a href="#troubleshooting" className="group">
              <div className="p-6 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600 hover:border-gray-300 dark:hover:border-gray-500 transition-all duration-200 group-hover:shadow-md hover:shadow-lg">
                <Settings className="h-8 w-8 text-gray-600 dark:text-gray-400 mb-3" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Troubleshooting</h3>
                <p className="text-gray-700 dark:text-gray-300 text-sm">Common issues and solutions</p>
              </div>
            </a>
          </div>

          {/* Content Sections */}
          <div className="space-y-12">
            {/* Getting Started */}
            <section id="getting-started" className="scroll-mt-20">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Zap className="h-8 w-8 mr-3 text-blue-600 dark:text-blue-400" />
                Getting Started
              </h2>
              <div className="prose prose-lg dark:prose-invert max-w-none">
                <h3>1. Account Setup</h3>
                <p>
                  To get started with Visual Memory Search, you'll need to create an account. 
                  We support multiple authentication methods:
                </p>
                <ul>
                  <li><strong>Google OAuth:</strong> Quick sign-in with your Google account</li>
                  <li><strong>GitHub OAuth:</strong> Sign in with your GitHub credentials</li>
                  <li><strong>Email/Password:</strong> Traditional account creation</li>
                </ul>

                <h3>2. First Upload</h3>
                <p>
                  After signing in, you can start uploading screenshots immediately. 
                  Supported formats include PNG, JPG, JPEG, GIF, and BMP files.
                </p>

                <h3>3. Search Your Screenshots</h3>
                <p>
                  Use natural language queries to find your screenshots. Our AI-powered 
                  search understands both text content and visual elements.
                </p>
              </div>
            </section>

            {/* Development Setup */}
            <section id="development-setup" className="scroll-mt-20">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Code className="h-8 w-8 mr-3 text-indigo-600 dark:text-indigo-400" />
                Development Setup
              </h2>
              <div className="prose prose-lg dark:prose-invert max-w-none">
                <h3>Prerequisites</h3>
                <ul>
                  <li><strong>Python:</strong> 3.11+ (3.12.2 recommended)</li>
                  <li><strong>Node.js:</strong> 18+ (for frontend)</li>
                  <li><strong>Git:</strong> For cloning the repository</li>
                  <li><strong>pyenv:</strong> For Python version management (optional but recommended)</li>
                </ul>

                <h3>Backend Setup (FastAPI)</h3>
                <p>Follow these steps to set up the backend in a virtual environment:</p>
                
                <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg my-4">
                  <h4 className="font-semibold mb-2">1. Clone and Navigate</h4>
                  <pre className="text-sm bg-gray-800 dark:bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>git clone https://github.com/sakomws/buildathon.git
cd buildathon/visualmemorysearch/backend</code></pre>
                </div>

                <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg my-4">
                  <h4 className="font-semibold mb-2">2. Create Virtual Environment</h4>
                  <pre className="text-sm bg-gray-800 dark:bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate</code></pre>
                </div>

                <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg my-4">
                  <h4 className="font-semibold mb-2">3. Install Dependencies</h4>
                  <pre className="text-sm bg-gray-800 dark:bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code># Core FastAPI dependencies
pip install fastapi uvicorn pydantic python-dotenv python-multipart

# Authentication and HTTP
pip install python-jose passlib httpx

# AI/ML and image processing
pip install opencv-python pillow pytesseract transformers sentence-transformers scikit-learn</code></pre>
                </div>

                <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg my-4">
                  <h4 className="font-semibold mb-2">4. Environment Configuration</h4>
                  <pre className="text-sm bg-gray-800 dark:bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>cp .env.example .env
# Edit .env with your OAuth credentials and API keys</code></pre>
                </div>

                <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg my-4">
                  <h4 className="font-semibold mb-2">5. Start Backend Server</h4>
                  <pre className="text-sm bg-gray-800 dark:bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>uvicorn main:app --reload --host 0.0.0.0 --port 8000</code></pre>
                </div>

                <h3>Frontend Setup (Next.js)</h3>
                <p>Set up the frontend in a separate terminal:</p>
                
                <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg my-4">
                  <h4 className="font-semibold mb-2">1. Navigate to Frontend</h4>
                  <pre className="text-sm bg-gray-800 dark:bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>cd ../frontend</code></pre>
                </div>

                <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg my-4">
                  <h4 className="font-semibold mb-2">2. Install Dependencies</h4>
                  <pre className="text-sm bg-gray-800 dark:bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>npm install</code></pre>
                </div>

                <div className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg my-4">
                  <h4 className="font-semibold mb-2">3. Start Development Server</h4>
                  <pre className="text-sm bg-gray-800 dark:bg-gray-900 text-gray-100 p-3 rounded overflow-x-auto"><code>npm run dev</code></pre>
                </div>

                <h3>Virtual Environment Benefits</h3>
                <ul>
                  <li><strong>Isolated Dependencies:</strong> No conflicts with system packages</li>
                  <li><strong>Clean Environment:</strong> Resolves Python version and dependency issues</li>
                  <li><strong>Reproducible Setup:</strong> Easy to recreate on other machines</li>
                  <li><strong>Better Management:</strong> Avoids version conflicts and package pollution</li>
                </ul>

                <h3>Common Issues & Solutions</h3>
                <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg border border-yellow-200 dark:border-yellow-700 my-4">
                  <h4 className="font-semibold text-yellow-800 dark:text-yellow-200 mb-2">Port Already in Use</h4>
                  <p className="text-yellow-700 dark:text-yellow-300 text-sm">
                    If you get "Address already in use" error, kill existing processes:
                  </p>
                  <pre className="text-sm mt-2"><code>pkill -f "uvicorn main:app"</code></pre>
                </div>

                <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg border border-yellow-200 dark:border-yellow-700 my-4">
                  <h4 className="font-semibold text-yellow-800 dark:text-yellow-200 mb-2">Python Version Issues</h4>
                  <p className="text-yellow-700 dark:text-yellow-300 text-sm">
                    Use pyenv to manage Python versions: <code>pyenv local 3.12.2</code>
                  </p>
                </div>

                <div className="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg border border-yellow-200 dark:border-yellow-700 my-4">
                  <h4 className="font-semibold text-yellow-800 dark:text-yellow-200 mb-2">Dependency Conflicts</h4>
                  <p className="text-yellow-700 dark:text-yellow-300 text-sm">
                    Always use virtual environment: <code>source venv/bin/activate</code>
                  </p>
                </div>

                <h3>Verification</h3>
                <p>After setup, verify both services are running:</p>
                <ul>
                  <li><strong>Backend:</strong> <code>http://localhost:8000/api/health</code> should return <code>&#123;"status":"healthy"&#125;</code></li>
                  <li><strong>Frontend:</strong> <code>http://localhost:3000</code> should show the login page</li>
                </ul>
              </div>
            </section>

            {/* Features */}
            <section id="features" className="scroll-mt-20">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Search className="h-8 w-8 mr-3 text-green-600" />
                Core Features
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">AI-Powered Search</h3>
                  <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                    <li>• Natural language queries</li>
                    <li>• Visual similarity search</li>
                    <li>• Text extraction (OCR)</li>
                    <li>• Combined search modes</li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Smart Organization</h3>
                  <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                    <li>• Automatic categorization</li>
                    <li>• Metadata extraction</li>
                    <li>• Tag-based filtering</li>
                    <li>• Advanced search filters</li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Enhanced Image Viewer</h3>
                  <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                    <li>• Modal-based viewing experience</li>
                    <li>• Zoom in/out functionality (50% - 300%)</li>
                    <li>• Mouse wheel and keyboard shortcuts</li>
                    <li>• Download, view, and delete actions</li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Enterprise Security</h3>
                  <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                    <li>• OAuth 2.0 authentication</li>
                    <li>• JWT token security</li>
                    <li>• Role-based access control</li>
                    <li>• Data encryption</li>
                  </ul>
                </div>

                <div className="space-y-4">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">Performance</h3>
                  <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                    <li>• Fast search indexing</li>
                    <li>• Scalable architecture</li>
                    <li>• Real-time updates</li>
                    <li>• Optimized storage</li>
                  </ul>
                </div>
              </div>
            </section>

            {/* API Reference */}
            <section id="api" className="scroll-mt-20">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Code className="h-8 w-8 mr-3 text-purple-600" />
                API Reference
              </h2>
              <div className="prose prose-lg dark:prose-invert max-w-none">
                <p>
                  Visual Memory Search provides a comprehensive REST API for developers 
                  to integrate screenshot management into their applications.
                </p>

                <h3>Authentication</h3>
                <p>
                  All API requests require authentication using Bearer tokens. 
                  Include your token in the Authorization header:
                </p>
                <pre className="bg-gray-100 dark:bg-gray-700 p-4 rounded-lg overflow-x-auto">
                  <code>Authorization: Bearer YOUR_TOKEN_HERE</code>
                </pre>

                <h3>Base URL</h3>
                <p>Production: <code>https://api.visualmemorysearch.com</code></p>
                <p>Development: <code>http://localhost:8000</code></p>

                <h3>Key Endpoints</h3>
                <ul>
                  <li><code>POST /api/upload</code> - Upload screenshots</li>
                  <li><code>GET /api/screenshots</code> - List all screenshots</li>
                  <li><code>POST /api/search</code> - Search screenshots</li>
                  <li><code>GET /api/screenshots/&#123;id&#125;</code> - Get specific screenshot</li>
                  <li><code>DELETE /api/screenshots/&#123;id&#125;</code> - Delete screenshot</li>
                </ul>

                <p>
                  For complete API documentation, visit our 
                  <a href="/api" className="text-blue-600 dark:text-blue-400 hover:underline ml-1">
                    API Reference page
                  </a>.
                </p>
              </div>
            </section>

            {/* Upload Guide */}
            <section id="upload" className="scroll-mt-20">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Upload className="h-8 w-8 mr-3 text-orange-600" />
                Upload Guide
              </h2>
              <div className="prose prose-lg dark:prose-invert max-w-none">
                <h3>Supported File Types</h3>
                <ul>
                  <li><strong>PNG:</strong> Best for screenshots with text</li>
                  <li><strong>JPG/JPEG:</strong> Good for general images</li>
                  <li><strong>GIF:</strong> Animated screenshots</li>
                  <li><strong>BMP:</strong> Uncompressed images</li>
                </ul>

                <h3>File Size Limits</h3>
                <p>Maximum file size: <strong>16 MB</strong></p>
                <p>Recommended dimensions: <strong>800x600 to 1920x1080</strong></p>

                <h3>Upload Methods</h3>
                <ul>
                  <li><strong>Drag & Drop:</strong> Simply drag files to the upload area</li>
                  <li><strong>File Browser:</strong> Click "Choose Files" to select from your device</li>
                  <li><strong>Bulk Upload:</strong> Select multiple files at once</li>
                  <li><strong>API Upload:</strong> Use our REST API for programmatic uploads</li>
                </ul>

                <h3>Processing Time</h3>
                <p>
                  After upload, screenshots are automatically processed to extract text, 
                  generate visual features, and add them to the search index. 
                  This typically takes 5-30 seconds depending on file size and complexity.
                </p>
              </div>
            </section>

            {/* Security */}
            <section id="security" className="scroll-mt-20">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Shield className="h-8 w-8 mr-3 text-red-600" />
                Security & Privacy
              </h2>
              <div className="prose prose-lg dark:prose-invert max-w-none">
                <h3>Data Protection</h3>
                <ul>
                  <li><strong>Encryption:</strong> All data is encrypted in transit and at rest</li>
                  <li><strong>Access Control:</strong> Role-based permissions and authentication</li>
                  <li><strong>Audit Logging:</strong> Complete activity tracking and monitoring</li>
                  <li><strong>Compliance:</strong> GDPR, CCPA, and SOC 2 compliant</li>
                </ul>

                <h3>Privacy Features</h3>
                <ul>
                  <li><strong>User Control:</strong> Full control over your data</li>
                  <li><strong>Data Export:</strong> Download your data anytime</li>
                  <li><strong>Account Deletion:</strong> Complete data removal on request</li>
                  <li><strong>Transparency:</strong> Clear data usage policies</li>
                </ul>

                <h3>Third-Party Services</h3>
                <p>
                  We use trusted third-party services for authentication (Google, GitHub) 
                  and analytics. All data sharing is clearly documented and user-controlled.
                </p>
              </div>
            </section>

            {/* Troubleshooting */}
            <section id="troubleshooting" className="scroll-mt-20">
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                <Settings className="h-8 w-8 mr-3 text-gray-600" />
                Troubleshooting
              </h2>
              <div className="space-y-6">
                <div className="p-6 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Upload Issues</h3>
                  <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                    <li>• Check file size (max 16MB)</li>
                    <li>• Verify file format (PNG, JPG, GIF, BMP)</li>
                    <li>• Ensure stable internet connection</li>
                    <li>• Try refreshing the page</li>
                  </ul>
                </div>

                <div className="p-6 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Search Problems</h3>
                  <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                    <li>• Wait for indexing to complete</li>
                    <li>• Try different search terms</li>
                    <li>• Check search type (text, visual, combined)</li>
                    <li>• Clear browser cache</li>
                  </ul>
                </div>

                <div className="p-6 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Authentication Errors</h3>
                  <ul className="space-y-2 text-gray-700 dark:text-gray-300">
                    <li>• Check OAuth app configuration</li>
                    <li>• Verify redirect URIs</li>
                    <li>• Clear browser cookies</li>
                    <li>• Try different browser</li>
                  </ul>
                </div>
              </div>

              <div className="mt-8 p-6 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-700">
                <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-3">Need More Help?</h3>
                <p className="text-blue-800 dark:text-blue-200 mb-4">
                  If you're still experiencing issues, our support team is here to help.
                </p>
                <a
                  href="/support"
                  className="inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                >
                  Contact Support
                  <Users className="w-4 h-4 ml-2" />
                </a>
              </div>
            </section>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
