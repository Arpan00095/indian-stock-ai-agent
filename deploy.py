#!/usr/bin/env python3
"""
Deployment script for Indian Stock Market AI Agent
"""
import os
import subprocess
import sys
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'main.py',
        'requirements.txt',
        'config.py',
        'data_fetcher.py',
        'oi_analyzer.py',
        'alert_system.py',
        'ai_chat_component.py',
        'trading_agent.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def create_streamlit_config():
    """Create Streamlit configuration for production"""
    config_dir = Path('.streamlit')
    config_dir.mkdir(exist_ok=True)
    
    config_content = """[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#00D4AA"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[browser]
gatherUsageStats = false
"""
    
    with open(config_dir / 'config.toml', 'w') as f:
        f.write(config_content)
    
    print("✅ Streamlit config created")

def create_procfile():
    """Create Procfile for Heroku deployment"""
    procfile_content = "web: streamlit run main.py --server.port=$PORT --server.address=0.0.0.0"
    
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    
    print("✅ Procfile created")

def create_runtime_file():
    """Create runtime.txt for Heroku"""
    runtime_content = "python-3.11.0"
    
    with open('runtime.txt', 'w') as f:
        f.write(runtime_content)
    
    print("✅ runtime.txt created")

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# Environment variables
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Database
*.db
*.sqlite3

# Streamlit
.streamlit/secrets.toml

# Temporary files
*.tmp
*.temp
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore created")

def test_application():
    """Test if the application runs without errors"""
    print("🧪 Testing application...")
    
    try:
        # Test import
        import main
        print("✅ Application imports successfully")
        
        # Test basic functionality
        from trading_agent import IndianStockTradingAgent
        agent = IndianStockTradingAgent()
        print("✅ Trading agent initializes successfully")
        
        return True
    except Exception as e:
        print(f"❌ Application test failed: {e}")
        return False

def main():
    """Main deployment preparation"""
    print("🚀 Preparing Indian Stock Market AI Agent for deployment...")
    print("=" * 60)
    
    # Check requirements
    if not check_requirements():
        print("❌ Deployment preparation failed")
        sys.exit(1)
    
    # Create configuration files
    create_streamlit_config()
    create_procfile()
    create_runtime_file()
    create_gitignore()
    
    # Test application
    if not test_application():
        print("❌ Application test failed")
        sys.exit(1)
    
    print("=" * 60)
    print("✅ Deployment preparation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Push your code to GitHub")
    print("2. Choose a deployment platform:")
    print("   - Streamlit Cloud (Free): https://share.streamlit.io")
    print("   - Railway (Free tier): https://railway.app")
    print("   - Render (Free tier): https://render.com")
    print("   - Heroku (Paid): https://heroku.com")
    print("\n🔗 Quick deployment links:")
    print("- Streamlit Cloud: https://share.streamlit.io")
    print("- Railway: https://railway.app")
    print("- Render: https://render.com")
    print("\n📚 See README_DEPLOYMENT.md for detailed instructions")

if __name__ == "__main__":
    main()
