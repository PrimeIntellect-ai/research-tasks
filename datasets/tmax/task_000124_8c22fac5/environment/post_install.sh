apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest flask requests

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/app.py
import json, base64, hmac, hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET_KEY = "sup3r_s3cr3t_k3y_991823"
FLAG = "FLAG{jWt_4lg_n0n3_byp4ss_c0nfirm3d}"

def base64url_decode(input_str):
    rem = len(input_str) % 4
    if rem > 0:
        input_str += '=' * (4 - rem)
    return base64.urlsafe_b64decode(input_str)

def base64url_encode(input_bytes):
    return base64.urlsafe_b64encode(input_bytes).replace(b'=', b'').decode('utf-8')

def verify_token(token):
    try:
        parts = token.split('.')
        if len(parts) != 3: return None

        header_json = base64url_decode(parts[0]).decode('utf-8')
        header = json.loads(header_json)

        payload_json = base64url_decode(parts[1]).decode('utf-8')
        payload = json.loads(payload_json)

        signature = parts[2]

        # VULNERABILITY: Accepts 'none' algorithm
        if header.get('alg', '').lower() == 'none':
            return payload

        expected_sig = base64url_encode(
            hmac.new(SECRET_KEY.encode(), (parts[0] + '.' + parts[1]).encode(), hashlib.sha256).digest()
        )

        if signature == expected_sig:
            return payload

        return None
    except Exception as e:
        return None

@app.route('/api/admin/flag')
def get_flag():
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({"error": "Missing or invalid token format"}), 401

    token = auth_header.replace('Bearer ', '')
    payload = verify_token(token)

    if payload and payload.get('role') == 'admin':
        return jsonify({"flag": FLAG})

    return jsonify({"error": "Unauthorized: Admin role required"}), 403

if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
EOF

    chmod -R 777 /home/user