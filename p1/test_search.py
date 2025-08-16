#!/usr/bin/env python3
"""
Test Search Functionality with Generated Dataset
Demonstrates Visual Memory Search using the test screenshots
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import VisualMemorySearch

def run_tests():
    """Run all test queries against the test dataset."""
    print("🧪 Running Visual Memory Search Tests")
    print("=" * 50)
    print()
    
    # Test queries covering different aspects
    test_queries = [
        # Basic UI elements
        "blue button",
        "login button", 
        "error message",
        "form input",
        
        # Interface types
        "dashboard",
        "mobile app",
        "dark theme",
        "user profile",
        
        # New screenshot types
        "shopping cart",
        "add to cart",
        "product page",
        "social media",
        "news feed",
        "gaming interface",
        "health bar",
        "inventory",
        "email client",
        "inbox",
        "compose button",
        "weather app",
        "temperature",
        "forecast",
        
        # Visual elements
        "chart",
        "graph",
        "icon",
        "navigation",
        "header",
        "sidebar",
        
        # Colors and themes
        "blue",
        "green",
        "red",
        "dark",
        "light",
        
        # Text content
        "username",
        "password",
        "email",
        "phone",
        "address"
    ]
    
    print(f"📊 Testing {len(test_queries)} queries against test dataset...")
    print()
    
    # Initialize search engine
    try:
        search_engine = VisualMemorySearch("test_screenshots")
        print("✅ Search engine initialized successfully")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize search engine: {e}")
        return
    
    # Run each test query
    for i, query in enumerate(test_queries, 1):
        print(f"🔍 Test {i:2d}: '{query}'")
        print("-" * 40)
        
        try:
            results = search_engine.search(query, top_k=3)
            
            if results:
                for j, result in enumerate(results, 1):
                    filename = result.get('filename', 'Unknown')
                    confidence = result.get('confidence_score', 0.0)
                    print(f"   {j}. {filename} (Confidence: {confidence:.3f})")
            else:
                print("   No results found")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        print()
    
    print("🎉 All tests completed!")
    print()
    print("💡 Tips for better results:")
    print("   • Try specific UI elements: 'blue button', 'login form'")
    print("   • Use descriptive terms: 'shopping cart', 'weather forecast'")
    print("   • Combine concepts: 'dark theme editor', 'mobile app interface'")
    print("   • Test with OpenAI: Set OPENAI_API_KEY for enhanced results")

def main():
    """Main test function."""
    try:
        run_tests()
    except KeyboardInterrupt:
        print("\n\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        print("💡 Check the README.md for troubleshooting tips")

if __name__ == "__main__":
    main() 