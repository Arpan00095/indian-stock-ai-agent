#!/usr/bin/env python3
"""
GitHub Setup Script for Indian Stock Market AI Agent
"""
import subprocess
import os
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_git_installed():
    """Check if git is installed"""
    try:
        subprocess.run(["git", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def setup_git_repository():
    """Setup git repository"""
    print("🚀 Setting up GitHub repository...")
    print("=" * 50)
    
    # Check if git is installed
    if not check_git_installed():
        print("❌ Git is not installed. Please install Git first:")
        print("   Download from: https://git-scm.com/downloads")
        return False
    
    # Check if already a git repository
    if Path('.git').exists():
        print("✅ Git repository already exists")
    else:
        # Initialize git repository
        if not run_command("git init", "Initializing git repository"):
            return False
    
    # Add all files
    if not run_command("git add .", "Adding files to git"):
        return False
    
    # Check if there are changes to commit
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    if not result.stdout.strip():
        print("✅ No changes to commit")
        return True
    
    # Commit changes
    if not run_command('git commit -m "Initial commit - Indian Stock Market AI Agent"', "Committing changes"):
        return False
    
    print("\n🎉 Git repository setup completed!")
    print("\n📋 Next steps:")
    print("1. Go to https://github.com and create a new repository")
    print("2. Copy the repository URL")
    print("3. Run these commands:")
    print("   git remote add origin YOUR_REPO_URL")
    print("   git branch -M main")
    print("   git push -u origin main")
    print("\n4. Then go to https://share.streamlit.io to deploy!")
    
    return True

def main():
    """Main function"""
    print("🇮🇳 Indian Stock Market AI Agent - GitHub Setup")
    print("=" * 60)
    
    if setup_git_repository():
        print("\n✅ GitHub setup completed successfully!")
        print("\n🚀 Ready for deployment!")
    else:
        print("\n❌ GitHub setup failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
