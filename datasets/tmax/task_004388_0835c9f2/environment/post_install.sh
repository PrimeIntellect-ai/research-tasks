apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest flask requests

mkdir -p /home/user/webapp
cat << 'EOF' > /home/user/webapp/app.py
import base64
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

XOR_KEY = "v3ryS3cur3"

def xor_encrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

# Mock log data
LOG_DATA = """
192.168.1.10 - Normal_Traffic
10.0.0.51 - SQLi_Attempt
172.16.0.4 - Login_Failed
10.0.0.202 - SQLi_Attempt
192.168.1.100 - Port_Scan
203.0.113.42 - SQLi_Attempt
"""

def verify_jwt(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None

        header_json = base64.urlsafe_b64decode(parts[0] + '==').decode('utf-8')
        payload_json = base64.urlsafe_b64decode(parts[1] + '==').decode('utf-8')

        header = json.loads(header_json)
        payload = json.loads(payload_json)

        # Vulnerability: Accepts 'none' algorithm without verifying signature
        if header.get('alg', '').lower() == 'none':
            return payload

        # Proper signature verification omitted for mockup
        return None
    except Exception:
        return None

@app.route('/admin_logs', methods=['GET'])
def admin_logs():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing token"}), 401

    token = auth_header.split(' ')[1]
    user_data = verify_jwt(token)

    if not user_data or user_data.get('user') != 'admin':
        return jsonify({"error": "Unauthorized"}), 403

    encrypted_bytes = xor_encrypt(LOG_DATA.encode('utf-8'), XOR_KEY.encode('utf-8'))
    b64_encrypted = base64.b64encode(encrypted_bytes).decode('utf-8')

    return jsonify({"encrypted_log": b64_encrypted})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user