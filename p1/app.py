#!/usr/bin/env python3
"""
Visual Memory Search - Web UI
A Flask-based web interface for the Visual Memory Search system.
"""

import os
import sys
import json
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import time
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import after path setup
try:
    from main import VisualMemorySearch
    from generate_test_dataset import generate_all_screenshots
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required modules are available")
    sys.exit(1)

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Flask app configuration
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global search engine instance
search_engine = None

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_search_engine():
    """Initialize the search engine."""
    global search_engine
    try:
        if search_engine is None:
            logger.info("Initializing search engine...")
            search_engine = VisualMemorySearch('test_screenshots')
            logger.info("Search engine initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize search engine: {e}")
        return False

@app.route('/')
def index():
    """Main page - redirect to login if not authenticated."""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Get list of indexed screenshots
    screenshots = []
    if init_search_engine():
        try:
            screenshots = search_engine.list_screenshots()
        except Exception as e:
            logger.error(f"Failed to list screenshots: {e}")
            screenshots = []
    
    return render_template('index.html', screenshots=screenshots)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and authentication."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (you can enhance this)
        if username == 'admin' and password == 'password123':
            session['user_id'] = username
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/search', methods=['POST'])
def search():
    """Search for screenshots."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not init_search_engine():
        return jsonify({'error': 'Search engine not available'}), 500
    
    try:
        query = request.form.get('query', '').strip()
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        logger.info(f"Searching for: {query}")
        results = search_engine.search(query, top_k=5)
        
        return jsonify({
            'success': True,
            'results': results,
            'query': query,
            'count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Upload and index a single file."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not init_search_engine():
        return jsonify({'error': 'Search engine not available'}), 500
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = int(time.time())
            filename = f"{timestamp}_{filename}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            
            file.save(filepath)
            logger.info(f"File saved: {filepath}")
            
            # Add to search engine
            if search_engine.add_screenshot(filepath):
                return jsonify({
                    'success': True,
                    'message': f'File {filename} uploaded and indexed successfully',
                    'filename': filename
                })
            else:
                return jsonify({'error': 'Failed to index file'}), 500
        else:
            return jsonify({'error': 'File type not allowed'}), 400
            
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    """Upload multiple files from a folder."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not init_search_engine():
        return jsonify({'error': 'Search engine not available'}), 500
    
    try:
        files = request.files.getlist('files[]')
        if not files:
            return jsonify({'error': 'No files selected'}), 400
        
        allowed_files = [f for f in files if f.filename and allowed_file(f.filename)]
        if not allowed_files:
            return jsonify({'error': 'No valid files selected'}), 400
        
        success_count = 0
        failed_count = 0
        
        for file in allowed_files:
            try:
                filename = secure_filename(file.filename)
                timestamp = int(time.time())
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                
                file.save(filepath)
                
                if search_engine.add_screenshot(filepath):
                    success_count += 1
                else:
                    failed_count += 1
                    
            except Exception as e:
                logger.error(f"Failed to process {file.filename}: {e}")
                failed_count += 1
        
        return jsonify({
            'success': True,
            'message': f'Uploaded {success_count} files successfully, {failed_count} failed',
            'success_count': success_count,
            'failed_count': failed_count
        })
        
    except Exception as e:
        logger.error(f"Folder upload failed: {e}")
        return jsonify({'error': f'Folder upload failed: {str(e)}'}), 500

@app.route('/generate_test_data', methods=['POST'])
def generate_test_data():
    """Generate test dataset."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        logger.info("Generating test data...")
        count = generate_all_screenshots()
        
        if count > 0:
            # Rebuild index with new data
            if init_search_engine():
                search_engine._create_index()
                return jsonify({
                    'success': True,
                    'message': f'Generated {count} test screenshots and rebuilt index',
                    'count': count
                })
            else:
                return jsonify({'error': 'Failed to rebuild index'}), 500
        else:
            return jsonify({'error': 'Failed to generate test data'}), 500
            
    except Exception as e:
        logger.error(f"Test data generation failed: {e}")
        return jsonify({'error': f'Test data generation failed: {str(e)}'}), 500

@app.route('/rebuild_index', methods=['POST'])
def rebuild_index():
    """Rebuild the search index."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if not init_search_engine():
        return jsonify({'error': 'Search engine not available'}), 500
    
    try:
        logger.info("Rebuilding index...")
        
        # Delete existing index files
        if search_engine.index_file.exists():
            search_engine.index_file.unlink()
        if search_engine.embeddings_file.exists():
            search_engine.embeddings_file.unlink()
        
        # Recreate index
        search_engine._create_index()
        
        return jsonify({
            'success': True,
            'message': 'Search index rebuilt successfully'
        })
        
    except Exception as e:
        logger.error(f"Index rebuild failed: {e}")
        return jsonify({'error': f'Index rebuild failed: {str(e)}'}), 500

@app.route('/debug', methods=['GET'])
def debug_info():
    """Get debug information."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        debug_data = {
            'search_engine_available': search_engine is not None,
            'screenshot_count': len(search_engine.screenshots_data) if search_engine else 0,
            'openai_configured': search_engine.use_openai if search_engine else False,
            'upload_folder': UPLOAD_FOLDER,
            'allowed_extensions': list(ALLOWED_EXTENSIONS)
        }
        
        return jsonify(debug_data)
        
    except Exception as e:
        logger.error(f"Debug info failed: {e}")
        return jsonify({'error': f'Debug info failed: {str(e)}'}), 500

@app.route('/status')
def status():
    """Get system status."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        if not init_search_engine():
            return jsonify({
                'status': 'error',
                'message': 'Search engine not available'
            })
        
        # Get basic stats
        total_screenshots = len(search_engine.screenshots_data) if search_engine.screenshots_data else 0
        openai_available = search_engine.use_openai if search_engine else False
        
        return jsonify({
            'status': 'ok',
            'total_screenshots': total_screenshots,
            'openai_available': openai_available,
            'index_file_exists': search_engine.index_file.exists() if search_engine else False,
            'embeddings_file_exists': search_engine.embeddings_file.exists() if search_engine else False
        })
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/test_screenshots/<filename>')
def serve_test_screenshot(filename):
    """Serve test screenshot files."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        file_path = Path('test_screenshots') / filename
        if file_path.exists():
            from flask import send_file
            return send_file(file_path, mimetype='image/png')
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Failed to serve test screenshot {filename}: {e}")
        return jsonify({'error': 'Failed to serve file'}), 500

@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded files."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        file_path = Path(UPLOAD_FOLDER) / filename
        if file_path.exists():
            from flask import send_file
            return send_file(file_path, mimetype='image/png')
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Failed to serve upload {filename}: {e}")
        return jsonify({'error': 'Failed to serve file'}), 500

@app.route('/image/<filename>')
def serve_image(filename):
    """Serve images from test_screenshots and uploads directories."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    try:
        # Check if file exists in test_screenshots
        test_path = Path('test_screenshots') / filename
        upload_path = Path(UPLOAD_FOLDER) / filename
        
        if test_path.exists():
            from flask import send_file
            return send_file(test_path, mimetype='image/png')
        elif upload_path.exists():
            from flask import send_file
            return send_file(upload_path, mimetype='image/png')
        else:
            return jsonify({'error': 'Image not found'}), 404
            
    except Exception as e:
        logger.error(f"Failed to serve image {filename}: {e}")
        return jsonify({'error': 'Failed to serve image'}), 500

def find_available_port(start_port=8000):
    """Find an available port starting from start_port."""
    import socket
    port = start_port
    while port < start_port + 100:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1
    return start_port

if __name__ == '__main__':
    port = find_available_port()
    print(f"🚀 Starting Visual Memory Search Web UI on port {port}")
    print(f"📱 Open your browser and go to: http://localhost:{port}")
    print("🔐 Login with: admin / password123")
    print("⏹️  Press Ctrl+C to stop the server")
    
    try:
        app.run(host='0.0.0.0', port=port, debug=False)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!") 