#!/usr/bin/env python3
"""
Project 1: Visual Memory Search - Web UI
A Flask web application for testing the visual memory search system.
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

def init_search_engine():
    """Initialize the search engine."""
    global search_engine
    try:
        logger.info("Initializing search engine...")
        
        # Use test_screenshots directory if it exists, otherwise create uploads
        screenshots_dir = 'test_screenshots' if os.path.exists('test_screenshots') else 'uploads'
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
            logger.info(f"Created directory: {screenshots_dir}")
        
        logger.info(f"Using screenshots directory: {screenshots_dir}")
        
        # Initialize the search engine
        search_engine = VisualMemorySearch(screenshots_dir)
        logger.info(f"Search engine initialized successfully with directory: {screenshots_dir}")
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
        if not init_search_engine():
            flash('Failed to initialize search engine. Check logs for details.', 'error')
            return render_template('index.html', error=True)
    
    # Get list of indexed screenshots
    try:
        screenshots = search_engine.list_screenshots() if search_engine else []
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
        
        # Perform search
        results = search_engine.search(query, top_k=10)
        
        # Format results for display
        formatted_results = []
        for result in results:
            formatted_result = {
                'filename': result['filename'],
                'confidence_score': round(result['confidence_score'], 3),
                'final_score': round(result.get('final_score', result['confidence_score']), 3),
                'openai_score': round(result.get('openai_score', 0), 3) if result.get('openai_score') else None,
                'ocr_text': result['ocr_text'][:100] + '...' if len(result['ocr_text']) > 100 else result['ocr_text'],
                'visual_description': result['visual_description'][:150] + '...' if len(result['visual_description']) > 150 else result['visual_description'],
                'dimensions': result['dimensions'],
                'semantic_tags': result.get('semantic_tags', []),
                'ui_patterns': result.get('ui_patterns', []),
                'content_types': result.get('content_types', [])
            }
            formatted_results.append(formatted_result)
        
        return jsonify({
            'success': True,
            'query': query,
            'results': formatted_results,
            'total_results': len(formatted_results)
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
        logger.info(f"File size: {file.content_length if hasattr(file, 'content_length') else 'Unknown'}")
        
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
            
            # Add to search index
            logger.info("Adding file to search index...")
            try:
                if search_engine.add_screenshot(upload_path):
                    logger.info(f"File {filename} uploaded and indexed successfully!")
                    flash(f'File {filename} uploaded and indexed successfully!', 'success')
                else:
                    logger.error(f"Failed to index file {filename}")
                    flash(f'Failed to index file {filename}', 'error')
            except Exception as index_error:
                logger.error(f"Indexing failed: {index_error}")
                flash(f'File uploaded but indexing failed: {str(index_error)}', 'warning')
        else:
            logger.error(f"Invalid file type: {file.filename}")
            flash('Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP', 'error')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Upload failed with exception: {e}")
        flash(f'Upload failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/upload_folder', methods=['POST'])
def upload_folder():
    """Handle folder upload with multiple images."""
    try:
        if 'files[]' not in request.files:
            flash('No folder selected', 'error')
            return redirect(request.url)
        
        files = request.files.getlist('files[]')
        
        if not files or files[0].filename == '':
            flash('No files in folder', 'error')
            return redirect(request.url)
        
        # Filter for image files
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp'}
        image_files = []
        
        for file in files:
            if file and file.filename:
                # Get file extension
                file_ext = os.path.splitext(file.filename)[1].lower()
                if file_ext in image_extensions:
                    image_files.append(file)
        
        if not image_files:
            flash('No image files found in folder', 'error')
            return redirect(request.url)
        
        logger.info(f"Processing {len(image_files)} images from folder upload")
        
        # Process each image
        success_count = 0
        failed_count = 0
        
        for file in image_files:
            try:
                if file and allowed_file(file.filename):
                    # Save file
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    # Add to search engine
                    if search_engine.add_screenshot(file_path):
                        success_count += 1
                        logger.info(f"Successfully processed folder image: {filename}")
                    else:
                        failed_count += 1
                        logger.warning(f"Failed to process folder image: {filename}")
                else:
                    failed_count += 1
                    logger.warning(f"Invalid file in folder: {file.filename}")
            except Exception as e:
                failed_count += 1
                logger.error(f"Error processing folder image {file.filename}: {e}")
        
        # Flash results
        if success_count > 0:
            flash(f'Successfully uploaded and indexed {success_count} images from folder', 'success')
        if failed_count > 0:
            flash(f'Failed to process {failed_count} images from folder', 'warning')
        
        logger.info(f"Folder upload completed: {success_count} success, {failed_count} failed")
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Folder upload error: {e}")
        flash(f'Folder upload failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/rebuild', methods=['POST'])
def rebuild_index():
    """Rebuild the search index."""
    global search_engine
    
    try:
        logger.info("Starting index rebuild...")
        
        if search_engine is None:
            flash('Search engine not initialized. Please refresh the page.', 'error')
            return redirect(url_for('index'))
        
        # Delete existing index files
        try:
            if search_engine.index_file.exists():
                search_engine.index_file.unlink()
                logger.info("Deleted old index file")
            if search_engine.embeddings_file.exists():
                search_engine.embeddings_file.unlink()
                logger.info("Deleted old embeddings file")
        except Exception as e:
            logger.error(f"Failed to delete old index files: {e}")
            flash('Failed to delete old index files', 'error')
            return redirect(url_for('index'))
        
        # Recreate index
        try:
            logger.info("Recreating search index...")
            search_engine._create_index()
            logger.info("Index rebuilt successfully")
            flash('Search index rebuilt successfully!', 'success')
        except Exception as e:
            logger.error(f"Failed to recreate index: {e}")
            flash(f'Failed to rebuild index: {str(e)}', 'error')
            return redirect(url_for('index'))
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Index rebuild failed: {e}")
        flash(f'Index rebuild failed: {str(e)}', 'error')
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
        })

@app.route('/debug')
def debug_info():
    """Debug information for troubleshooting."""
    try:
        debug_data = {
            'search_engine_initialized': search_engine is not None,
            'current_directory': os.getcwd(),
            'test_screenshots_exists': os.path.exists('test_screenshots'),
            'uploads_exists': os.path.exists('uploads'),
            'generate_test_dataset_exists': os.path.exists('generate_test_dataset.py'),
            'main_py_exists': os.path.exists('main.py'),
            'python_path': sys.path[:5],  # First 5 entries
            'environment_vars': {
                'OPENAI_API_KEY': 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET',
                'SECRET_KEY': 'SET' if os.getenv('SECRET_KEY') else 'NOT SET'
            }
        }
        
        if search_engine:
            debug_data.update({
                'screenshots_count': len(search_engine.screenshots_data) if search_engine.screenshots_data else 0,
                'index_file_exists': search_engine.index_file.exists() if search_engine.index_file else False,
                'embeddings_file_exists': search_engine.embeddings_file.exists() if search_engine.embeddings_file else False,
                'use_openai': search_engine.use_openai
            })
        
        return jsonify(debug_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@app.route('/generate_test_data', methods=['POST'])
def generate_test_data():
    """Generate test dataset."""
    try:
        logger.info("Starting test data generation...")
        
        # Check if search engine is available
        if search_engine is None:
            flash('Search engine not initialized. Please refresh the page.', 'error')
            return redirect(url_for('index'))
        
        # Import the function
        try:
            from generate_test_dataset import generate_all_screenshots
            logger.info("Successfully imported generate_all_screenshots function")
        except ImportError as e:
            logger.error(f"Import error: {e}")
            flash('Failed to import test data generator. Check the logs.', 'error')
            return redirect(url_for('index'))
        
        # Generate test screenshots
        logger.info("Calling generate_all_screenshots...")
        success_count = generate_all_screenshots()
        logger.info(f"Generated {success_count} screenshots")
        
        if success_count > 0:
            # Rebuild index with new data
            try:
                if search_engine.index_file.exists():
                    search_engine.index_file.unlink()
                    logger.info("Deleted old index file")
                if search_engine.embeddings_file.exists():
                    search_engine.embeddings_file.unlink()
                    logger.info("Deleted old embeddings file")
                
                logger.info("Rebuilding search index...")
                search_engine._create_index()
                logger.info("Index rebuilt successfully")
                
                flash(f'Generated {success_count} test screenshots and rebuilt index!', 'success')
            except Exception as e:
                logger.error(f"Index rebuild failed: {e}")
                flash(f'Generated {success_count} screenshots but failed to rebuild index: {str(e)}', 'warning')
        else:
            flash('Failed to generate test screenshots', 'error')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Test data generation failed: {e}")
        flash(f'Test data generation failed: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize search engine on startup
    if not init_search_engine():
        logger.error("Failed to initialize search engine. Check configuration.")
    
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Find available port
    port = find_available_port(8000)
    if port is None:
        logger.error("No available ports found in range 8000-8099")
        sys.exit(1)
    
    print(f"🚀 Starting Visual Memory Search Web UI...")
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print(f"📱 Open your browser and navigate to the URL above")
    print(f"⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=port) 