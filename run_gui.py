#!/usr/bin/env python3
"""
Simple launcher script for ULCA Desktop GUI
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import PyQt6
        print("✅ PyQt6 is installed")
    except ImportError:
        print("❌ PyQt6 is not installed")
        print("Please install it with: pip install PyQt6")
        return False
    
    try:
        import requests
        print("✅ Requests is installed")
    except ImportError:
        print("❌ Requests is not installed")
        print("Please install it with: pip install requests")
        return False
    
    return True

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running")
            return True
        else:
            print("⚠️  Ollama responded but with unexpected status")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama is not running")
        print("Please start Ollama with: ollama serve")
        return False
    except Exception as e:
        print(f"⚠️  Error checking Ollama: {e}")
        return False

def main():
    """Main launcher function"""
    print("🚀 ULCA Desktop GUI Launcher")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again.")
        sys.exit(1)
    
    # Check Ollama
    print("\n🔍 Checking Ollama status...")
    ollama_running = check_ollama()
    
    if not ollama_running:
        print("\n⚠️  Warning: Ollama is not running.")
        print("The GUI will start but LLM features won't work.")
        print("You can start Ollama in another terminal with: ollama serve")
        
        response = input("\nContinue anyway? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            print("Exiting...")
            sys.exit(0)
    
    # Launch GUI
    print("\n🚀 Starting ULCA Desktop GUI...")
    try:
        # Import and run the GUI
        from ulca_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI: {e}")
        print("Make sure ulca_gui.py is in the current directory")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
