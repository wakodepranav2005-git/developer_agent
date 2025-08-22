#!/usr/bin/env python3
"""
ULCA Setup Test Script
Run this to verify your ULCA installation and LLM connectivity
"""

import requests
import json
import sys
import os
from pathlib import Path

def test_llm_connectivity():
    """Test connection to local LLM API"""
    print("🧪 Testing LLM connectivity...")
    
    # Test Ollama API
    ollama_url = "http://localhost:11434/api/generate"
    
    try:
        # Simple test request
        test_payload = {
            "model": "claude-3.5-sonnet",
            "prompt": "Hello! Please respond with 'Connection successful!'",
            "stream": False,
            "options": {
                "temperature": 0.1,
                "max_tokens": 50
            }
        }
        
        print(f"📡 Testing connection to: {ollama_url}")
        response = requests.post(ollama_url, json=test_payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if "response" in result:
                print(f"✅ LLM connection successful!")
                print(f"🤖 Response: {result['response']}")
                return True
            else:
                print(f"⚠️  Unexpected response format: {result}")
                return False
        else:
            print(f"❌ HTTP {response.status_code}: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed. Is Ollama running?")
        print("   Try: ollama serve")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out. Check your model loading.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_python_dependencies():
    """Test required Python packages"""
    print("\n🐍 Testing Python dependencies...")
    
    required_packages = ['requests', 'pathlib']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - Missing")
            print(f"   Install with: pip install {package}")
            return False
    
    return True

def test_directory_permissions():
    """Test write permissions in current directory"""
    print("\n📁 Testing directory permissions...")
    
    current_dir = Path.cwd()
    test_file = current_dir / "ulca_test_permissions.tmp"
    
    try:
        # Test write permission
        test_file.write_text("test")
        test_file.unlink()  # Clean up
        print(f"✅ Write permissions OK in: {current_dir}")
        return True
    except Exception as e:
        print(f"❌ Write permission denied in: {current_dir}")
        print(f"   Error: {e}")
        return False

def test_file_operations():
    """Test basic file operations"""
    print("\n📝 Testing file operations...")
    
    test_content = {
        "test": "data",
        "timestamp": "2024-01-01T00:00:00"
    }
    
    try:
        # Test JSON file creation
        test_file = Path("ulca_test_file.json")
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_content, f, indent=2)
        
        # Test JSON file reading
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_content = json.load(f)
        
        if loaded_content == test_content:
            print("✅ File read/write operations OK")
        else:
            print("❌ File content mismatch")
            return False
        
        # Clean up
        test_file.unlink()
        return True
        
    except Exception as e:
        print(f"❌ File operations failed: {e}")
        return False

def show_setup_instructions():
    """Show setup instructions if tests fail"""
    print("\n📚 Setup Instructions:")
    print("1. Install Python 3.10+")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Start Ollama: ollama serve")
    print("4. Pull Claude model: ollama pull claude-3.5-sonnet")
    print("5. Run ULCA: python universal_claude_agent.py")

def main():
    """Run all tests"""
    print("🚀 ULCA Setup Test")
    print("=" * 40)
    
    tests = [
        ("Python Dependencies", test_python_dependencies),
        ("Directory Permissions", test_directory_permissions),
        ("File Operations", test_file_operations),
        ("LLM Connectivity", test_llm_connectivity)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 Test Results Summary:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! ULCA is ready to use.")
        print("   Run: python universal_claude_agent.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        show_setup_instructions()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
