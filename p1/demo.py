#!/usr/bin/env python3
"""
Demo script for Visual Memory Search
Shows how to use the VisualMemorySearch class programmatically
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import VisualMemorySearch

def demo_basic_usage():
    """Demonstrate basic usage of the VisualMemorySearch class."""
    print("🔍 Visual Memory Search - Demo Mode")
    print("=" * 50)
    
    # Create a demo screenshots directory
    demo_dir = Path("demo_screenshots")
    demo_dir.mkdir(exist_ok=True)
    
    print(f"📁 Using demo directory: {demo_dir.absolute()}")
    
    # Check if there are any screenshots
    screenshot_files = list(demo_dir.glob("*.png")) + list(demo_dir.glob("*.jpg")) + list(demo_dir.glob("*.jpeg"))
    
    if not screenshot_files:
        print("📭 No screenshots found in demo directory.")
        print("💡 You can:")
        print("   1. Add some screenshots manually")
        print("   2. Use the test dataset: python main.py test_screenshots")
        print("   3. Generate test data: python generate_test_dataset.py")
        print()
        return
    
    # Initialize the search engine
    try:
        search_engine = VisualMemorySearch(str(demo_dir))
        print("✅ Search engine initialized successfully!")
        
        # Show available commands
        print("\n📋 Available Demo Commands:")
        print("  1. list    - List indexed screenshots")
        print("  2. search  - Perform a search query")
        print("  3. add     - Add a screenshot (if you have one)")
        print("  4. quit    - Exit demo")
        
        while True:
            try:
                command = input("\n🎯 Demo command (list/search/add/quit): ").strip().lower()
                
                if command == 'quit':
                    print("👋 Thanks for trying Visual Memory Search!")
                    break
                    
                elif command == 'list':
                    screenshots = search_engine.list_screenshots()
                    if screenshots:
                        print(f"\n📱 Found {len(screenshots)} indexed screenshots:")
                        for ss in screenshots:
                            print(f"  • {ss['filename']} ({ss['dimensions'][0]}x{ss['dimensions'][1]})")
                    else:
                        print("📭 No screenshots indexed yet.")
                        print("💡 Add some screenshots to see them here!")
                
                elif command == 'search':
                    query = input("🔍 Enter search query: ").strip()
                    if query:
                        print(f"\n🔍 Searching for: '{query}'")
                        results = search_engine.search(query)
                        
                        if results:
                            print(f"\n📊 Found {len(results)} results:")
                            print("-" * 40)
                            for i, result in enumerate(results, 1):
                                print(f"{i:2d}. {result['filename']:<30} Score: {result['confidence_score']:.3f}")
                        else:
                            print("❌ No results found.")
                            print("💡 Try adding some screenshots first!")
                    else:
                        print("❌ Please enter a search query.")
                
                elif command == 'add':
                    file_path = input("📁 Enter path to screenshot file: ").strip()
                    if file_path and os.path.exists(file_path):
                        if search_engine.add_screenshot(file_path):
                            print(f"✅ Successfully added: {file_path}")
                        else:
                            print(f"❌ Failed to add: {file_path}")
                    else:
                        print("❌ File not found. Please provide a valid path.")
                
                else:
                    print("❓ Unknown command. Available: list, search, add, quit")
                    
            except KeyboardInterrupt:
                print("\n\n👋 Demo interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    except Exception as e:
        print(f"❌ Failed to initialize search engine: {e}")
        print("\n💡 Make sure you have:")
        print("  1. Installed all requirements: pip install -r requirements.txt")
        print("  2. Installed Tesseract OCR")
        print("  3. Sufficient disk space for AI models")

def demo_advanced_features():
    """Demonstrate advanced features and API usage."""
    print("\n🚀 Advanced Features Demo")
    print("=" * 30)
    
    demo_dir = Path("demo_screenshots")
    
    try:
        # Check if there are screenshots
        screenshot_files = list(demo_dir.glob("*.png")) + list(demo_dir.glob("*.jpg")) + list(demo_dir.glob("*.jpeg"))
        
        if not screenshot_files:
            print("📭 No screenshots found. Skipping advanced demo.")
            return
        
        search_engine = VisualMemorySearch(str(demo_dir))
        
        # Show system info
        print(f"📊 System Information:")
        print(f"  • Screenshots indexed: {len(search_engine.screenshots_data)}")
        print(f"  • Index file: {search_engine.index_file}")
        print(f"  • Embeddings file: {search_engine.embeddings_file}")
        print(f"  • Models loaded: {search_engine.embedding_model is not None}")
        
        # Show search capabilities
        print(f"\n🔍 Search Capabilities:")
        print(f"  • Text search: OCR content")
        print(f"  • Visual search: AI-generated descriptions")
        print(f"  • Semantic search: Natural language understanding")
        print(f"  • Confidence scoring: 0.0 to 1.0")
        
    except Exception as e:
        print(f"❌ Advanced demo failed: {e}")

def demo_test_dataset():
    """Demo using the generated test dataset."""
    print("\n🧪 Test Dataset Demo")
    print("=" * 30)
    
    test_dir = Path("test_screenshots")
    if not test_dir.exists():
        print("❌ Test dataset not found!")
        print("💡 Run 'python generate_test_dataset.py' first")
        return
    
    try:
        print(f"📁 Using test dataset: {test_dir.absolute()}")
        search_engine = VisualMemorySearch(str(test_dir))
        print("✅ Search engine ready!")
        
        # Test some queries
        test_queries = [
            "blue button",
            "login form",
            "dark theme",
            "mobile app",
            "dashboard with charts"
        ]
        
        print(f"\n🧪 Testing {len(test_queries)} queries:")
        print("-" * 40)
        
        for query in test_queries:
            try:
                print(f"\n🔍 Query: '{query}'")
                results = search_engine.search(query, top_k=3)
                
                if results:
                    print(f"📊 Results ({len(results)} found):")
                    for i, result in enumerate(results, 1):
                        print(f"  {i}. {result['filename']:<25} Score: {result['confidence_score']:.3f}")
                else:
                    print("  ❌ No results")
                    
            except Exception as e:
                print(f"  ❌ Search failed: {e}")
        
        print(f"\n💡 Try your own queries!")
        print(f"🚀 Interactive mode: python main.py test_screenshots")
        
    except Exception as e:
        print(f"❌ Test dataset demo failed: {e}")

def main():
    """Main demo function."""
    print("🎉 Welcome to Visual Memory Search Demo!")
    print("This demo shows how to use the search engine interactively.")
    
    try:
        # Basic demo
        demo_basic_usage()
        
        # Advanced features
        demo_advanced_features()
        
        # Test dataset demo
        demo_test_dataset()
        
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Thanks for trying!")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("💡 Check the README.md for troubleshooting tips.")

if __name__ == "__main__":
    main() 