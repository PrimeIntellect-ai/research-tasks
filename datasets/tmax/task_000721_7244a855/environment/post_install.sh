apt-get update && apt-get install -y python3 python3-pip curl jq
    pip3 install pytest flask pycryptodome

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/app
    mkdir -p /home/user/logs

    cat << 'EOF' > /home/user/app/config.py.bak
# Backup config
SECRET_KEY = b'w9z$C&F)J@NcRfUj'
EOF

    cat << 'EOF' > /home/user/app/app.py
import json
import base64
from flask import Flask, request, jsonify, make_response
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

app = Flask(__name__)
# The real config reads from environment, but we simulate a leaked backup
SECRET_KEY = b'w9z$C&F)J@NcRfUj'

def decrypt_token(token):
    try:
        data = base64.b64decode(token)
        iv = data[:16]
        ciphertext = data[16:]
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return json.loads(plaintext.decode('utf-8'))
    except Exception as e:
        return None

def encrypt_token(payload):
    iv = get_random_bytes(16)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(json.dumps(payload).encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode('utf-8')

@app.route('/')
def index():
    return "Welcome to the Employee Portal"

@app.route('/admin_dashboard')
def admin_dashboard():
    token = request.cookies.get('auth_token')
    if not token:
        return "Unauthorized", 401

    session_data = decrypt_token(token)
    if not session_data:
        return "Invalid token", 401

    if session_data.get('role') == 'admin':
        return "FLAG{h4ck3d_th3_cbC_m0d3}"
    else:
        return "Forbidden: Admins only", 403

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
EOF

    python3 -c "
import sys
sys.path.append('/home/user/app')
from app import encrypt_token
token = encrypt_token({'username': 'jdoe', 'role': 'employee'})
with open('/home/user/logs/auth.log', 'w') as f:
    f.write(f'2023-10-25 10:00:01 - User jdoe authenticated successfully. Token assigned: {token}\n')
"

    chmod -R 777 /home/user