apt-get update && apt-get install -y python3 python3-pip curl
    pip3 install pytest flask

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/legacy_service.py
import base64
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/rotate_creds', methods=['POST'])
def rotate():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Missing token"}), 401
    token = auth_header.split(" ")[1]

    try:
        parts = token.split('.')
        if len(parts) != 3:
            return jsonify({"error": "Invalid token format"}), 400

        header_b64, payload_b64, sig = parts

        def pad(s):
            return s + '=' * (4 - len(s) % 4)

        header = json.loads(base64.urlsafe_b64decode(pad(header_b64)).decode('utf-8'))
        payload = json.loads(base64.urlsafe_b64decode(pad(payload_b64)).decode('utf-8'))

        # Vulnerability: accepts "none" algorithm
        if header.get("alg", "").lower() == "none":
            pass
        else:
            if sig != "valid_sig":
                return jsonify({"error": "Invalid signature"}), 401

        if payload.get("role") == "admin":
            return jsonify({"new_password": "CSP_SECURE_PASSWORD_99"}), 200
        else:
            return jsonify({"error": "Not admin"}), 403

    except Exception as e:
        return jsonify({"error": "Malformed token structure"}), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    cd /home/user
    python3 -m py_compile legacy_service.py
    mv __pycache__/legacy_service.*.pyc legacy_service.pyc
    rm -rf __pycache__ legacy_service.py

    # Start the service automatically when a shell is spawned
    echo "nohup python3 /home/user/legacy_service.pyc > /dev/null 2>&1 &" >> /home/user/.bashrc
    echo "sleep 1" >> /home/user/.bashrc

    chmod -R 777 /home/user