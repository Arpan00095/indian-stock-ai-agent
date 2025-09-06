#!/usr/bin/env python3
"""
Installation Script for Indian Stock Market AI Agent
Automatically sets up the environment and dependencies
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
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python 3.8+ required. Current version: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install requirements
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("\n📝 Creating .env file...")
        try:
            with open("env_example.txt", "r") as f:
                env_content = f.read()
            
            with open(".env", "w") as f:
                f.write(env_content)
            
            print("✅ .env file created from template")
            print("💡 Edit .env file to add your API keys")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def test_installation():
    """Test if installation was successful"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        import yfinance
        import pandas
        import numpy
        import streamlit
        import plotly
        import requests
        
        print("✅ All required packages imported successfully")
        
        # Test basic functionality
        from data_fetcher import IndianMarketDataFetcher
        from oi_analyzer import OIAnalyzer
        from alert_system import AlertSystem
        
        print("✅ All modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def show_next_steps():
    """Show next steps for the user"""
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Edit .env file to add your API keys (optional)")
    print("2. Run quick demo: python quick_start.py")
    print("3. Start web interface: python main.py --web")
    print("4. Use command line: python main.py --cli")
    print("\n📚 Documentation:")
    print("- README.md: Complete usage guide")
    print("- Master cheatsheet: Available in web interface")
    print("\n🚀 Quick Start:")
    print("python quick_start.py")

def main():
    """Main installation function"""
    print("🇮🇳 Indian Stock Market AI Agent - Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Installation failed: Incompatible Python version")
        return False
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Installation failed: Dependency installation failed")
        return False
    
    # Create .env file
    if not create_env_file():
        print("\n⚠️ Warning: Could not create .env file")
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation failed: Test failed")
        return False
    
    # Show next steps
    show_next_steps()
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
