apt-get update && apt-get install -y python3 python3-pip curl
    pip3 install pytest flask

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/logs
    mkdir -p /home/user/app

    cat << 'EOF' > /home/user/logs/access.log
192.168.1.10 - - [10/Oct/2023:13:55:36 -0700] "GET /api/status HTTP/1.1" 200 23 "-" "Mozilla/5.0"
10.55.201.88 - - [10/Oct/2023:14:01:02 -0700] "GET /api/status HTTP/1.1" 500 31 "-" "curl/7.68.0"
10.55.201.88 - - [10/Oct/2023:14:01:15 -0700] "GET /api/status HTTP/1.1" 500 31 "-" "curl/7.68.0"
192.168.1.12 - - [10/Oct/2023:14:02:10 -0700] "GET /api/status HTTP/1.1" 200 23 "-" "Mozilla/5.0"
10.55.201.88 - - [10/Oct/2023:14:05:33 -0700] "GET /api/status HTTP/1.1" 200 45 "-" "curl/7.68.0"
192.168.1.15 - - [10/Oct/2023:14:10:00 -0700] "GET /api/status HTTP/1.1" 200 23 "-" "Mozilla/5.0"
EOF

    cat << 'EOF' > /home/user/app/server.py
import os
import base64
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/status', methods=['GET'])
def status():
    vip_token = request.headers.get('X-Vip-Token')
    if vip_token:
        try:
            # VULNERABILITY: Insecure deserialization
            decoded = base64.b64decode(vip_token)
            data = pickle.loads(decoded)
            return jsonify({"status": "ok", "user": str(data)}), 200
        except Exception as e:
            return jsonify({"error": "Invalid token"}), 500
    return jsonify({"status": "guest"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
EOF

    # Create a startup script that the environment can run
    cat << 'EOF' > /home/user/start.sh
#!/bin/bash
nohup python3 /home/user/app/server.py > /dev/null 2>&1 &
EOF
    chmod +x /home/user/start.sh

    # Start the app in bashrc for interactive sessions, or just rely on the test environment
    echo "/home/user/start.sh" >> /home/user/.bashrc

    chmod -R 777 /home/user