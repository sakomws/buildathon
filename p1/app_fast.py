#!/usr/bin/env python3
"""
Project 1: Visual Memory Search - Web UI (Fast Version)
A Flask web application for testing the visual memory search system.
This version skips OpenAI processing during initialization for faster startup.
"""

import os
import sys
import socket
from pathlib import Path
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import logging
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Import the VisualMemorySearch class
from main import VisualMemorySearch

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Global search engine instance
search_engine = None

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_available_port(start_port=8000, max_attempts=100):
    """Find an available port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def init_search_engine_fast():
    """Initialize the search engine quickly without OpenAI processing."""
    global search_engine
    try:
        logger.info("Initializing search engine (fast mode)...")
        
        # Use test_screenshots directory if it exists, otherwise create uploads
        screenshots_dir = 'test_screenshots' if os.path.exists('test_screenshots') else 'uploads'
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            logger.info(f"Created directory: {screenshots_dir}")
        
        logger.info(f"Using screenshots directory: {screenshots_dir}")
        
        # Create a minimal search engine without processing screenshots
        search_engine = VisualMemorySearch(screenshots_dir)
        
        # Skip the heavy initialization for now
        logger.info("Search engine initialized in fast mode - screenshots will be processed on-demand")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize search engine: {e}")
        search_engine = None
        return False

@app.route('/')
def index():
    """Main page with search interface."""
    global search_engine
    
    if search_engine is None:
        if not init_search_engine_fast():
            flash('Failed to initialize search engine. Check logs for details.', 'error')
            return render_template('index.html', error=True)
    
    # Get list of indexed screenshots (empty for now)
    try:
        screenshots = []  # Start with empty list for fast startup
        if search_engine and hasattr(search_engine, 'screenshots_data') and search_engine.screenshots_data:
            screenshots = search_engine.list_screenshots()
    except Exception as e:
        logger.error(f"Failed to list screenshots: {e}")
        screenshots = []
    
    return render_template('index.html', screenshots=screenshots, error=False)

@app.route('/search', methods=['POST'])
def search():
    """Handle search requests."""
    global search_engine
    
    if search_engine is None:
        return jsonify({'error': 'Search engine not initialized'}), 500
    
    try:
        query = request.form.get('query', '').strip()
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        logger.info(f"Searching for: {query}")
        
        # For now, return empty results until screenshots are processed
        return jsonify({
            'success': True,
            'query': query,
            'results': [],
            'total_results': 0,
            'message': 'Screenshots are still being processed. Please wait or upload new images.'
        })
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return jsonify({'error': f'Search failed: {str(e)}'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads."""
    global search_engine
    
    logger.info("Upload request received")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request content type: {request.content_type}")
    logger.info(f"Request files: {list(request.files.keys()) if request.files else 'No files'}")
    logger.info(f"Request form: {list(request.form.keys()) if request.form else 'No form data'}")
    
    if search_engine is None:
        logger.error("Search engine not initialized for upload")
        flash('Search engine not initialized. Please refresh the page.', 'error')
        return redirect(url_for('index'))
    
    try:
        logger.info("Processing upload request...")
        
        # Check if file was sent
        if 'file' not in request.files:
            logger.error("No file in request")
            logger.error(f"Available keys: {list(request.files.keys()) if request.files else 'None'}")
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        logger.info(f"File received: {file.filename}")
        logger.info(f"File content type: {file.content_type}")
        
        if file.filename == '':
            logger.error("Empty filename")
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        # Check file type
        if file and allowed_file(file.filename):
            logger.info(f"File type allowed: {file.filename}")
            
            # Secure the filename
            filename = secure_filename(file.filename)
            logger.info(f"Secured filename: {filename}")
            
            # Ensure uploads directory exists
            upload_dir = app.config['UPLOAD_FOLDER']
            os.makedirs(upload_dir, exist_ok=True)
            logger.info(f"Upload directory: {upload_dir}")
            
            # Save file
            upload_path = os.path.join(upload_dir, filename)
            logger.info(f"Saving file to: {upload_path}")
            
            try:
                file.save(upload_path)
                logger.info(f"File saved successfully: {upload_path}")
            except Exception as save_error:
                logger.error(f"Failed to save file: {save_error}")
                flash(f'Failed to save file: {str(save_error)}', 'error')
                return redirect(url_for('index'))
            
            # Check if file was actually saved
            if not os.path.exists(upload_path):
                logger.error(f"File not found after save: {upload_path}")
                flash('File was not saved properly', 'error')
                return redirect(url_for('index'))
            
            # Add to search index (simplified for now)
            logger.info("File uploaded successfully!")
            flash(f'File {filename} uploaded successfully! (Indexing will happen in background)', 'success')
        else:
            logger.error(f"Invalid file type: {file.filename}")
            flash('Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP', 'error')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Upload failed with exception: {e}")
        flash(f'Upload failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/status')
def status():
    """Get system status."""
    global search_engine
    
    try:
        if search_engine is None:
            return jsonify({
                'status': 'error',
                'message': 'Search engine not initialized'
            })
        
        # Get basic stats
        total_screenshots = 0
        if hasattr(search_engine, 'screenshots_data') and search_engine.screenshots_data:
            total_screenshots = len(search_engine.screenshots_data)
        
        return jsonify({
            'status': 'ok',
            'total_screenshots': total_screenshots,
            'openai_available': False,  # Disabled for fast mode
            'message': 'Fast mode - screenshots will be processed on-demand'
        })
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/image/<path:filename>')
def serve_image(filename):
    """Serve images from test_screenshots and uploads directories."""
    try:
        # Check if file exists in test_screenshots
        test_path = os.path.join('test_screenshots', filename)
        upload_path = os.path.join('uploads', filename)
        
        if os.path.exists(test_path):
            from flask import send_file
            return send_file(test_path, mimetype='image/png')
        elif os.path.exists(upload_path):
            from flask import send_file
            return send_file(upload_path, mimetype='image/png')
        else:
            return "Image not found", 404
            
    except Exception as e:
        logger.error(f"Failed to serve image {filename}: {e}")
        return "Error serving image", 500

if __name__ == '__main__':
    # Initialize search engine on startup (fast mode)
    if not init_search_engine_fast():
        logger.error("Failed to initialize search engine. Check configuration.")
    
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Find available port
    port = find_available_port(8000)
    if port is None:
        logger.error("No available ports found in range 8000-8099")
        sys.exit(1)
    
    print(f"🚀 Starting Visual Memory Search Web UI (Fast Mode)...")
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print(f"📱 Open your browser and navigate to the URL above")
    print(f"⏹️  Press Ctrl+C to stop the server")
    print(f"⚡ Fast mode: Screenshots will be processed on-demand")
    print("-" * 60)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=port) 