# 🛡️ Beginner Cybersecurity Mini‑Projects

This repository is an **improved fork** of an existing cybersecurity learning project.  
I forked the original work to expand it, modernize certain components, fix issues, and add new features — especially within the keylogger project — while continuing to learn through hands‑on practice.

The goal of this collection is to explore fundamental cybersecurity concepts through small, focused projects ranging from cryptography to network analysis and web vulnerabilities.

Each directory represents an independent mini‑project, and some are implemented in multiple programming languages for learning purposes.

---

## 📚 Project Overview

| Project | Description |
|--------|-------------|
| **RSA Algorithm** | A from‑scratch implementation of the RSA encryption algorithm (key generation, encryption, decryption). |
| **Keylogger (Educational)** | An enhanced version of the original keylogger: added encryption, legal warning, time‑limit, secure email handling, and improved structure. Designed strictly for educational and defensive understanding. |
| **Network Sniffer** | A simple network scanner that identifies devices on the local network (IP + MAC address). |
| **Phishing Pages** | A pedagogical phishing simulation demonstrating social engineering risks. Credentials entered are logged locally. |
| **Steganography** | LSB steganography implemented using the Python `stegano` library. |
| **SSTI** | A demonstration of Server‑Side Template Injection using Flask, showing how template engines can be exploited. |

---

## 🔐 Major Update: Educational Keylogger Improvements

As part of this fork, the **Keylogger** project received a complete overhaul.

### ✔️ Improvements Added

#### 🔒 Security
- Log encryption using **Fernet (AES)**
- Secure email sending via **SMTP_SSL**
- Automatic deletion of the log file after sending

#### ⚖️ Legal & Ethical Compliance
- Mandatory legal warning at startup
- Explicit user confirmation required
- Clear reminders about legal restrictions

#### 🧠 Functional Enhancements
- Timestamping of every keystroke
- Full handling of special keys
- Configurable runtime limit
- Centralized configuration dictionary (`CONFIG`)

#### 🧹 Code Quality
- Modular structure
- Better error handling
- Clear documentation and comments

---

## 🎯 Learning Objectives

This fork aims to strengthen understanding of:

- Offensive and defensive cybersecurity mechanisms  
- Common vulnerabilities and how they work  
- Network analysis and monitoring  
- Cryptography fundamentals  
- Python scripting for security  
- Building a credible cybersecurity portfolio  

---

## ⚠️ Legal Disclaimer

Some projects in this repository (keylogger, phishing, SSTI, etc.) involve sensitive concepts.  
They are provided **strictly for educational purposes**.

> **Using these tools on any system without explicit consent is illegal.**  
> Both the original author and the maintainer of this fork disclaim any responsibility for misuse.

---

## 🛠️ Installation

Clone the repository *(bash)*  
Navigate into the project directory *(bash)*  
Install dependencies *(bash)*  

---

## 🧪 Running the Projects

Run any project independently *(bash)*  

---

## 📝 Git Commit Convention

Recommended commit message for the keylogger update *(bash)*  

Full workflow *(bash)*  

---

## 📌 Possible Future Enhancements

- Add unit tests  
- Build a simple IDS/IPS  
- Implement an educational brute‑forcer  
- Add a hash‑collision demonstration  
- Create a small local SIEM  

---
