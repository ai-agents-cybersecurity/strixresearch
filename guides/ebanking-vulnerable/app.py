#!/usr/bin/env python3
"""
VULNERABLE E-BANKING APPLICATION FOR PENTESTING
===============================================
WARNING: This application is INTENTIONALLY VULNERABLE.
DO NOT deploy in production. For security testing only.

Vulnerabilities included:
1. SQL Injection (Authentication, Search)
2. Broken Authentication (Weak passwords, no MFA, predictable sessions)
3. IDOR (Insecure Direct Object Reference)
4. XSS (Cross-Site Scripting) - Stored and Reflected
5. CSRF (Cross-Site Request Forgery)
6. Sensitive Data Exposure
7. Business Logic Flaws (amount manipulation, negative transfers)
8. Insecure Direct API Access
9. Mass Assignment
10. Security Misconfiguration (debug mode, verbose errors)
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response, flash
import sqlite3
import hashlib
import secrets
import json
from datetime import datetime
import os

app = Flask(__name__)
# VULNERABILITY: Weak/known secret key
app.secret_key = 'test-bank-secret-key-12345'
app.config['DEBUG'] = True  # VULNERABILITY: Debug mode enabled

DATABASE = 'bank.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            email TEXT,
            full_name TEXT,
            phone TEXT,
            is_admin INTEGER DEFAULT 0,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Accounts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            account_number TEXT UNIQUE,
            account_type TEXT,
            balance REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_account INTEGER,
            to_account INTEGER,
            amount REAL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (from_account) REFERENCES accounts(id),
            FOREIGN KEY (to_account) REFERENCES accounts(id)
        )
    ''')
    
    # Messages table (for XSS demo)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT,
            content TEXT,
            from_user TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Cards table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            card_number TEXT,
            cvv TEXT,
            expiry TEXT,
            is_blocked INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Insert test data
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        # VULNERABILITY: Weak passwords, plaintext storage for some
        users = [
            ('admin', 'admin123', 'admin@securebank.com', 'Administrator', '555-0100', 1, 1000000.00),
            ('john_doe', 'password123', 'john@example.com', 'John Doe', '555-0101', 0, 5000.00),
            ('jane_smith', 'welcome1', 'jane@example.com', 'Jane Smith', '555-0102', 0, 12500.00),
            ('bob_wilson', 'qwerty', 'bob@example.com', 'Bob Wilson', '555-0103', 0, 2500.00),
            ('alice_jones', 'letmein', 'alice@example.com', 'Alice Jones', '555-0104', 0, 7800.00),
            ('test_user', 'test123', 'test@example.com', 'Test Account', '555-0105', 0, 1000.00),
        ]
        for u in users:
            cursor.execute('''
                INSERT INTO users (username, password, email, full_name, phone, is_admin, balance)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', u)
    
    # Create accounts for users
    cursor.execute("SELECT * FROM accounts")
    if not cursor.fetchone():
        accounts = [
            (1, '1000000001', 'Checking', 1000000.00),
            (1, '1000000002', 'Savings', 5000000.00),
            (2, '1000000003', 'Checking', 5000.00),
            (2, '1000000004', 'Savings', 15000.00),
            (3, '1000000005', 'Checking', 12500.00),
            (4, '1000000006', 'Checking', 2500.00),
            (5, '1000000007', 'Checking', 7800.00),
            (6, '1000000008', 'Checking', 1000.00),
        ]
        for a in accounts:
            cursor.execute('''
                INSERT INTO accounts (user_id, account_number, account_type, balance)
                VALUES (?, ?, ?, ?)
            ''', a)
    
    # Create some cards
    cursor.execute("SELECT * FROM cards")
    if not cursor.fetchone():
        cards = [
            (1, '4532123456789012', '123', '12/26'),
            (2, '4532123456789013', '456', '11/25'),
            (3, '4532123456789014', '789', '10/26'),
        ]
        for c in cards:
            cursor.execute('''
                INSERT INTO cards (user_id, card_number, cvv, expiry)
                VALUES (?, ?, ?, ?)
            ''', c)
    
    # Create sample transactions
    cursor.execute("SELECT * FROM transactions")
    if not cursor.fetchone():
        transactions = [
            (3, 4, 500.00, 'Payment for dinner'),
            (4, 3, 250.00, 'Rent split'),
            (2, 3, 1000.00, 'Consulting fee'),
            (5, 2, 150.00, 'Gift'),
        ]
        for t in transactions:
            cursor.execute('''
                INSERT INTO transactions (from_account, to_account, amount, description)
                VALUES (?, ?, ?, ?)
            ''', t)
    
    # Create XSS demo message
    cursor.execute("SELECT * FROM messages WHERE subject='Welcome!'")
    if not cursor.fetchone():
        messages = [
            (2, 'Welcome!', 'Welcome to SecureBank! Your account is now active.', 'System'),
            (2, 'Statement Available', 'Your monthly statement is ready for review.', 'System'),
            (3, 'Security Alert', 'New login detected from IP 192.168.1.1', 'Security'),
            (2, 'Loan Offer', '<script>alert("XSS")</script>Special offer!', 'Marketing'),  # Stored XSS
        ]
        for m in messages:
            cursor.execute('''
                INSERT INTO messages (user_id, subject, content, from_user)
                VALUES (?, ?, ?, ?)
            ''', m)
    
    conn.commit()
    conn.close()

# VULNERABILITY: SQL Injection in login
def check_login_sql_injection(username, password):
    conn = get_db()
    cursor = conn.cursor()
    # VULNERABILITY: String concatenation in SQL query
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

# "Secure" login (still vulnerable to other attacks)
def check_login_secure(username, password):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

@app.route('/')
def index():
    return render_template('index.html')

# VULNERABILITY: Multiple login methods - one is vulnerable to SQLi
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        login_type = request.form.get('login_type', 'legacy')  # Hidden parameter
        
        # VULNERABILITY: Can switch between secure and insecure login
        if login_type == 'legacy':
            user = check_login_sql_injection(username, password)
        else:
            user = check_login_secure(username, password)
        
        if user:
            # VULNERABILITY: Predictable session IDs, no MFA
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            session['session_token'] = hashlib.md5(f"{user['id']}{datetime.now()}".encode()).hexdigest()[:16]
            
            # VULNERABILITY: Insecure cookie settings
            resp = redirect(url_for('dashboard'))
            resp.set_cookie('user_id', str(user['id']), httponly=False)  # No HttpOnly
            resp.set_cookie('session', session['session_token'], httponly=False, secure=False)
            return resp
        else:
            # VULNERABILITY: User enumeration through error messages
            cursor = get_db().cursor()
            cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
            if cursor.fetchone():
                error = "Invalid password"
            else:
                error = "Username not found"
            return render_template('login.html', error=error)
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        
        conn = get_db()
        cursor = conn.cursor()
        
        # VULNERABILITY: No input validation, mass assignment possible
        try:
            # VULNERABILITY: SQL Injection possible here too
            query = f"""
                INSERT INTO users (username, password, email, full_name, phone, balance)
                VALUES ('{username}', '{password}', '{email}', '{full_name}', '{phone}', 0.0)
            """
            cursor.execute(query)
            conn.commit()
            
            # Create default account
            user_id = cursor.lastrowid
            account_num = f"100000{user_id:04d}"
            cursor.execute('''
                INSERT INTO accounts (user_id, account_number, account_type, balance)
                VALUES (?, ?, 'Checking', 0.0)
            ''', (user_id, account_num))
            conn.commit()
            
            flash('Account created successfully!')
            return redirect(url_for('login'))
        except Exception as e:
            # VULNERABILITY: Verbose error messages
            return render_template('register.html', error=f"Registration failed: {str(e)}")
        finally:
            conn.close()
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user info
    cursor.execute("SELECT * FROM users WHERE id=?", (session['user_id'],))
    user = cursor.fetchone()
    
    # Get accounts
    cursor.execute("SELECT * FROM accounts WHERE user_id=?", (session['user_id'],))
    accounts = cursor.fetchall()
    
    # Get recent transactions
    cursor.execute('''
        SELECT t.*, a1.account_number as from_acc_num, a2.account_number as to_acc_num
        FROM transactions t
        LEFT JOIN accounts a1 ON t.from_account = a1.id
        LEFT JOIN accounts a2 ON t.to_account = a2.id
        WHERE a1.user_id=? OR a2.user_id=?
        ORDER BY t.created_at DESC LIMIT 10
    ''', (session['user_id'], session['user_id']))
    transactions = cursor.fetchall()
    
    # Get messages (XSS demo)
    cursor.execute("SELECT * FROM messages WHERE user_id=? ORDER BY created_at DESC", (session['user_id'],))
    messages = cursor.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', user=user, accounts=accounts, 
                         transactions=transactions, messages=messages)

# VULNERABILITY: IDOR - can access any account by changing the ID
@app.route('/account/<int:account_id>')
def account_detail(account_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # VULNERABILITY: No authorization check - any logged-in user can view any account
    cursor.execute("SELECT * FROM accounts WHERE id=?", (account_id,))
    account = cursor.fetchone()
    
    if account:
        # Get all transactions for this account
        cursor.execute('''
            SELECT t.*, a1.account_number as from_acc_num, a2.account_number as to_acc_num
            FROM transactions t
            LEFT JOIN accounts a1 ON t.from_account = a1.id
            LEFT JOIN accounts a2 ON t.to_account = a2.id
            WHERE t.from_account=? OR t.to_account=?
            ORDER BY t.created_at DESC
        ''', (account_id, account_id))
        transactions = cursor.fetchall()
        
        conn.close()
        return render_template('account.html', account=account, transactions=transactions)
    
    conn.close()
    return "Account not found", 404

# VULNERABILITY: CSRF - no token validation
@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get user's accounts
    cursor.execute("SELECT * FROM accounts WHERE user_id=?", (session['user_id'],))
    accounts = cursor.fetchall()
    
    if request.method == 'POST':
        from_account_id = request.form.get('from_account')
        to_account_number = request.form.get('to_account')
        amount = float(request.form.get('amount', 0))
        description = request.form.get('description', '')
        
        # VULNERABILITY: No CSRF token check
        # VULNERABILITY: Business logic flaw - negative amounts
        # VULNERABILITY: Race condition possible
        
        cursor.execute("SELECT * FROM accounts WHERE id=?", (from_account_id,))
        from_acc = cursor.fetchone()
        
        # VULNERABILITY: IDOR - can use any account as source
        if from_acc:
            cursor.execute("SELECT * FROM accounts WHERE account_number=?", (to_account_number,))
            to_acc = cursor.fetchone()
            
            if to_acc:
                # VULNERABILITY: No transaction logging, no verification
                # VULNERABILITY: Amount manipulation possible (negative, overflow)
                new_from_balance = from_acc['balance'] - amount
                new_to_balance = to_acc['balance'] + amount
                
                cursor.execute("UPDATE accounts SET balance=? WHERE id=?", (new_from_balance, from_acc['id']))
                cursor.execute("UPDATE accounts SET balance=? WHERE id=?", (new_to_balance, to_acc['id']))
                
                # Record transaction
                cursor.execute('''
                    INSERT INTO transactions (from_account, to_account, amount, description)
                    VALUES (?, ?, ?, ?)
                ''', (from_acc['id'], to_acc['id'], amount, description))
                
                conn.commit()
                flash(f'Transfer of ${amount} completed!')
                return redirect(url_for('dashboard'))
            else:
                error = "Destination account not found"
        else:
            error = "Source account not found"
        
        conn.close()
        return render_template('transfer.html', accounts=accounts, error=error)
    
    conn.close()
    return render_template('transfer.html', accounts=accounts)

# VULNERABILITY: Reflected XSS
@app.route('/search')
def search():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    query = request.args.get('q', '')
    
    # VULNERABILITY: Reflected XSS - query is not escaped
    # VULNERABILITY: SQL Injection in search
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(f"""
            SELECT * FROM transactions 
            WHERE description LIKE '%{query}%' 
            ORDER BY created_at DESC
        """)
        results = cursor.fetchall()
    except Exception as e:
        results = []
        error = str(e)  # VULNERABILITY: Verbose error
    finally:
        conn.close()
    
    return render_template('search.html', query=query, results=results)

# VULNERABILITY: Stored XSS through message composition
@app.route('/message', methods=['POST'])
def send_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    to_user = request.form.get('to_user')
    subject = request.form.get('subject')
    content = request.form.get('content')
    
    conn = get_db()
    cursor = conn.cursor()
    
    # VULNERABILITY: Find user by username (info disclosure)
    cursor.execute(f"SELECT id FROM users WHERE username='{to_user}'")
    recipient = cursor.fetchone()
    
    if recipient:
        # VULNERABILITY: No input sanitization - XSS possible
        cursor.execute('''
            INSERT INTO messages (user_id, subject, content, from_user)
            VALUES (?, ?, ?, ?)
        ''', (recipient['id'], subject, content, session['username']))
        conn.commit()
        flash('Message sent!')
    else:
        flash('User not found')
    
    conn.close()
    return redirect(url_for('dashboard'))

# VULNERABILITY: Admin panel with broken access control
@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # VULNERABILITY: Client-side authorization check (can be bypassed)
    # The real check is commented out for "debugging"
    # if not session.get('is_admin'):
    #     return "Access denied", 403
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    cursor.execute('''
        SELECT t.*, a1.account_number as from_acc, a2.account_number as to_acc
        FROM transactions t
        LEFT JOIN accounts a1 ON t.from_account = a1.id
        LEFT JOIN accounts a2 ON t.to_account = a2.id
        ORDER BY t.created_at DESC
    ''')
    all_transactions = cursor.fetchall()
    
    conn.close()
    
    return render_template('admin.html', users=users, transactions=all_transactions)

# VULNERABILITY: API with no authentication/authorization
@app.route('/api/users')
def api_users():
    # VULNERABILITY: No API authentication
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, full_name, phone, balance FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(users)

@app.route('/api/user/<int:user_id>')
def api_user(user_id):
    # VULNERABILITY: No authentication, IDOR
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify(dict(user))
    return jsonify({"error": "User not found"}), 404

@app.route('/api/accounts')
def api_accounts():
    # VULNERABILITY: Returns all accounts, no auth
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts")
    accounts = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(accounts)

# VULNERABILITY: Sensitive data exposure
@app.route('/api/cards')
def api_cards():
    # VULNERABILITY: No authentication, exposes sensitive card data
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards")
    cards = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(cards)

# VULNERABILITY: Mass assignment - can update any field
@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({"error": "Not logged in"}), 401
    
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # VULNERABILITY: Mass assignment - can update any column including is_admin, balance
    for key, value in data.items():
        cursor.execute(f"UPDATE users SET {key}=? WHERE id=?", (value, session['user_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Profile updated"})

# VULNERABILITY: Debug/backup endpoints exposed
@app.route('/debug')
def debug_info():
    # VULNERABILITY: Information disclosure
    info = {
        "app_config": {
            "debug": app.config['DEBUG'],
            "secret_key": app.secret_key,
            "database": DATABASE,
        },
        "request_headers": dict(request.headers),
        "session": dict(session),
        "environment": dict(os.environ)
    }
    return jsonify(info)

@app.route('/backup/<path:filename>')
def backup(filename):
    # VULNERABILITY: Path traversal
    try:
        with open(f"/home/spider/Desktop/ebanking/{filename}", 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/logout')
def logout():
    session.clear()
    resp = redirect(url_for('index'))
    resp.set_cookie('user_id', '', expires=0)
    resp.set_cookie('session', '', expires=0)
    return resp

# VULNERABILITY: Password reset with insecure token generation
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM users WHERE email='{email}'")
        user = cursor.fetchone()
        
        if user:
            # VULNERABILITY: Predictable reset token
            token = hashlib.md5(f"{user['id']}reset".encode()).hexdigest()[:8]
            # VULNERABILITY: Token exposed in response
            return render_template('forgot_password.html', 
                                 message=f"Reset token for {email}: {token}")
        else:
            # VULNERABILITY: User enumeration
            return render_template('forgot_password.html', error="Email not found")
        
        conn.close()
    
    return render_template('forgot_password.html')

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # VULNERABILITY: No token expiration
    conn = get_db()
    cursor = conn.cursor()
    
    # Find user by "verifying" token (insecure)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    
    target_user = None
    for user in users:
        expected_token = hashlib.md5(f"{user['id']}reset".encode()).hexdigest()[:8]
        if expected_token == token:
            target_user = user
            break
    
    if not target_user:
        return "Invalid token", 400
    
    if request.method == 'POST':
        new_password = request.form.get('password')
        cursor.execute(f"UPDATE users SET password='{new_password}' WHERE id={target_user['id']}")
        conn.commit()
        conn.close()
        return "Password updated successfully"
    
    conn.close()
    return render_template('reset_password.html', token=token)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
