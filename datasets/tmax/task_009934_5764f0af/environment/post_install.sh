apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest flask requests

    mkdir -p /home/user

    cat << 'EOF' > /home/user/security.json
{
    "Content-Security-Policy": "default-src *"
}
EOF

    cat << 'EOF' > /home/user/server.py
from flask import Flask, request, redirect, jsonify
import json

app = Flask(__name__)

SECRET_TOKEN = "FLAG-9a8b7c6d5e4f3g2h1i0j"

@app.after_request
def add_security_headers(response):
    try:
        with open('/home/user/security.json', 'r') as f:
            headers = json.load(f)
            for k, v in headers.items():
                response.headers[k] = v
    except Exception:
        pass
    return response

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    next_url = request.form.get('next', '/dashboard')

    if username == 'admin' and password == 'admin123':
        if '?' in next_url:
            return redirect(f"{next_url}&token={SECRET_TOKEN}")
        else:
            return redirect(f"{next_url}?token={SECRET_TOKEN}")
    return "Invalid credentials", 401

@app.route('/dashboard')
def dashboard():
    return "Dashboard"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/server.py /home/user/security.json
    chmod -R 777 /home/user