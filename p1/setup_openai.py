#!/usr/bin/env python3
"""
OpenAI Setup Script for Visual Memory Search
Configures OpenAI API for enhanced visual understanding
"""

import os
import sys
from pathlib import Path

def setup_openai():
    """Setup OpenAI API configuration."""
    print("🔧 OpenAI API Setup for Visual Memory Search")
    print("=" * 50)
    print()
    print("This will enable GPT-4 Vision for much better visual understanding")
    print("and higher confidence scores in your searches.")
    print()
    
    # Check if OpenAI package is installed
    try:
        import openai
        print("✅ OpenAI package is installed")
    except ImportError:
        print("❌ OpenAI package not found")
        print("💡 Install with: pip install openai")
        return False
    
    # Check for existing API key
    current_key = os.getenv('OPENAI_API_KEY')
    if current_key:
        print(f"✅ OpenAI API key already configured")
        print(f"   Key: {current_key[:8]}...{current_key[-4:]}")
        print()
        
        choice = input("Do you want to update the API key? (y/n): ").strip().lower()
        if choice not in ['y', 'yes']:
            print("Keeping existing API key")
            return True
    
    # Get new API key
    print("🔑 Enter your OpenAI API key:")
    print("   Get one from: https://platform.openai.com/api-keys")
    print()
    
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided")
        return False
    
    # Test the API key
    print("\n🧪 Testing API key...")
    try:
        openai.api_key = api_key
        
        # Test with a simple API call
        response = openai.Model.list()
        print("✅ API key is valid!")
        
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        print("💡 Please check your API key and try again")
        return False
    
    # Save to environment file
    env_file = Path(".env")
    if env_file.exists():
        # Update existing .env file
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Remove existing OPENAI_API_KEY line
        lines = [line for line in lines if not line.startswith('OPENAI_API_KEY')]
        
        # Add new API key
        lines.append(f"OPENAI_API_KEY={api_key}\n")
        
        with open(env_file, 'w') as f:
            f.writelines(lines)
    else:
        # Create new .env file
        with open(env_file, 'w') as f:
            f.write(f"OPENAI_API_KEY={api_key}\n")
    
    print(f"✅ API key saved to {env_file}")
    
    # Instructions for using
    print("\n📋 Next Steps:")
    print("1. Restart your terminal or run: source .env")
    print("2. Rebuild your search index: python main.py test_screenshots --rebuild")
    print("3. Test with: python main.py test_screenshots --query 'blue button'")
    print()
    print("🎉 OpenAI integration is now configured!")
    print("   You should see much higher confidence scores and better visual understanding!")
    
    return True

def check_openai_status():
    """Check OpenAI API status."""
    print("🔍 OpenAI API Status Check")
    print("=" * 30)
    
    try:
        import openai
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            print(f"✅ API Key: {api_key[:8]}...{api_key[-4:]}")
            
            # Test API
            try:
                openai.api_key = api_key
                response = openai.Model.list()
                print("✅ API Connection: Working")
                print("✅ Ready for enhanced visual search!")
            except Exception as e:
                print(f"❌ API Connection: Failed - {e}")
                
        else:
            print("❌ No API key found")
            print("💡 Run: python setup_openai.py")
            
    except ImportError:
        print("❌ OpenAI package not installed")
        print("💡 Install with: pip install openai")

def main():
    """Main setup function."""
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        check_openai_status()
    else:
        setup_openai()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("💡 Check the README.md for troubleshooting tips") 