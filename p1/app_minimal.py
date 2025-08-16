#!/usr/bin/env python3
"""
Project 1: Visual Memory Search - Minimal Web UI
A minimal Flask web application for testing file uploads only.
This version skips ALL heavy initialization for instant startup.
"""

import os
import sys
import socket
from pathlib import Path
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

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

@app.route('/')
def index():
    """Main page with upload interface only."""
    # Get list of uploaded files
    try:
        uploaded_files = []
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                if allowed_file(filename):
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        uploaded_files.append({
                            'filename': filename,
                            'size': file_size,
                            'size_kb': round(file_size / 1024, 1)
                        })
    except Exception as e:
        logger.error(f"Failed to list uploaded files: {e}")
        uploaded_files = []
    
    return render_template('index.html', screenshots=uploaded_files, error=False)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads."""
    logger.info("Upload request received")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request content type: {request.content_type}")
    logger.info(f"Request files: {list(request.files.keys()) if request.files else 'No files'}")
    logger.info(f"Request form: {list(request.form.keys()) if request.form else 'No form data'}")
    
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
            
            logger.info("File uploaded successfully!")
            flash(f'File {filename} uploaded successfully!', 'success')
        else:
            logger.error(f"Invalid file type: {file.filename}")
            flash('Invalid file type. Allowed: PNG, JPG, JPEG, GIF, BMP', 'error')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        logger.error(f"Upload failed with exception: {e}")
        flash(f'Upload failed: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    """Handle search requests (placeholder for now)."""
    return jsonify({
        'success': True,
        'query': request.form.get('query', ''),
        'results': [],
        'total_results': 0,
        'message': 'Search functionality not available in minimal mode. Focus on upload testing.',
        'openai_available': False
    })

@app.route('/status')
def status():
    """Get system status."""
    try:
        # Count uploaded files
        total_files = 0
        if os.path.exists(UPLOAD_FOLDER):
            total_files = len([f for f in os.listdir(UPLOAD_FOLDER) if allowed_file(f)])
        
        return jsonify({
            'status': 'ok',
            'total_screenshots': total_files,
            'openai_available': False,
            'message': 'Minimal mode - upload functionality only'
        })
        
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        })

@app.route('/image/<path:filename>')
def serve_image(filename):
    """Serve images from uploads directory."""
    try:
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        
        if os.path.exists(upload_path):
            from flask import send_file
            return send_file(upload_path, mimetype='image/png')
        else:
            return "Image not found", 404
            
    except Exception as e:
        logger.error(f"Failed to serve image {filename}: {e}")
        return "Error serving image", 500

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Find available port
    port = find_available_port(8000)
    if port is None:
        logger.error("No available ports found in range 8000-8099")
        sys.exit(1)
    
    print(f"🚀 Starting Visual Memory Search Web UI (Minimal Mode)...")
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print(f"📱 Open your browser and navigate to the URL above")
    print(f"⏹️  Press Ctrl+C to stop the server")
    print(f"⚡ Minimal mode: Upload functionality only - instant startup")
    print("-" * 60)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=port) 