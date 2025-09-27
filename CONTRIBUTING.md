# 🤝 Contributing to Credential Tester

Thank you for your interest in contributing to the Credential Tester project! We welcome contributions from the community and appreciate your help in making this tool better.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Documentation](#documentation)

## 📜 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code. Please report unacceptable behavior to the project maintainers.

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- Git
- Google Chrome browser
- Basic knowledge of Python and Selenium

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/credential-tester-mail.com.git
   cd credential-tester-mail.com
   ```

3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/Houssam-C-H/credential-tester-mail.com.git
   ```

## 🛠️ Development Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### 3. Verify Setup

```bash
# Run tests to verify everything works
python -m pytest tests/

# Run the GUI to test
python simple_gui.py
```

## 🎯 How to Contribute

### Types of Contributions

We welcome several types of contributions:

- 🐛 **Bug Reports**: Report bugs and issues
- 🔧 **Bug Fixes**: Fix existing bugs
- ✨ **New Features**: Add new functionality
- 📚 **Documentation**: Improve documentation
- 🧪 **Tests**: Add or improve tests
- 🎨 **UI/UX**: Improve the GUI interface
- ⚡ **Performance**: Optimize code performance
- 🔒 **Security**: Improve security features

### Contribution Workflow

1. **Check existing issues** and pull requests
2. **Create an issue** for significant changes
3. **Fork the repository** (if you haven't already)
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
5. **Make your changes** following our guidelines
6. **Test your changes** thoroughly
7. **Commit your changes** with clear messages
8. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
9. **Create a Pull Request**

## 📝 Development Guidelines

### Code Style

- **Follow PEP 8**: Use Python's official style guide
- **Use type hints**: Add type annotations for better code clarity
- **Write docstrings**: Document all functions and classes
- **Keep functions small**: Aim for single responsibility
- **Use meaningful names**: Variables and functions should be self-explanatory

### Example Code Style

```python
def test_login_credentials(email: str, password: str, driver: WebDriver) -> Dict[str, str]:
    """
    Test login credentials against the target website.
    
    Args:
        email: User's email address
        password: User's password
        driver: Selenium WebDriver instance
        
    Returns:
        Dictionary containing test results and status
        
    Raises:
        TimeoutException: If login elements are not found
        WebDriverException: If browser operation fails
    """
    try:
        # Implementation here
        pass
    except Exception as e:
        logger.error(f"Login test failed for {email}: {e}")
        raise
```

### File Organization

```
credential-tester-mail.com/
├── src/                    # Source code
│   ├── core/              # Core functionality
│   ├── gui/               # GUI components
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── docs/                   # Documentation
├── examples/               # Example files
└── scripts/               # Build and deployment scripts
```

### Git Commit Messages

Use clear, descriptive commit messages:

```bash
# Good commit messages
git commit -m "Add rate limiting to prevent server overload"
git commit -m "Fix WebDriver timeout issues on slow connections"
git commit -m "Update documentation for new GUI features"

# Bad commit messages
git commit -m "fix"
git commit -m "update stuff"
git commit -m "changes"
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_login.py

# Run with coverage
python -m pytest --cov=src tests/

# Run with verbose output
python -m pytest -v tests/
```

### Writing Tests

Create test files in the `tests/` directory:

```python
# tests/test_login.py
import pytest
from src.core.login_tester import LoginTester

class TestLoginTester:
    def test_valid_credentials(self):
        """Test login with valid credentials."""
        tester = LoginTester()
        result = tester.test_credentials("test@example.com", "password123")
        assert result["status"] == "SUCCESS"
    
    def test_invalid_credentials(self):
        """Test login with invalid credentials."""
        tester = LoginTester()
        result = tester.test_credentials("invalid@example.com", "wrongpass")
        assert result["status"] == "FAILED"
```

### Test Coverage

- Aim for at least 80% code coverage
- Test both success and failure scenarios
- Include edge cases and error conditions
- Test GUI components with mock objects

## 📚 Documentation

### Code Documentation

- **Docstrings**: Use Google-style docstrings
- **Comments**: Explain complex logic and business rules
- **Type hints**: Add type annotations for better IDE support

### User Documentation

- **README updates**: Update README.md for new features
- **API documentation**: Document new functions and classes
- **Examples**: Provide usage examples for new features
- **Screenshots**: Add screenshots for GUI changes

### Documentation Standards

```python
def setup_webdriver(headless: bool = False) -> WebDriver:
    """
    Setup and configure Selenium WebDriver.
    
    Args:
        headless: Whether to run browser in headless mode
        
    Returns:
        Configured WebDriver instance
        
    Example:
        >>> driver = setup_webdriver(headless=True)
        >>> driver.get("https://example.com")
    """
    # Implementation here
```

## 🔍 Pull Request Process

### Before Submitting

1. **Test your changes** thoroughly
2. **Update documentation** if needed
3. **Add tests** for new functionality
4. **Check code style** with linters
5. **Update CHANGELOG.md** if applicable

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Security enhancement

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

### Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** on different environments
4. **Documentation** review
5. **Approval** and merge

## 🐛 Issue Reporting

### Bug Reports

When reporting bugs, include:

- **Clear description** of the issue
- **Steps to reproduce** the problem
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, etc.)
- **Error messages** and logs
- **Screenshots** if applicable

### Feature Requests

For new features, include:

- **Use case** and motivation
- **Detailed description** of the feature
- **Proposed implementation** (if you have ideas)
- **Alternative solutions** considered

### Issue Template

```markdown
## Bug Report / Feature Request

### Description
[Clear description of the issue or feature]

### Environment
- OS: [e.g., Windows 10, macOS 12, Ubuntu 20.04]
- Python Version: [e.g., 3.9.7]
- Browser: [e.g., Chrome 95.0.4638.69]

### Steps to Reproduce (for bugs)
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happens]

### Additional Context
[Any other relevant information]
```

## 🏷️ Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated
- [ ] Release notes prepared
- [ ] Tag created in Git

## 🤔 Questions?

If you have questions about contributing:

- **Check existing issues** for similar questions
- **Create a new issue** with the "question" label
- **Join discussions** in existing issues
- **Contact maintainers** for urgent matters

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page
- **Project documentation**

Thank you for contributing to the Credential Tester project! 🎉
