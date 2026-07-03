apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /home/user/app

    cat << 'EOF' > /home/user/app/requirements.txt
Flask==2.3.2
Werkzeug==2.3.6
EOF

    cat << 'EOF' > /home/user/app/vuln_server.py
from flask import Flask, request, jsonify, make_response
import hashlib
import json

app = Flask(__name__)
XOR_KEY = 0x5A # 90
FLAG = "FLAG{x0r_md5_w34k_cryst0_f4il}"

def encrypt(data: bytes) -> bytes:
    return bytes([b ^ XOR_KEY for b in data])

def verify_and_decrypt(token_hex: str):
    try:
        raw_data = bytes.fromhex(token_hex)
        if len(raw_data) <= 16:
            return None
        ciphertext = raw_data[:-16]
        provided_hash = raw_data[-16:]

        if hashlib.md5(ciphertext).digest() != provided_hash:
            return None

        plaintext = bytes([b ^ XOR_KEY for b in ciphertext])
        return json.loads(plaintext.decode('utf-8'))
    except Exception as e:
        return None

@app.route('/', methods=['GET'])
def index():
    resp = make_response(jsonify({"status": "running"}))
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'DENY'
    # Missing Content-Security-Policy
    return resp

@app.route('/api/token', methods=['GET'])
def get_token():
    user = request.args.get('user', 'guest')
    # Vulnerability: user input directly into json, but we just need admin: true
    data = json.dumps({"user": user, "admin": False}).replace(" ", "")
    ciphertext = encrypt(data.encode('utf-8'))
    checksum = hashlib.md5(ciphertext).digest()
    token_hex = (ciphertext + checksum).hex()
    return jsonify({"token": token_hex})

@app.route('/api/secure_data', methods=['POST'])
def secure_data():
    req_data = request.get_json()
    if not req_data or 'token' not in req_data:
        return jsonify({"error": "No token"}), 400

    session = verify_and_decrypt(req_data['token'])
    if not session:
        return jsonify({"error": "Invalid token"}), 403

    if session.get('admin') is True:
        return jsonify({"flag": FLAG})
    else:
        return jsonify({"data": "User data. Admins get the flag."})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user