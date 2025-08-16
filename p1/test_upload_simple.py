#!/usr/bin/env python3
"""
Simple test for upload functionality
"""

import os
import sys
from pathlib import Path

def test_file_upload_basics():
    """Test basic file upload functionality."""
    print("🧪 Testing basic file upload functionality...")
    
    # Test 1: Check if uploads directory exists
    uploads_dir = 'uploads'
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
        print(f"✅ Created uploads directory: {uploads_dir}")
    else:
        print(f"✅ Uploads directory exists: {uploads_dir}")
    
    # Test 2: Check if we can create a test file
    test_file_path = os.path.join(uploads_dir, 'test_upload.txt')
    try:
        with open(test_file_path, 'w') as f:
            f.write('Test upload file')
        print(f"✅ Created test file: {test_file_path}")
        
        # Clean up
        os.remove(test_file_path)
        print(f"✅ Cleaned up test file")
        
    except Exception as e:
        print(f"❌ Failed to create test file: {e}")
        return False
    
    # Test 3: Check if main.py exists and can be imported
    try:
        sys.path.append(str(Path(__file__).parent))
        from main import VisualMemorySearch
        print("✅ VisualMemorySearch class imported successfully")
        
        # Test 4: Check if search engine can be initialized
        if os.path.exists('test_screenshots'):
            try:
                search_engine = VisualMemorySearch('test_screenshots')
                print("✅ Search engine initialized successfully")
                return True
            except Exception as e:
                print(f"❌ Search engine initialization failed: {e}")
                return False
        else:
            print("⚠️  test_screenshots directory not found, skipping search engine test")
            return True
            
    except ImportError as e:
        print(f"❌ Failed to import VisualMemorySearch: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting upload functionality test...")
    print("=" * 50)
    
    success = test_file_upload_basics()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Upload functionality should work.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    print("\n💡 Next steps:")
    print("   1. Wait for the web server to finish initializing")
    print("   2. Open the web UI in your browser")
    print("   3. Try uploading a file to test the functionality") 