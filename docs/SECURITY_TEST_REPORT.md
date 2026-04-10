# Secure Voting App - Phase 4

This is Phase 4 of the Secure Voting Application built with Flask, focusing on security hardening and audit logging.

---

## Project Overview

A secure web application for casting votes while ensuring:

- User session privacy  
- Secure storage of votes  
- Audit logging for all vote activity  
- Defense against common web vulnerabilities  
- Secure HTTP headers and Content Security Policy (CSP)  

---

## Features Implemented in Phase 4

### Session Management

- Unique `user_id` generated per session  
- Cookies configured with:
  - Secure  
  - HttpOnly  
  - SameSite=Lax  

---

### Audit Logging

- All votes are logged in `audit_log.txt` with hashed user identifiers  

Log format:

timestamp - AUDIT: User [Hash: abc123...] voted. Ballot ID: 1


---

### Content Security Policy (CSP)

- Prevents XSS attacks  
- Restricts resource loading:


default-src 'self'
script-src 'self'
style-src 'self' 'unsafe-inline'
img-src 'self' data:
object-src 'none'
frame-ancestors 'none'


---

### Security Headers

- X-Frame-Options: DENY  
- X-Content-Type-Options: nosniff  
- X-XSS-Protection: 1; mode=block  
- Referrer-Policy: no-referrer  
- Permissions-Policy: geolocation=(), camera=()  

Cross-Origin Policies:
- Cross-Origin-Embedder-Policy: require-corp  
- Cross-Origin-Opener-Policy: same-origin  
- Cross-Origin-Resource-Policy: same-origin  

Server Header:

Server: SecureServer


---

### CSRF Protection

- Implemented using Flask-WTF CSRFProtect  
- Enabled for all POST requests  

---

### Database

- SQLite database (`voting.db`)  
- Model: Ballot table with:
  - id  
  - user_id  
  - vote  

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
├── venv/
├── audit_log.txt
├── instance/
│ └── voting.db
├── requirements.txt
└── README.md


---

## Setup Instructions

### 1. Clone the repository


```bash
git clone https://github.com/Raveehanaseem/SecureVotingApp-sprint-VoteGuardian
cd online-voting-app


2. Create and activate virtual environment


python3 -m venv venv
source venv/bin/activate
venv\Scripts\activate


3. Install dependencies
pip install -r requirements.txt


4. Set Flask environment variables
export FLASK_APP=app
export FLASK_ENV=development


5. Initialize the database
flask shell
from app import db
db.create_all()
exit()
6. Run the application


flask run

Visit: http://127.0.0.1:5000/

Security Hardening Notes
All votes are stored securely and cannot be modified by the client
CSRF protection is enabled for all POST requests
Inline styles are currently allowed (unsafe-inline) and should be removed later
External CDN scripts/styles should include Subresource Integrity (SRI)
Cookies are configured for secure HTTPS deployment
Known Warnings / Notes

ZAP Scan Warnings (Phase 4):

Server header leak masked using Server: SecureServer
CSP allows inline styles (unsafe-inline)
Subresource Integrity missing for CDN assets
Cookie Slack warning due to HTTP environment

These are warnings, not critical vulnerabilities, but should be addressed for production.

Phase 4 Deliverables
Fully running Flask app with secure vote casting
Audit logging with hashed identifiers
Security headers and CSP implemented
CSRF protection enabled
SQLite database integration
Next Steps
Remove inline styles and implement CSP nonces
Add Subresource Integrity (SRI) for external resources
Deploy application over HTTPS
Implement user authentication
Author

Abdul Wadood
Project Phase: 4 - Security Hardening and Audit Logging
