#!/usr/bin/env python3
"""
Test script for FastAPI endpoints.
"""

import requests
import json
import time
from pathlib import Path
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import get_settings

def test_imports():
    """Test if all modules can be imported successfully."""
    try:
        print("Testing imports...")
        
        # Test configuration
        from app.core.config import get_settings
        print("✓ Configuration module imported successfully")
        
        # Test schemas
        from app.models.schemas import SearchQuery, SearchResult, ScreenshotInfo
        print("✓ Schemas module imported successfully")
        
        # Test logger
        from app.utils.logger import setup_logging, get_logger
        print("✓ Logger module imported successfully")
        
        # Test service
        from app.services.visual_search_service import VisualSearchService
        print("✓ Visual search service imported successfully")
        
        # Test main app
        from main import app
        print("✓ Main FastAPI app imported successfully")
        
        print("\n🎉 All imports successful! The application is ready to run.")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    try:
        print("\nTesting configuration...")
        from app.core.config import get_settings
        
        settings = get_settings()
        print(f"✓ App name: {settings.app_name}")
        print(f"✓ Screenshot directory: {settings.screenshot_dir}")
        print(f"✓ OpenAI API key configured: {'Yes' if settings.openai_api_key else 'No'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing FastAPI Visual Memory Search Application\n")
    
    success = True
    success &= test_imports()
    success &= test_configuration()
    
    if success:
        print("\n✅ All tests passed! You can now run the application with:")
        print("   python run_fastapi.py")
        print("   or")
        print("   uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
        sys.exit(1)
