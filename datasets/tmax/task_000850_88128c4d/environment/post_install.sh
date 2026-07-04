apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest cryptography flask

mkdir -p /home/user/app
mkdir -p /home/user/evidence

# 1. /home/user/app/server.py
cat << 'EOF' > /home/user/app/server.py
from flask import Flask, request, make_response
from cryptography.fernet import Fernet
import sqlite3

app = Flask(__name__)

# Hardcoded secret key for session management (bad practice)
APP_SECRET_KEY = b'xL_4kP9qR2aT8vN5mC7wJ1sY6zH3bF0dG9eK2uM8oYI='
fernet = Fernet(APP_SECRET_KEY)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Vulnerability 1: SQL Injection (CWE-89)
    cursor.execute(f"SELECT username FROM users WHERE id = {user_id}")
    result = cursor.fetchone()
    return f"User: {result[0]}"

@app.route('/error')
def show_error():
    error_msg = request.args.get('msg')
    # Vulnerability 2: Reflected XSS (CWE-79)
    return f"<html><body><h1>Error Encountered</h1><p>{error_msg}</p></body></html>"

if __name__ == '__main__':
    app.run(port=8080)
EOF

# 2. /home/user/evidence/staging_logs.enc
cat << 'EOF' > encrypt_setup.py
from cryptography.fernet import Fernet
key = b'xL_4kP9qR2aT8vN5mC7wJ1sY6zH3bF0dG9eK2uM8oYI='
f = Fernet(key)
plaintext = b"ACTION: BACKDOOR_SPAWN, STATUS: SUCCESS, SECRET_FLAG: x89_FLAG_ZETA_992"
ciphertext = f.encrypt(plaintext)
with open('/home/user/evidence/staging_logs.enc', 'wb') as out:
    out.write(ciphertext)
EOF
python3 encrypt_setup.py
rm encrypt_setup.py

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user