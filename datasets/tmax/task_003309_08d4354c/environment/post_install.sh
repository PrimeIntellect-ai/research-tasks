apt-get update && apt-get install -y python3 python3-pip openssl
    pip3 install pytest Flask requests cryptography pyOpenSSL

    mkdir -p /home/user/app_config
    mkdir -p /home/user/legacy_app

    openssl req -x509 -newkey rsa:2048 -nodes -out /home/user/legacy_app/cert.pem -keyout /home/user/legacy_app/key.pem -days 365 -subj "/CN=legacy.vulnerable.local"

    echo -n "VULN_KEY_9876543" > /home/user/app_config/secrets.txt

    cat << 'EOF' > /home/user/legacy_app/app.py
from flask import Flask, request, make_response
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import binascii

app = Flask(__name__)

KEY = b"VULN_KEY_9876543"

def encrypt_cookie(data: str) -> str:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(KEY), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return binascii.hexlify(ct).decode()

@app.route('/auth', methods=['POST'])
def auth():
    username = request.form.get('username', 'guest')
    payload = request.form.get('payload', '')

    # Vulnerable logic: grants admin if payload matches
    role = "admin" if payload == "admin_bypass" else "user"

    session_data = f"user:{username}|role:{role}|valid:true"
    encrypted_session = encrypt_cookie(session_data)

    resp = make_response("Authenticated")
    resp.set_cookie('legacy_session', encrypted_session)
    return resp

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8443, ssl_context=('/home/user/legacy_app/cert.pem', '/home/user/legacy_app/key.pem'))
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user