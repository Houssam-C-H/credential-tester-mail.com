"""
Setup script for Credential Tester for Mail.com

This script provides an easy way to install and configure
the credential testing tool.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Read development requirements
def read_dev_requirements():
    try:
        with open("requirements-dev.txt", "r", encoding="utf-8") as fh:
            return [line.strip() for line in fh if line.strip() and not line.startswith("#") and not line.startswith("-r")]
    except FileNotFoundError:
        return []

setup(
    name="credential-tester-mail",
    version="1.0.0",
    author="Houssam-C-H",
    author_email="houssam@example.com",
    description="A comprehensive Python automation tool for testing login credentials on mail.com",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/Houssam-C-H/credential-tester-mail.com",
    project_urls={
        "Bug Reports": "https://github.com/Houssam-C-H/credential-tester-mail.com/issues",
        "Source": "https://github.com/Houssam-C-H/credential-tester-mail.com",
        "Documentation": "https://github.com/Houssam-C-H/credential-tester-mail.com#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Testing",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": read_dev_requirements(),
        "test": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.0",
            "pytest-xdist>=3.3.0",
        ],
        "docs": [
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
        ],
        "security": [
            "bandit>=1.7.5",
            "safety>=2.3.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "credential-tester=credential_tester:main",
            "credential-tester-gui=credential_tester_gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml", "*.json"],
    },
    keywords=[
        "selenium",
        "automation",
        "testing",
        "credentials",
        "login",
        "mail.com",
        "webdriver",
        "gui",
        "security",
        "penetration-testing",
    ],
    zip_safe=False,
    platforms=["any"],
    license="MIT",
    # Additional metadata
    maintainer="Houssam-C-H",
    maintainer_email="houssam@example.com",
    download_url="https://github.com/Houssam-C-H/credential-tester-mail.com/archive/v1.0.0.tar.gz",
    # Long description from README
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    # Project URLs
    project_urls={
        "Homepage": "https://github.com/Houssam-C-H/credential-tester-mail.com",
        "Bug Reports": "https://github.com/Houssam-C-H/credential-tester-mail.com/issues",
        "Source": "https://github.com/Houssam-C-H/credential-tester-mail.com",
        "Documentation": "https://github.com/Houssam-C-H/credential-tester-mail.com#readme",
        "Changelog": "https://github.com/Houssam-C-H/credential-tester-mail.com/blob/main/CHANGELOG.md",
    },
)

# Additional setup information
if __name__ == "__main__":
    print("Credential Tester for Mail.com - Setup")
    print("=====================================")
    print("This package provides automated login testing for mail.com")
    print("using Selenium WebDriver with both CLI and GUI interfaces.")
    print()
    print("For more information, visit:")
    print("https://github.com/Houssam-C-H/credential-tester-mail.com")
    print()
    print("Installation:")
    print("pip install -e .")
    print()
    print("Development installation:")
    print("pip install -e .[dev]")
    print()
    print("Testing:")
    print("pip install -e .[test]")
    print("pytest")
    print()
    print("Documentation:")
    print("pip install -e .[docs]")
    print()
    print("Security scanning:")
    print("pip install -e .[security]")
    print("bandit -r .")
    print("safety check")
