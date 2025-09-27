#!/usr/bin/env python3
"""
Installation script for Credential Tester for Mail.com

This script provides an easy way to install and configure
the credential testing tool with all dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Print installation banner."""
    print("=" * 60)
    print("🔐 Credential Tester for Mail.com - Installation")
    print("=" * 60)
    print("Author: Houssam-C-H")
    print("GitHub: https://github.com/Houssam-C-H/credential-tester-mail.com")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible.")
    return True

def check_system_requirements():
    """Check system requirements."""
    print("🖥️ Checking system requirements...")
    
    # Check operating system
    system = platform.system()
    print(f"   Operating System: {system}")
    
    # Check if Chrome is available (optional)
    chrome_paths = {
        "Windows": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ],
        "Darwin": [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        ],
        "Linux": [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
        ]
    }
    
    chrome_found = False
    for path in chrome_paths.get(system, []):
        if os.path.exists(path):
            chrome_found = True
            print(f"✅ Chrome found at: {path}")
            break
    
    if not chrome_found:
        print("⚠️  Warning: Chrome browser not found.")
        print("   The tool will attempt to download ChromeDriver automatically.")
        print("   Make sure you have Chrome installed for best compatibility.")
    
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing dependencies...")
    
    try:
        # Upgrade pip first
        print("   Upgrading pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True)
        
        # Install requirements
        print("   Installing core dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        
        print("✅ Dependencies installed successfully.")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("   Please check your internet connection and try again.")
        return False

def install_dev_dependencies():
    """Install development dependencies (optional)."""
    print("🛠️ Installing development dependencies...")
    
    try:
        if os.path.exists("requirements-dev.txt"):
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"], 
                          check=True, capture_output=True)
            print("✅ Development dependencies installed.")
        else:
            print("⚠️  Development requirements file not found, skipping...")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not install development dependencies: {e}")
        return False

def create_example_files():
    """Create example files."""
    print("📝 Creating example files...")
    
    # Create examples directory
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    # Create example credentials file
    credentials_example = examples_dir / "credentials_example.txt"
    if not credentials_example.exists():
        with open(credentials_example, "w") as f:
            f.write("# Example Credentials File\n")
            f.write("# Format: email,password\n")
            f.write("# Lines starting with # are comments\n\n")
            f.write("test1@example.com,password123\n")
            f.write("test2@example.com,password456\n")
        print("   ✅ Created examples/credentials_example.txt")
    
    # Create example config
    config_example = examples_dir / "config_example.py"
    if not config_example.exists():
        with open(config_example, "w") as f:
            f.write('"""\n')
            f.write("Example Configuration File\n")
            f.write("Copy this file and modify as needed\n")
            f.write('"""\n\n')
            f.write("# Basic configuration\n")
            f.write('LOGIN_URL = "https://www.mail.com/"\n')
            f.write('CREDENTIALS_FILE = "credentials.txt"\n')
        print("   ✅ Created examples/config_example.py")
    
    return True

def run_tests():
    """Run basic tests to verify installation."""
    print("🧪 Running installation tests...")
    
    try:
        # Test imports
        import selenium
        import pandas
        import openpyxl
        import webdriver_manager
        print("   ✅ All core modules imported successfully.")
        
        # Test basic functionality
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print("   ✅ Selenium WebDriver available.")
        
        print("✅ Installation tests passed.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions."""
    print("\n" + "=" * 60)
    print("🎉 Installation Complete!")
    print("=" * 60)
    print()
    print("📋 Usage Instructions:")
    print("1. Create a credentials file (credentials.txt):")
    print("   email1@example.com,password1")
    print("   email2@example.com,password2")
    print()
    print("2. Run the command-line version:")
    print("   python credential_tester.py")
    print()
    print("3. Or run the GUI version:")
    print("   python credential_tester_gui.py")
    print()
    print("📚 Documentation:")
    print("   README.md - Complete documentation")
    print("   examples/ - Example files and configurations")
    print("   CONTRIBUTING.md - How to contribute")
    print()
    print("🔒 Security Notice:")
    print("   Only use this tool on systems you own or have permission to test.")
    print("   Never use for unauthorized access attempts.")
    print()
    print("🆘 Support:")
    print("   GitHub Issues: https://github.com/Houssam-C-H/credential-tester-mail.com/issues")
    print("   Documentation: https://github.com/Houssam-C-H/credential-tester-mail.com#readme")
    print()

def main():
    """Main installation function."""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check system requirements
    if not check_system_requirements():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Installation failed. Please check the errors above.")
        sys.exit(1)
    
    # Install development dependencies (optional)
    install_dev_dependencies()
    
    # Create example files
    create_example_files()
    
    # Run tests
    if not run_tests():
        print("⚠️  Installation completed but tests failed.")
        print("   The tool may still work, but please check the errors above.")
    
    # Print usage instructions
    print_usage_instructions()
    
    print("✅ Installation completed successfully!")
    print("   You can now use the Credential Tester tool.")

if __name__ == "__main__":
    main()
