#!/usr/bin/env python3
"""
🖥️ Simple GUI for Credential Tester - Mail.com

This is a user-friendly graphical interface for the Credential Tester application.
It provides an easy-to-use interface for testing login credentials with real-time
progress tracking and result display.

📋 Features:
- File selection for credentials
- Real-time progress tracking
- Live result display
- Background testing with subprocess
- Immediate result saving
- Comprehensive logging

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

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import subprocess
import os
import sys
import time
from datetime import datetime
import queue

# =============================================================================
# MAIN GUI CLASS
# =============================================================================

class SimpleLoginGUI:
    """
    Simple GUI class for the Login Automation Tool.
    
    This class provides a user-friendly interface for:
    - Selecting credentials files
    - Starting and stopping tests
    - Viewing real-time progress
    - Displaying results
    - Managing test processes
    """
    
    def __init__(self, root):
        """
        Initialize the GUI application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("🔐 Login Automation Tool - Simple GUI")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # Application state variables
        self.test_running = False          # Whether a test is currently running
        self.test_process = None           # Subprocess for running tests
        self.message_queue = queue.Queue() # Queue for thread-safe communication
        
        # Create the user interface
        self.create_interface()
        
        # Start background processes
        self.process_messages()            # Start message processing
        self.periodic_refresh()           # Start periodic refresh during testing

    def create_interface(self):
        """
        Create the main user interface.
        
        This function creates all the GUI elements including:
        - Header with title and version
        - File selection controls
        - Status and progress displays
        - Control buttons
        - Results display tabs
        - Footer information
        """
        # Main container frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # =====================================================================
        # HEADER SECTION
        # =====================================================================
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Application title
        title_label = ttk.Label(header_frame, text="🔐 Login Automation Tool", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # Version/subtitle
        version_label = ttk.Label(header_frame, text="Simple GUI Interface", 
                                 font=('Arial', 10), foreground='gray')
        version_label.pack(side=tk.RIGHT)
        
        # =====================================================================
        # CONTROLS SECTION
        # =====================================================================
        
        controls_frame = ttk.LabelFrame(main_frame, text="📋 Test Controls", padding=15)
        controls_frame.pack(fill=tk.X, pady=(0, 15))
        
        # File selection frame
        file_frame = ttk.Frame(controls_frame)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        # File selection label
        ttk.Label(file_frame, text="Credentials File:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # File selection controls
        file_select_frame = ttk.Frame(file_frame)
        file_select_frame.pack(fill=tk.X, pady=(5, 0))
        
        # File path entry field
        self.file_var = tk.StringVar(value="credentials.txt")
        file_entry = ttk.Entry(file_select_frame, textvariable=self.file_var, 
                              font=('Arial', 10), width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Browse button
        browse_btn = ttk.Button(file_select_frame, text="📁 Browse", 
                               command=self.browse_file, width=10)
        browse_btn.pack(side=tk.RIGHT)
        
        # =====================================================================
        # STATUS DISPLAY SECTION
        # =====================================================================
        
        # Status display frame
        status_frame = ttk.Frame(controls_frame)
        status_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Status label
        ttk.Label(status_frame, text="Status:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.status_var = tk.StringVar(value="Ready to start test")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                font=('Arial', 10), foreground='blue')
        status_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Current test display frame
        current_test_frame = ttk.Frame(controls_frame)
        current_test_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Current test label
        ttk.Label(current_test_frame, text="Current Test:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.current_test_var = tk.StringVar(value="None")
        current_test_label = ttk.Label(current_test_frame, textvariable=self.current_test_var, 
                                      font=('Arial', 10), foreground='purple')
        current_test_label.pack(anchor=tk.W, pady=(5, 0))
        
        # =====================================================================
        # PROGRESS DISPLAY SECTION
        # =====================================================================
        
        # Progress bar frame
        progress_frame = ttk.Frame(controls_frame)
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Progress label
        ttk.Label(progress_frame, text="Progress:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        # Progress bar container
        progress_container = ttk.Frame(progress_frame)
        progress_container.pack(fill=tk.X, pady=(5, 0))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_container, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Progress percentage label
        self.progress_label = ttk.Label(progress_container, text="0%", 
                                       font=('Arial', 10))
        self.progress_label.pack(side=tk.RIGHT)
        
        # =====================================================================
        # CONTROL BUTTONS SECTION
        # =====================================================================
        
        # Control buttons frame
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(fill=tk.X)
        
        # Start test button
        self.start_btn = ttk.Button(button_frame, text="▶️ Start Test", 
                                   command=self.start_test, 
                                   style='Accent.TButton')
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Stop test button
        self.stop_btn = ttk.Button(button_frame, text="⏹️ Stop Test", 
                                  command=self.stop_test, 
                                  state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh results button
        refresh_btn = ttk.Button(button_frame, text="🔄 Refresh Results", 
                               command=self.refresh_results)
        refresh_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear results button
        clear_btn = ttk.Button(button_frame, text="🧹 Clear Results", 
                              command=self.clear_results)
        clear_btn.pack(side=tk.LEFT)
        
        # =====================================================================
        # RESULTS DISPLAY SECTION
        # =====================================================================
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="📊 Results", padding=15)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Statistics frame
        stats_frame = ttk.Frame(results_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Working credentials count
        working_frame = ttk.Frame(stats_frame)
        working_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(working_frame, text="✅ Working:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.working_count = tk.StringVar(value="0")
        ttk.Label(working_frame, textvariable=self.working_count, 
                 font=('Arial', 12, 'bold'), foreground='green').pack(side=tk.LEFT, padx=(5, 0))
        
        # Failed credentials count
        failed_frame = ttk.Frame(stats_frame)
        failed_frame.pack(side=tk.LEFT, padx=(0, 20))
        
        ttk.Label(failed_frame, text="❌ Failed:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.failed_count = tk.StringVar(value="0")
        ttk.Label(failed_frame, textvariable=self.failed_count, 
                 font=('Arial', 12, 'bold'), foreground='red').pack(side=tk.LEFT, padx=(5, 0))
        
        # Total count
        total_frame = ttk.Frame(stats_frame)
        total_frame.pack(side=tk.LEFT)
        
        ttk.Label(total_frame, text="📋 Total:", 
                 font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.total_count = tk.StringVar(value="0")
        ttk.Label(total_frame, textvariable=self.total_count, 
                 font=('Arial', 12, 'bold'), foreground='blue').pack(side=tk.LEFT, padx=(5, 0))
        
        # =====================================================================
        # NOTEBOOK FOR RESULTS AND LOGS
        # =====================================================================
        
        # Create notebook for different result views
        notebook = ttk.Notebook(results_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Working credentials tab
        working_frame = ttk.Frame(notebook)
        notebook.add(working_frame, text="✅ Working Credentials")
        
        ttk.Label(working_frame, text="Successfully logged in credentials:", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        # Working credentials text area
        self.working_text = scrolledtext.ScrolledText(working_frame, height=8, 
                                                     font=('Consolas', 10), 
                                                     bg='#f0fff0')
        self.working_text.pack(fill=tk.BOTH, expand=True)
        
        # Failed credentials tab
        failed_frame = ttk.Frame(notebook)
        notebook.add(failed_frame, text="❌ Failed Credentials")
        
        ttk.Label(failed_frame, text="Failed login attempts:", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        # Failed credentials text area
        self.failed_text = scrolledtext.ScrolledText(failed_frame, height=8, 
                                                    font=('Consolas', 10), 
                                                    bg='#fff0f0')
        self.failed_text.pack(fill=tk.BOTH, expand=True)
        
        # Log tab
        log_frame = ttk.Frame(notebook)
        notebook.add(log_frame, text="📝 Live Log")
        
        ttk.Label(log_frame, text="Test progress and messages:", 
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=8, 
                                                 font=('Consolas', 9), 
                                                 bg='#f8f8f8', state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # =====================================================================
        # FOOTER SECTION
        # =====================================================================
        
        # Footer frame
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(15, 0))
        
        # Footer text
        self.footer_text = tk.StringVar(value="Ready - Select credentials file and click Start Test")
        footer_label = ttk.Label(footer_frame, textvariable=self.footer_text, 
                                font=('Arial', 9), foreground='gray')
        footer_label.pack(anchor=tk.W)

    def browse_file(self):
        """
        Browse for credentials file.
        
        This function opens a file dialog to allow the user to select
        a credentials file for testing.
        """
        filename = filedialog.askopenfilename(
            title="Select Credentials File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="credentials.txt"
        )
        if filename:
            self.file_var.set(filename)
            self.count_credentials()

    def count_credentials(self):
        """
        Count credentials in the selected file.
        
        This function reads the selected file and counts the number of
        valid credential entries, then updates the UI with this information.
        """
        try:
            filename = self.file_var.get()
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    lines = f.readlines()
                
                count = 0
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and ',' in line:
                        count += 1
                
                self.footer_text.set(f"Found {count} credentials in {os.path.basename(filename)}")
                self.total_count.set(str(count))
                
                # Show existing results summary
                self.show_existing_results_summary()
            else:
                self.footer_text.set("File not found")
                
        except Exception as e:
            self.footer_text.set(f"Error reading file: {str(e)}")

    def show_existing_results_summary(self):
        """
        Show summary of existing results when GUI starts.
        
        This function checks for existing result files and displays
        a summary of previously tested credentials.
        """
        try:
            working_count = 0
            failed_count = 0
            
            # Count working credentials
            if os.path.exists("working_credentials.txt"):
                with open("working_credentials.txt", "r", encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines[1:]:  # Skip header
                        if line.strip() and ',' in line:
                            working_count += 1
            
            # Count failed credentials
            if os.path.exists("not_working.txt"):
                with open("not_working.txt", "r", encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines[1:]:  # Skip header
                        if line.strip() and ',' in line:
                            failed_count += 1
            
            if working_count > 0 or failed_count > 0:
                summary = f"📊 Existing results: {working_count} working, {failed_count} failed"
                self.footer_text.set(summary)
                
                # Update counts in GUI
                self.working_count.set(str(working_count))
                self.failed_count.set(str(failed_count))
                
                # Refresh results display
                self.refresh_results()
                
        except Exception as e:
            print(f"Error showing existing results summary: {e}")

    def start_test(self):
        """
        Start the login test using the original script.
        
        This function validates the credentials file and starts the testing
        process in a background thread to prevent GUI freezing.
        """
        if self.test_running:
            return
        
        # Validate file
        filename = self.file_var.get()
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"Credentials file not found: {filename}")
            return
        
        # Update UI state
        self.test_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_var.set("Starting test...")
        
        # Clear previous results
        self.clear_results()
        
        # Count credentials for progress
        self.count_credentials()
        
        # Add log message
        self.add_log(f"Starting test with {filename}")
        self.add_log("Using original reliable method")
        
        # Start test in background thread
        self.test_thread = threading.Thread(target=self.run_test_background, daemon=True)
        self.test_thread.start()

    def stop_test(self):
        """
        Stop the running test.
        
        This function stops the currently running test process
        and updates the UI accordingly.
        """
        if not self.test_running:
            return
        
        self.test_running = False
        
        # Terminate the subprocess if running
        if self.test_process and self.test_process.poll() is None:
            self.test_process.terminate()
        
        # Update UI
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status_var.set("Test stopped by user")
        self.add_log("Test stopped by user")

    def run_test_background(self):
        """
        Run the original script in background.
        
        This function runs the main login_test.py script as a subprocess
        and monitors its output for real-time updates.
        """
        try:
            # Modify login_test.py to use the selected credentials file
            self.modify_original_script()
            
            # Start the original script
            self.test_process = subprocess.Popen(
                [sys.executable, "credential_tester.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor the process
            self.monitor_test_process()
            
        except Exception as e:
            self.message_queue.put(('error', f"Failed to start test: {str(e)}"))
            self.test_running = False

    def modify_original_script(self):
        """
        Temporarily modify the original script to use selected file.
        
        This function creates a backup of the original script and modifies
        it to use the selected credentials file.
        """
        # Read the original script
        with open("credential_tester.py", "r", encoding='utf-8') as f:
            content = f.read()
        
        # Create a backup
        with open("credential_tester_backup.py", "w", encoding='utf-8') as f:
            f.write(content)
        
        # Modify the credentials file path
        filename = self.file_var.get()
        modified_content = content.replace(
            'CREDENTIALS_FILE = "credentials.txt"',
            f'CREDENTIALS_FILE = "{filename}"'
        )
        
        # Write the modified version
        with open("credential_tester.py", "w", encoding='utf-8') as f:
            f.write(modified_content)

    def restore_original_script(self):
        """
        Restore the original script.
        
        This function restores the original script from the backup
        after the test is completed.
        """
        try:
            if os.path.exists("credential_tester_backup.py"):
                with open("credential_tester_backup.py", "r", encoding='utf-8') as f:
                    content = f.read()
                
                with open("credential_tester.py", "w", encoding='utf-8') as f:
                    f.write(content)
                
                os.remove("credential_tester_backup.py")
        except:
            pass

    def monitor_test_process(self):
        """
        Monitor the test process and update UI.
        
        This function monitors the subprocess output and updates the UI
        with real-time progress information.
        """
        total_creds = int(self.total_count.get() or 0)
        current_progress = 0
        
        try:
            # Read both stdout and stderr
            import select
            import sys
            
            while self.test_running and self.test_process.poll() is None:
                # Check for output from both stdout and stderr
                output_line = None
                
                # Try to read from stdout
                try:
                    line = self.test_process.stdout.readline()
                    if line:
                        output_line = line.strip()
                except:
                    pass
                
                # Try to read from stderr if no stdout
                if not output_line:
                    try:
                        line = self.test_process.stderr.readline()
                        if line:
                            output_line = line.strip()
                    except:
                        pass
                
                if output_line:
                    self.add_log(output_line)
                    
                    # Update progress based on log messages
                    if any(keyword in output_line.lower() for keyword in ["testing", "trying", "checking"]) and "@" in output_line:
                        current_progress += 1
                        progress_pct = (current_progress / total_creds * 100) if total_creds > 0 else 0
                        self.progress_var.set(progress_pct)
                        self.progress_label.config(text=f"{progress_pct:.1f}%")
                        self.status_var.set(f"Testing {current_progress}/{total_creds}")
                        
                        # Extract email from the line to show current test
                        if "@" in output_line:
                            email = output_line.split("@")[0].split()[-1] + "@" + output_line.split("@")[1].split()[0]
                            self.current_test_var.set(f"Testing: {email}")
                    
                    # Check for immediate save indicators
                    elif any(keyword in output_line.lower() for keyword in ["✅ success saved immediately", "❌ failed saved immediately"]):
                        self.add_log("💾 Result saved immediately - refreshing display...")
                        # Refresh results immediately when something is saved
                        self.refresh_results()
                        
                        # Clear current test display
                        self.current_test_var.set("Test completed")
                    
                    # Check for success indicators
                    elif any(keyword in output_line.lower() for keyword in ["success", "logged in", "navigator", "mail.com/mail"]):
                        self.add_log("✅ SUCCESS detected!")
                        self.refresh_results()
                    
                    # Check for failure indicators
                    elif any(keyword in output_line.lower() for keyword in ["failed", "error", "timeout", "not found"]):
                        self.add_log("❌ FAILURE detected")
                        self.refresh_results()
                    
                    # Check for completion of individual tests
                    elif "browser closed" in output_line.lower():
                        # Each test completed, refresh results
                        self.refresh_results()
                        # Clear current test display
                        self.current_test_var.set("Browser closed")
                
                time.sleep(0.1)
            
            # Process finished - read any remaining output
            try:
                remaining_stdout, remaining_stderr = self.test_process.communicate(timeout=5)
                if remaining_stdout:
                    for line in remaining_stdout.split('\n'):
                        if line.strip():
                            self.add_log(line.strip())
                if remaining_stderr:
                    for line in remaining_stderr.split('\n'):
                        if line.strip():
                            self.add_log(f"[ERROR] {line.strip()}")
            except:
                pass
            
            # Process finished
            return_code = self.test_process.poll()
            if return_code == 0:
                self.message_queue.put(('completed', "Test completed successfully"))
            else:
                self.message_queue.put(('completed', f"Test finished with code {return_code}"))
                
        except Exception as e:
            self.message_queue.put(('error', f"Error monitoring test: {str(e)}"))
        
        finally:
            self.test_running = False
            self.restore_original_script()

    def refresh_results(self):
        """
        Refresh and display results.
        
        This function reads the result files and updates the display
        with the latest results.
        """
        try:
            # Read working credentials
            working_count = 0
            working_lines = []
            
            if os.path.exists("working_credentials.txt"):
                with open("working_credentials.txt", "r", encoding='utf-8') as f:
                    content = f.read().strip()
                
                if content:
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and ',' in line and not line.lower().startswith('mail,pass'):
                            # Format: email,password,status or email,password
                            parts = line.split(',')
                            if len(parts) >= 2:
                                email = parts[0].strip()
                                password = parts[1].strip()
                                status = parts[2].strip() if len(parts) > 2 else "SUCCESS"
                                
                                if status.upper() in ["SUCCESS", "LOGGEDIN", "LOGGED IN"]:
                                    working_lines.append(f"✅ {email} : {password}")
                                    working_count += 1
            
            # Update working credentials display
            self.working_text.delete(1.0, tk.END)
            if working_lines:
                self.working_text.insert(1.0, '\n'.join(working_lines))
            else:
                self.working_text.insert(1.0, "No working credentials found yet.")
            
            # Read failed credentials
            failed_count = 0
            failed_lines = []
            
            if os.path.exists("not_working.txt"):
                with open("not_working.txt", "r", encoding='utf-8') as f:
                    content = f.read().strip()
                
                if content:
                    lines = content.split('\n')
                    for line in lines:
                        line = line.strip()
                        if line and ',' in line and not line.lower().startswith('mail,pass'):
                            # Format: email,password,status or email,password
                            parts = line.split(',')
                            if len(parts) >= 2:
                                email = parts[0].strip()
                                password = parts[1].strip()
                                status = parts[2].strip() if len(parts) > 2 else "FAILED"
                                
                                if status.upper() in ["FAILED", "ERROR", "TIMEOUT"]:
                                    failed_lines.append(f"❌ {email} : {status}")
                                    failed_count += 1
            
            # Update failed credentials display
            self.failed_text.delete(1.0, tk.END)
            if failed_lines:
                self.failed_text.insert(1.0, '\n'.join(failed_lines))
            else:
                self.failed_text.insert(1.0, "No failed credentials yet.")
            
            # Update counts
            self.working_count.set(str(working_count))
            self.failed_count.set(str(failed_count))
            
            # Update status
            if working_count > 0 or failed_count > 0:
                self.footer_text.set(f"Results: {working_count} working, {failed_count} failed")
                
            # Force GUI update
            self.root.update_idletasks()
            
        except Exception as e:
            self.add_log(f"Error refreshing results: {str(e)}")

    def clear_results(self):
        """
        Clear all results from the display.
        
        This function clears all result displays and resets counters.
        """
        self.working_text.delete(1.0, tk.END)
        self.failed_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        self.working_count.set("0")
        self.failed_count.set("0")
        self.progress_var.set(0)
        self.progress_label.config(text="0%")

    def add_log(self, message):
        """
        Add message to log display.
        
        Args:
            message: Message to add to the log
        """
        try:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_line = f"[{timestamp}] {message}\n"
            
            # Use thread-safe queue for log messages
            self.message_queue.put(('log', log_line))
        except:
            pass
    
    def add_log_direct(self, message):
        """
        Add message directly to log (thread-safe).
        
        Args:
            message: Message to add to the log
        """
        try:
            self.log_text.config(state=tk.NORMAL)
            self.log_text.insert(tk.END, message)
            self.log_text.see(tk.END)
            self.log_text.config(state=tk.DISABLED)
            
            # Force update
            self.root.update_idletasks()
        except:
            pass

    def process_messages(self):
        """
        Process messages from background threads.
        
        This function processes messages from the message queue
        and updates the UI accordingly.
        """
        try:
            while True:
                try:
                    msg_type, data = self.message_queue.get_nowait()
                    
                    if msg_type == 'error':
                        messagebox.showerror("Error", data)
                        self.start_btn.config(state=tk.NORMAL)
                        self.stop_btn.config(state=tk.DISABLED)
                        self.status_var.set("Error occurred")
                    elif msg_type == 'completed':
                        self.start_btn.config(state=tk.NORMAL)
                        self.stop_btn.config(state=tk.DISABLED)
                        self.status_var.set("Test completed")
                        self.add_log_direct(f"[{datetime.now().strftime('%H:%M:%S')}] {data}\n")
                        self.refresh_results()
                    elif msg_type == 'log':
                        self.add_log_direct(data)
                        
                except queue.Empty:
                    break
                    
        except Exception as e:
            print(f"Error processing messages: {e}")
        
        # Schedule next check
        self.root.after(200, self.process_messages)  # Check more frequently
    
    def periodic_refresh(self):
        """
        Periodically refresh results during testing.
        
        This function refreshes the results display periodically
        during testing to show real-time updates.
        """
        if self.test_running:
            self.refresh_results()
        
        # Schedule next refresh
        self.root.after(2000, self.periodic_refresh)  # Refresh every 2 seconds

# =============================================================================
# MAIN APPLICATION FUNCTION
# =============================================================================

def main():
    """
    Main function to start the GUI application.
    
    This function creates the main window, centers it on screen,
    and starts the GUI event loop.
    """
    # Create main window
    root = tk.Tk()
    app = SimpleLoginGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Set minimum size
    root.minsize(800, 600)
    
    try:
        # Start GUI event loop
        root.mainloop()
    except KeyboardInterrupt:
        pass

# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
