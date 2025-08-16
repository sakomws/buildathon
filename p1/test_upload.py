#!/usr/bin/env python3
"""
Test script for upload functionality
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_port_finding():
    """Test the port finding functionality."""
    try:
        from app import find_available_port
        port = find_available_port(8000)
        print(f"✅ Port finding works: {port}")
        return True
    except Exception as e:
        print(f"❌ Port finding failed: {e}")
        return False

def test_search_engine_init():
    """Test search engine initialization."""
    try:
        from main import VisualMemorySearch
        search_engine = VisualMemorySearch('test_screenshots')
        print(f"✅ Search engine initialized: {search_engine}")
        return True
    except Exception as e:
        print(f"❌ Search engine init failed: {e}")
        return False

def test_file_upload_logic():
    """Test the file upload logic."""
    try:
        from app import allowed_file, UPLOAD_FOLDER
        print(f"✅ Upload folder: {UPLOAD_FOLDER}")
        
        # Test allowed file types
        test_files = ['test.png', 'test.jpg', 'test.jpeg', 'test.gif', 'test.bmp', 'test.txt']
        for test_file in test_files:
            is_allowed = allowed_file(test_file)
            print(f"   {test_file}: {'✅' if is_allowed else '❌'}")
        
        return True
    except Exception as e:
        print(f"❌ File upload logic test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing upload functionality...")
    print("=" * 40)
    
    tests = [
        ("Port Finding", test_port_finding),
        ("Search Engine Init", test_search_engine_init),
        ("File Upload Logic", test_file_upload_logic),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\n🎯 Overall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}") 