apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest flask requests

    mkdir -p /home/user/app

    cat << 'EOF' > /home/user/app/app.py
from flask import Flask, request, jsonify, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'super_secret_incident_key'
DB_PATH = 'users.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT,
                    is_admin INTEGER,
                    bio TEXT
                 )''')
    c.execute("INSERT INTO users (username, password, is_admin, bio) VALUES ('investigator', 'unknown_long_random_password', 0, 'Standard user')")
    conn.commit()
    conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '')
    password = data.get('password', '')

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Vulnerability 1: SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    try:
        c.execute(query)
        user = c.fetchone()
    except:
        return jsonify({"error": "Database error"}), 500
    finally:
        conn.close()

    if user:
        session['user_id'] = user[0]
        session['username'] = user[1]
        session['is_admin'] = user[3]
        return jsonify({"message": "Logged in successfully"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Vulnerability 2: Mass Assignment / Privilege Escalation
    for key, value in data.items():
        if key in ['bio', 'is_admin']:
            c.execute(f"UPDATE users SET {key} = ? WHERE id = ?", (value, session['user_id']))
            if key == 'is_admin':
                session['is_admin'] = value # Update session

    conn.commit()
    conn.close()
    return jsonify({"message": "Profile updated"})

@app.route('/admin/flag', methods=['GET'])
def get_flag():
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({"error": "Admin access required"}), 403

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT bio FROM users WHERE id = ?", (session['user_id'],))
    bio = c.fetchone()[0]
    conn.close()

    # Vulnerability 3 Simulation: Checking for injected XSS payload
    if '<script>' in bio and '</script>' in bio:
        return jsonify({"flag": "FLAG{inc1d3nt_r3sp0ns3_ch41n_m4st3r}"})
    else:
        return jsonify({"error": "Admin checks failed. No XSS payload detected in bio."}), 400

if __name__ == '__main__':
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host='127.0.0.1', port=5000)
EOF

    cd /home/user/app
    python3 -c "import app; app.init_db()"

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user