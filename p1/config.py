#!/usr/bin/env python3
"""
Configuration file for Visual Memory Search
"""

import os
from pathlib import Path

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_MODEL = "gpt-4-vision-preview"
OPENAI_MAX_TOKENS = 2000
OPENAI_TEMPERATURE = 0.1

# Search Configuration
DEFAULT_TOP_K = 5
MIN_CONFIDENCE_THRESHOLD = 0.1
MAX_CONFIDENCE_THRESHOLD = 1.0

# Image Processing
MAX_IMAGE_SIZE = 2048  # OpenAI supports larger images
SUPPORTED_FORMATS = ['.png', '.jpg', '.jpeg']

# UI Detection
BUTTON_MIN_WIDTH = 50
BUTTON_MAX_WIDTH = 300
BUTTON_MIN_HEIGHT = 20
BUTTON_MAX_HEIGHT = 100
COLOR_DETECTION_THRESHOLD = 5.0  # Percentage of image

# Boost Factors
COLOR_MATCH_BOOST = 1.8
COLOR_RELATED_BOOST = 1.5
BUTTON_MATCH_BOOST = 1.6
UI_MATCH_BOOST = 1.4
TEXT_MATCH_BOOST = 0.3  # Per matching word

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# File Paths
DEFAULT_INDEX_FILE = "search_index.json"
DEFAULT_EMBEDDINGS_FILE = "embeddings.npy"

def get_openai_config():
    """Get OpenAI configuration."""
    return {
        'api_key': OPENAI_API_KEY,
        'model': OPENAI_MODEL,
        'max_tokens': OPENAI_MAX_TOKENS,
        'temperature': OPENAI_TEMPERATURE
    }

def is_openai_available():
    """Check if OpenAI API is available."""
    return bool(OPENAI_API_KEY)

def get_supported_formats():
    """Get list of supported image formats."""
    return SUPPORTED_FORMATS 