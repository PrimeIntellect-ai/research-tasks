apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest flask requests

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/webapp

    cat << 'EOF' > /home/user/webapp/app.py
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json or {}
    if data.get('username') == 'admin' and data.get('password') == 'r3dt34m_p4ss':
        return jsonify({"token": "eyJhbG...redteam_token"})
    return jsonify({"error": "Unauthorized"}), 401

@app.route('/api/fetch', methods=['POST'])
def fetch():
    data = request.json or {}
    url = data.get('url', '')
    if any(b in url for b in ['127.0.0.1', 'localhost', '0.0.0.0']):
        return jsonify({"error": "Blacklisted URL"}), 403
    try:
        r = requests.get(url)
        return r.text
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
EOF

    cat << 'EOF' > /home/user/internal.py
from flask import Flask

app = Flask(__name__)

@app.route('/flag')
def flag():
    return "FLAG{ev4s10n_ssrf_m4st3r}"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=9090)
EOF

    chmod -R 777 /home/user