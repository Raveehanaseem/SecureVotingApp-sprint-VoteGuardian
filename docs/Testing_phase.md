# Secure Voting App - Phase 4

This is **Phase 4** of the Secure Voting Application built with Flask, focusing on **security hardening** and **audit logging**.

---

## **Project Overview**

A secure web application for casting votes while ensuring:

- User session privacy
- Secure storage of votes
- Audit logging for all vote activity
- Defense against common web vulnerabilities
- Secure HTTP headers and Content Security Policy (CSP)

---

## **Features Implemented in Phase 4**

1. **Session Management**
   - Unique `user_id` generated per session
   - Cookies configured with:
     - `Secure`  
     - `HttpOnly`  
     - `SameSite=Lax`

2. **Audit Logging**
   - All votes are logged in `audit_log.txt` with hashed user identifiers
   - Log format:  
     ```
     timestamp - AUDIT: User [Hash: abc123...] voted. Ballot ID: 1
     ```

3. **Content Security Policy (CSP)**
   - Prevents XSS attacks
   - Restricts resource loading:
     - `default-src 'self'`
     - `script-src 'self'`
     - `style-src 'self' 'unsafe-inline'` (to be fixed later with nonces)
     - `img-src 'self' data:`
     - `object-src 'none'`
     - `frame-ancestors 'none'`

4. **Security Headers**
   - `X-Frame-Options: DENY`
   - `X-Content-Type-Options: nosniff`
   - `X-XSS-Protection: 1; mode=block`
   - `Referrer-Policy: no-referrer`
   - `Permissions-Policy: geolocation=(), camera=()`
   - Cross-Origin policies:
     - `Cross-Origin-Embedder-Policy: require-corp`
     - `Cross-Origin-Opener-Policy: same-origin`
     - `Cross-Origin-Resource-Policy: same-origin`
   - Server header masked: `Server: SecureServer`

5. **CSRF Protection**
   - Implemented using **Flask-WTF CSRFProtect**

6. **Database**
   - SQLite database (`voting.db`)
   - Model: `Ballot` table with `id`, `user_id`, `vote` fields

---

## **Project Structure**


online-voting-app/
│
├─ app/
│ ├─ init.py # App factory and security headers
│ ├─ routes.py # Flask routes for voting
│ ├─ models.py # Database models
│ ├─ templates/
│ │ ├─ vote.html # Voting form
│ │ └─ thank_you.html
│ └─ static/ # CSS/JS files
│
├─ venv/ # Virtual environment
├─ audit_log.txt # Vote audit log
├─ instance/
│ └─ voting.db # SQLite database
├─ requirements.txt
└─ README.md


---

## **Setup Instructions**

1. Clone the repository:

```bash
git clone <repo_url>
cd online-voting-app
Create and activate virtual environment:
python3 -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows
Install dependencies:
pip install -r requirements.txt
Set Flask environment variables:
export FLASK_APP=app
export FLASK_ENV=development
Initialize the database:
flask shell
>>> from app import db
>>> db.create_all()
>>> exit()
Run the application:
flask run
Visit http://127.0.0.1:5000/ in your browser.
Security Hardening Notes
All votes are stored securely and cannot be modified by the client
CSRF is enabled for all POST requests
Inline styles are still allowed (unsafe-inline), to be replaced by CSP nonces in future updates
External CDN scripts/styles should include SRI (Subresource Integrity)
Cookies are secured for HTTPS deployment
Known Warnings / Notes
ZAP Scan Warnings (Phase 4) observed:
Server header leak (Server: SecureServer) — masked already
CSP inline styles (unsafe-inline) — recommended to replace with nonces
Subresource Integrity missing for CDN assets
Cookie Slack detected for local HTTP — resolved in HTTPS

These are mostly warnings, not vulnerabilities, but should be addressed for production deployment.

Phase 4 Deliverables
Fully running Flask app with secure vote casting
Audit logging of votes with hashed identifiers
Security headers and CSP implemented
CSRF protection enabled
SQLite database for storing ballots
Next Steps (Future Phases)
Remove all inline styles and implement CSP nonces
Add Subresource Integrity (SRI) for all external scripts
Deploy over HTTPS for production to enforce secure cookies
Implement user authentication for multi-session tracking

Author: Abdul Wadood
Project Phase: 4 - Security Hardening & Audit Logging
