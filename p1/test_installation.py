#!/usr/bin/env python3
"""
Test script to verify Visual Memory Search installation
Checks all required packages and dependencies
"""

import sys
import importlib
from pathlib import Path

def test_package(package_name, import_name=None):
    """Test if a package can be imported."""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} - NOT INSTALLED")
        return False

def test_system_dependencies():
    """Test system-level dependencies."""
    print("🔍 Testing System Dependencies")
    print("=" * 40)
    
    # Test Tesseract OCR
    try:
        import pytesseract
        pytesseract.get_tesseract_version()
        print("✅ Tesseract OCR - Working")
    except Exception as e:
        print(f"❌ Tesseract OCR - Error: {e}")
        print("   💡 Install with: brew install tesseract (macOS) or sudo apt-get install tesseract-ocr (Ubuntu)")
    
    print()

def test_python_packages():
    """Test Python package dependencies."""
    print("🐍 Testing Python Packages")
    print("=" * 40)
    
    packages = [
        ("opencv-python", "cv2"),
        ("Pillow", "PIL"),
        ("pytesseract", "pytesseract"),
        ("torch", "torch"),
        ("transformers", "transformers"),
        ("sentence-transformers", "sentence_transformers"),
        ("faiss-cpu", "faiss"),
        ("scikit-learn", "sklearn"),
        ("numpy", "numpy"),
    ]
    
    all_installed = True
    for package, import_name in packages:
        if not test_package(package, import_name):
            all_installed = False
    
    print()
    return all_installed

def test_ai_models():
    """Test AI model loading capabilities."""
    print("🤖 Testing AI Model Capabilities")
    print("=" * 40)
    
    try:
        from sentence_transformers import SentenceTransformer
        print("✅ Sentence Transformers - Available")
        
        # Test model download (this will take time on first run)
        print("📥 Testing model download...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Text embedding model - Loaded successfully")
        
    except Exception as e:
        print(f"❌ AI Models - Error: {e}")
        print("   💡 This might be due to network issues or insufficient disk space")
        return False
    
    try:
        from transformers import pipeline
        print("✅ Transformers Pipeline - Available")
        
    except Exception as e:
        print(f"❌ Transformers Pipeline - Error: {e}")
        return False
    
    print()
    return True

def test_basic_functionality():
    """Test basic functionality without heavy models."""
    print("🧪 Testing Basic Functionality")
    print("=" * 40)
    
    try:
        # Test image processing
        import cv2
        import numpy as np
        from PIL import Image
        
        # Create a test image
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        test_image[25:75, 25:75] = [255, 255, 255]  # White square
        
        # Test PIL
        pil_image = Image.fromarray(test_image)
        print("✅ PIL Image Processing - Working")
        
        # Test OpenCV
        gray = cv2.cvtColor(test_image, cv2.COLOR_RGB2GRAY)
        print("✅ OpenCV Image Processing - Working")
        
        # Test numpy
        if test_image.shape == (100, 100, 3):
            print("✅ NumPy Array Operations - Working")
        
    except Exception as e:
        print(f"❌ Basic Functionality - Error: {e}")
        return False
    
    print()
    return True

def main():
    """Run all tests."""
    print("🚀 Visual Memory Search - Installation Test")
    print("=" * 50)
    print()
    
    all_tests_passed = True
    
    # Test system dependencies
    test_system_dependencies()
    
    # Test Python packages
    if not test_python_packages():
        all_tests_passed = False
    
    # Test basic functionality
    if not test_basic_functionality():
        all_tests_passed = False
    
    # Test AI models (optional, can be slow)
    print("🤖 AI Model Testing (Optional - Can be slow on first run)")
    print("   Press Enter to skip, or wait for model download...")
    
    try:
        import select
        if select.select([sys.stdin], [], [], 5.0)[0]:  # Wait 5 seconds for input
            input()
            print("⏭️  Skipping AI model test")
        else:
            if not test_ai_models():
                print("⚠️  AI models test failed, but basic functionality should still work")
    except:
        print("⏭️  Skipping AI model test")
    
    # Summary
    print("📊 Test Summary")
    print("=" * 40)
    
    if all_tests_passed:
        print("🎉 All basic tests passed!")
        print("✅ You can now run the Visual Memory Search application")
        print()
        print("🚀 Next steps:")
        print("   1. Create a directory with screenshots")
        print("   2. Run: python main.py /path/to/screenshots")
        print("   3. Or try the demo: python demo.py")
    else:
        print("❌ Some tests failed")
        print("💡 Please check the error messages above and install missing packages")
        print()
        print("🔧 Installation help:")
        print("   pip install -r requirements.txt")
        print("   brew install tesseract  # macOS")
        print("   sudo apt-get install tesseract-ocr  # Ubuntu")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("💡 Check the README.md for troubleshooting tips") 