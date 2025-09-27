# 🔐 Credential Tester for Mail.com

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Houssam--C--H-orange.svg)](https://github.com/Houssam-C-H)
[![Selenium](https://img.shields.io/badge/Selenium-4.15.2-red.svg)](https://selenium-python.readthedocs.io/)

A comprehensive Python automation tool for testing login credentials on mail.com using Selenium WebDriver. Features both command-line and GUI interfaces with robust error handling and multiple detection methods.

## 🚀 Features

- **Dual Interface**: Command-line script and modern GUI application
- **Smart Detection**: Multiple methods to detect successful/failed logins
- **Real-time Results**: Immediate saving of results during testing
- **Progress Tracking**: Live progress updates and detailed logging
- **Error Recovery**: Robust error handling with automatic retry mechanisms
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Security Focused**: Built-in rate limiting and respectful testing practices

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Output Files](#output-files)
- [GUI Interface](#gui-interface)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Security & Ethics](#security--ethics)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Houssam-C-H/credential-tester-mail.com.git
   cd credential-tester-mail.com
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create credentials file**:
   ```bash
   # Create credentials.txt with format: email,password
   echo "test@example.com,password123" > credentials.txt
   ```

4. **Run the tool**:
   ```bash
   # Command line interface
   python credential_tester.py
   
   # Or use the GUI
   python credential_tester_gui.py
   ```

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- Internet connection

### Step-by-step Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Houssam-C-H/credential-tester-mail.com.git
   cd credential-tester-mail.com
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation**:
   ```bash
   python -c "import selenium; print('Selenium installed successfully')"
   ```

## 💻 Usage

### Command Line Interface

1. **Prepare your credentials file** (`credentials.txt`):
   ```
   email1@example.com,password1
   email2@example.com,password2
   email3@example.com,password3
   ```

2. **Run the script**:
   ```bash
   python credential_tester.py
   ```

3. **Monitor progress**: The script will display real-time progress and save results immediately.

### GUI Interface

1. **Launch the GUI**:
   ```bash
   python credential_tester_gui.py
   ```

2. **Select credentials file**: Use the browse button to select your credentials file.

3. **Start testing**: Click "Start Test" and monitor progress in real-time.

4. **View results**: Check the "Working Credentials" and "Failed Credentials" tabs for results.

## 📁 Output Files

The tool generates several output files to track results:

### `working_credentials.txt`
Contains successfully logged-in accounts:
```
mail,pass,loggedin
email1@example.com,password1,SUCCESS
email2@example.com,password2,SUCCESS
```

### `not_working.txt`
Contains failed login attempts:
```
mail,pass,loggedin
email3@example.com,password3,FAILED
email4@example.com,password4,ERROR: Element not found
```

### `login_results.xlsx`
Detailed Excel report with timestamps and full error messages for comprehensive analysis.

## ⚙️ Configuration

### Key Settings in `credential_tester.py`:

```python
LOGIN_URL = "https://www.mail.com/"           # Target website
CREDENTIALS_FILE = "credentials.txt"         # Input file
WORKING_FILE = "working_credentials.txt"      # Success output
NOT_WORKING_FILE = "not_working.txt"         # Failure output
WAIT_TIMEOUT = 15                            # Element wait time (seconds)
```

### Advanced Configuration:

- **Headless Mode**: Uncomment `options.add_argument("--headless")` for background operation
- **Rate Limiting**: Add delays between requests to be respectful
- **Custom Selectors**: Modify element selectors for different websites

## 🎯 GUI Interface

The GUI provides a user-friendly interface with:

- **File Selection**: Browse and select credentials files
- **Real-time Progress**: Live updates during testing
- **Results Display**: Separate tabs for working and failed credentials
- **Live Logging**: Detailed log of all operations
- **Progress Tracking**: Visual progress bar and statistics

### GUI Features:

- ✅ **Working Credentials Tab**: Shows successful logins
- ❌ **Failed Credentials Tab**: Shows failed attempts with error details
- 📝 **Live Log Tab**: Real-time operation logging
- 📊 **Statistics**: Live count of working/failed credentials

## 🔍 Advanced Features

### Smart Login Detection

The tool uses multiple detection methods:

1. **URL Analysis**: Detects successful redirects to dashboard/inbox
2. **Element Detection**: Looks for success indicators on the page
3. **Error Detection**: Identifies common error messages
4. **Form State**: Checks if login form is still visible

### Error Handling

- **Automatic Retry**: Retries failed operations with exponential backoff
- **Multiple WebDriver Strategies**: Falls back to different browser configurations
- **Graceful Degradation**: Continues testing even if individual tests fail
- **Immediate Saving**: Results are saved immediately to prevent data loss

### Performance Optimizations

- **Headless Mode**: Run without GUI for faster execution
- **Resource Management**: Automatic cleanup of browser instances
- **Memory Optimization**: Efficient handling of large credential lists
- **Parallel Processing**: Support for concurrent testing (advanced)

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| **ChromeDriver not found** | The tool automatically downloads the correct version |
| **Element not found** | Check if the website structure has changed |
| **Slow performance** | Enable headless mode or reduce wait times |
| **Memory issues** | Process credentials in smaller batches |

### Debug Mode

Enable detailed logging by modifying the script:
```python
# Add this to see more detailed output
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Tips

1. **Use headless mode** for faster execution
2. **Reduce wait times** if the website is fast
3. **Process in batches** for large credential lists
4. **Monitor system resources** during long runs

## 🔒 Security & Ethics

### ⚠️ Important Security Notice

**This tool is for educational and authorized testing purposes only.**

- ✅ **Authorized Testing**: Only use on systems you own or have explicit permission to test
- ❌ **Unauthorized Access**: Never use for unauthorized penetration testing
- 🔒 **Data Protection**: Handle credentials securely and delete test data after use
- 📋 **Compliance**: Ensure compliance with local laws and regulations

### Best Practices

1. **Rate Limiting**: Add delays between requests to avoid overwhelming servers
2. **Respectful Testing**: Use appropriate timeouts and avoid aggressive testing
3. **Data Security**: Store credentials securely and delete after testing
4. **Logging**: Keep detailed logs for audit purposes

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Getting Started

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Contribution Guidelines

- **Code Style**: Follow PEP 8 Python style guidelines
- **Testing**: Add tests for new features
- **Documentation**: Update documentation for new features
- **Security**: Ensure all changes maintain security best practices

### Areas for Contribution

- 🐛 **Bug Fixes**: Report and fix bugs
- ✨ **New Features**: Add new functionality
- 📚 **Documentation**: Improve documentation and examples
- 🧪 **Testing**: Add more comprehensive tests
- 🔧 **Performance**: Optimize code performance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Houssam-C-H**
- GitHub: [@Houssam-C-H](https://github.com/Houssam-C-H)
- Repository: [credential-tester-mail.com](https://github.com/Houssam-C-H/credential-tester-mail.com)

## 🙏 Acknowledgments

- Selenium WebDriver team for the excellent automation framework
- The Python community for amazing libraries
- Contributors and users who provide feedback and suggestions

---

**⭐ If you find this project helpful, please give it a star!**
