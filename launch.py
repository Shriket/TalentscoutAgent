#!/usr/bin/env python3
"""
TalentScout Hiring Assistant Launcher
This script will check dependencies and launch the application
"""

import sys
import os
import subprocess

def check_and_install_packages():
    """Check and install required packages"""
    required_packages = [
        'streamlit>=1.28.0',
        'streamlit-chat>=0.1.1', 
        'groq>=0.4.1',
        'gspread>=5.10.0',
        'google-auth>=2.22.0',
        'pandas>=2.0.0',
        'pydantic>=2.0.0',
        'python-dotenv>=1.0.0',
        'textblob>=0.17.1',
        'googletrans>=4.0.0',
        'email-validator>=2.0.0'
    ]
    
    print("🔍 Checking required packages...")
    
    missing_packages = []
    
    for package in required_packages:
        package_name = package.split('>=')[0].split('==')[0]
        try:
            if package_name == 'streamlit-chat':
                import streamlit_chat
            elif package_name == 'python-dotenv':
                import dotenv
            elif package_name == 'google-auth':
                import google.auth
            elif package_name == 'email-validator':
                import email_validator
            else:
                __import__(package_name)
            print(f"✅ {package_name}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package_name} - Missing")
    
    if missing_packages:
        print(f"\n📦 Installing {len(missing_packages)} missing packages...")
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"✅ Installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False
    
    return True

def launch_streamlit():
    """Launch the Streamlit application"""
    print("\n🚀 Launching TalentScout Hiring Assistant...")
    
    try:
        # Set environment variables for better Streamlit experience
        os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
        os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
        os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'
        
        # Launch Streamlit
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'main.py', '--server.port', '8501'])
        
    except KeyboardInterrupt:
        print("\n👋 TalentScout application stopped.")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🤖 TalentScout Hiring Assistant Launcher")
    print("=" * 60)
    
    print(f"Python: {sys.version}")
    print(f"Executable: {sys.executable}")
    print()
    
    # Check and install packages
    if not check_and_install_packages():
        print("❌ Failed to install required packages. Please check your internet connection.")
        return
    
    print("\n✅ All packages ready!")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("\n⚠️  Warning: .env file not found!")
        print("Please copy .env.example to .env and add your API keys:")
        print("- GROQ_API_KEY (required)")
        print("- GOOGLE_SHEET_ID (optional)")
        print("- GOOGLE_SERVICE_ACCOUNT_JSON (optional)")
        print()
        
        response = input("Continue anyway? (y/n): ").lower().strip()
        if response != 'y':
            print("Please set up your .env file first.")
            return
    
    # Launch the application
    launch_streamlit()

if __name__ == "__main__":
    main()
