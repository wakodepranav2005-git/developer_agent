#!/usr/bin/env python3
"""
Installation script for ULCA Desktop GUI
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("   Please use Python 3.8 or higher")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing Python dependencies...")
    
    # Upgrade pip first
    if not run_command("pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install PyQt6
    if not run_command("pip install PyQt6", "Installing PyQt6"):
        return False
    
    # Install requests if not already installed
    try:
        import requests
        print("✅ Requests is already installed")
    except ImportError:
        if not run_command("pip install requests", "Installing requests"):
            return False
    
    return True

def main():
    """Main installation function"""
    print("🚀 ULCA Desktop GUI Installation")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed")
        print("Please check the error messages above and try again")
        sys.exit(1)
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Ensure your local LLM (Ollama) is running:")
    print("   ollama serve")
    print("2. Start the GUI with:")
    print("   python ulca_gui.py")
    print("3. Or use the launcher:")
    print("   python run_gui.py")
    print("4. Or use the demo:")
    print("   python demo_gui.py")

if __name__ == "__main__":
    main()
