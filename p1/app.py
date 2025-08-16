#!/usr/bin/env python3
"""
Project 1: Visual Memory Search - Web UI
A Flask web application for testing the visual memory search system.
"""

import os
import sys
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

def init_search_engine():
    """Initialize the search engine."""
    global search_engine
    try:
        # Use test_screenshots directory if it exists, otherwise create uploads
        screenshots_dir = 'test_screenshots' if os.path.exists('test_screenshots') else 'uploads'
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)
        
        search_engine = VisualMemorySearch(screenshots_dir)
        logger.info(f"Search engine initialized with directory: {screenshots_dir}")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize search engine: {e}")
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
    
    if search_engine is None:
        flash('Search engine not initialized', 'error')
        return redirect(url_for('index'))
    
    try:
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            # Save to uploads folder
            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            file.save(upload_path)
            
            # Add to search index
            if search_engine.add_screenshot(upload_path):
                flash(f'File {filename} uploaded and indexed successfully!', 'success')
            else:
                flash(f'Failed to index file {filename}', 'error')
        else:
            flash('Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP', 'error')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        flash(f'Upload failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/rebuild', methods=['POST'])
def rebuild_index():
    """Rebuild the search index."""
    global search_engine
    
    try:
        if search_engine:
            # Delete existing index files
            if search_engine.index_file.exists():
                search_engine.index_file.unlink()
            if search_engine.embeddings_file.exists():
                search_engine.embeddings_file.unlink()
            
            # Recreate index
            search_engine._create_index()
            flash('Search index rebuilt successfully!', 'success')
        else:
            flash('Search engine not initialized', 'error')
        
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

@app.route('/generate_test_data', methods=['POST'])
def generate_test_data():
    """Generate test dataset."""
    try:
        from generate_test_dataset import generate_all_screenshots
        
        # Generate test screenshots
        success_count = generate_all_screenshots()
        
        if success_count > 0:
            # Rebuild index with new data
            if search_engine:
                if search_engine.index_file.exists():
                    search_engine.index_file.unlink()
                if search_engine.embeddings_file.exists():
                    search_engine.embeddings_file.unlink()
                search_engine._create_index()
            
            flash(f'Generated {success_count} test screenshots and rebuilt index!', 'success')
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
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=8000) 