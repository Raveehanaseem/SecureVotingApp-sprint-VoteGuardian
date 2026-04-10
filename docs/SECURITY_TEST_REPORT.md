# Secure Voting App – Phase 4  
### Security Hardening, Audit Logging, and Security Testing (SAST & DAST)

---

## Project Overview

The Secure Voting Application is a Flask-based web system designed to provide a secure, privacy-focused, and tamper-resistant voting platform.

Phase 4 focuses on:

- Security hardening  
- Audit logging  
- Secure session handling  
- Protection against common web vulnerabilities  
- Security testing (SAST & DAST validation)

---

## Key Objectives

- Ensure user session privacy and integrity  
- Secure storage of votes in a database  
- Maintain complete audit trails for all actions  
- Mitigate common web vulnerabilities (XSS, CSRF, clickjacking)  
- Enforce strict security headers and CSP policies  
- Validate security using SAST and DAST testing tools  

---

## Features Implemented in Phase 4

---

### 1. Session Management

- Each user is assigned a unique `user_id` per session  
- Secure cookie configuration:
  - Secure  
  - HttpOnly  
  - SameSite=Lax  

---

### 2. Audit Logging

All voting activity is recorded in `audit_log.txt`.

**Log Format:**

timestamp - AUDIT: User [Hash: abc123...] voted. Ballot ID: 1


- User identity is hashed for privacy protection  
- Logs are append-only to preserve integrity  

---

### 3. Content Security Policy (CSP)

CSP is implemented to reduce XSS attack risks:


default-src 'self';
script-src 'self';
style-src 'self' 'unsafe-inline';
img-src 'self' data:;
object-src 'none';
frame-ancestors 'none';


---

### 4. Security Headers

- X-Frame-Options: DENY  
- X-Content-Type-Options: nosniff  
- X-XSS-Protection: 1; mode=block  
- Referrer-Policy: no-referrer  
- Permissions-Policy: geolocation=(), camera=()  

**Cross-Origin Policies:**
- Cross-Origin-Embedder-Policy: require-corp  
- Cross-Origin-Opener-Policy: same-origin  
- Cross-Origin-Resource-Policy: same-origin  

**Server Header:**

Server: SecureServer


---

### 5. CSRF Protection

- Implemented using Flask-WTF CSRFProtect  
- Protects all POST requests from unauthorized submissions  

---

### 6. Database

- SQLite database: `voting.db`  
- Located in `instance/` directory  

**Ballot Table Schema:**
- id → Primary key  
- user_id → Session-based identifier  
- vote → Selected candidate/option  

---

## Project Structure


online-voting-app/
│
├── app/
│ ├── init.py
│ ├── routes.py
│ ├── models.py
│ ├── templates/
│ │ ├── vote.html
│ │ └── thank_you.html
│ └── static/
│
├── instance/
│ └── voting.db
│
├── audit_log.txt
├── requirements.txt
├── venv/
└── README.md


---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo_url>
cd online-voting-app


2. Create Virtual Environment


python3 -m venv venv
source venv/bin/activate

Windows:

venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt


4. Set Flask Environment Variables

Linux/macOS:

export FLASK_APP=app
export FLASK_ENV=development

Windows (PowerShell):

set FLASK_APP=app
set FLASK_ENV=development


5. Initialize Database

flask shell

Then:

from app import db
db.create_all()
exit()


6. Run the Application
flask run

Open in browser:

http://127.0.0.1:5000/

Security Hardening Notes

Votes are securely stored and cannot be modified by the client
CSRF protection is enabled for all POST requests
Inline styles are temporarily allowed (unsafe-inline) but should be removed in production
External CDN resources should include Subresource Integrity (SRI)
Cookies are configured for HTTPS-ready deployment
Known Security Findings (SAST & DAST)
CSP allows inline styles (unsafe-inline)
Missing Subresource Integrity (SRI) for external assets
Cookies less secure in HTTP development environment
Server header exposure masked as SecureServer
Phase 4 Deliverables
Fully functional Flask voting system
Secure session management
Audit logging with hashed identifiers
CSP + security headers implementation
CSRF protection enabled
SQLite database integration
Security testing (SAST & DAST validation)
Next Phase Improvements
Remove inline styles and implement CSP nonces
Add Subresource Integrity (SRI) for external resources
Deploy application over HTTPS
Implement user authentication system
Add Role-Based Access Control (RBAC)
Strengthen security testing pipeline (CI/CD with SAST + DAST)
Author

Abdul Wadood
Secure Voting System Project
Phase 4: Security Hardening, Audit Logging, and Security Testing (SAST & DAST)
