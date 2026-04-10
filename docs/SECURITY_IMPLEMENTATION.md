# Secure CR Election System (Phase 3)
**Team Name:** VoteGuardian  
**Lead:** Raveeha Naseem  
**Focus:** Secure Implementation & DevSecOps Integration

---

## Project Overview
This project is a secure web-based voting application for CR elections, built with a "Security-by-Design" approach. We have implemented robust defenses against common web vulnerabilities and integrated an automated security pipeline.

## Security Features (Mitigations)

### 1. IDOR Protection (Insecure Direct Object Reference)
- **Problem:** Users could view others' ballots by changing the ID in the URL.
- **Solution:** Implemented **Scoped Queries**. Every database request now validates the `ballot_id` against the active `session['user_id']`.
- **Result:** `403 Forbidden` error if unauthorized access is attempted.

### 2. CSRF Defense (Cross-Site Request Forgery)
- **Problem:** Malicious sites could trick a logged-in user into casting a vote.
- **Solution:** Integrated `Flask-WTF` middleware. Every POST request requires a unique, server-validated CSRF token.

### 3. Clickjacking Prevention
- **Problem:** Attacker could overlay our voting page in an invisible iframe.
- **Solution:** Implemented security headers (`X-Frame-Options: DENY`) globally to prevent the site from being framed.

### 4. Secure Audit Logging
- **Problem:** Maintaining election integrity while protecting voter privacy.
- **Solution:** - Automated SHA-256 Hashing of User IDs.
  - Persistent logging to `audit_log.txt`.
  - Custom filters to log only critical "AUDIT" events.

---

## CI/CD Pipeline (DevSecOps)
We have integrated an automated security scanner using **GitHub Actions** and **Bandit**.
- **Trigger:** Automated scan on every `git push`.
- **Function:** Scans the entire codebase for security debt and vulnerabilities.
- **Status:** Integrated into Phase 3 Implementation.

---

## Repository Structure
```text
├── .github/workflows/    # CI/CD (Bandit SAST Scan)
├── app/                  # Application Logic
├── docs/                 # Documentation & Reports
├── audit_log.txt         # Secure Hashed Logs
├── app.py                # Entry Point
└── requirements.txt      # Dependencies