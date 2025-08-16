#!/usr/bin/env python3
"""
Quick Demo for Visual Memory Search
Tests search functionality with the generated test dataset
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import VisualMemorySearch

def quick_search_demo():
    """Quick demo of search functionality with test dataset."""
    print("🔍 Visual Memory Search - Quick Demo")
    print("=" * 50)
    
    # Check if test dataset exists
    test_dir = Path("test_screenshots")
    if not test_dir.exists():
        print("❌ Test dataset not found!")
        print("💡 Run 'python generate_test_dataset.py' first")
        return
    
    print(f"📁 Using test dataset: {test_dir.absolute()}")
    print(f"📱 Found {len(list(test_dir.glob('*.png')))} test screenshots")
    print()
    
    try:
        # Initialize search engine
        print("🚀 Initializing search engine...")
        search_engine = VisualMemorySearch(str(test_dir))
        print("✅ Search engine ready!")
        print()
        
        # Test queries
        test_queries = [
            "blue button",
            "login form", 
            "dark theme interface",
            "mobile app layout",
            "dashboard with charts",
            "error message about auth",
            "404 page not found"
        ]
        
        print("🧪 Testing Search Queries")
        print("=" * 50)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n{i}. 🔍 Query: '{query}'")
            print("-" * 40)
            
            try:
                results = search_engine.search(query, top_k=3)
                
                if results:
                    print(f"📊 Found {len(results)} results:")
                    for j, result in enumerate(results, 1):
                        print(f"  {j}. {result['filename']:<25} Score: {result['confidence_score']:.3f}")
                else:
                    print("❌ No results found")
                    
            except Exception as e:
                print(f"❌ Search failed: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Quick demo complete!")
        print()
        print("💡 Try these additional queries:")
        print("   - 'screenshot with green button'")
        print("   - 'interface with sidebar'")
        print("   - 'form with input fields'")
        print()
        print("🚀 For interactive mode: python main.py test_screenshots")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Installed all requirements: pip install -r requirements.txt")
        print("   2. Generated test dataset: python generate_test_dataset.py")

if __name__ == "__main__":
    try:
        quick_search_demo()
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("💡 Check the README.md for troubleshooting tips") 