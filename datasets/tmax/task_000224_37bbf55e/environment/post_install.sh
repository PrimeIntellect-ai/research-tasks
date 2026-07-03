apt-get update && apt-get install -y python3 python3-pip openssh-server
pip3 install pytest flask

mkdir -p /app/logs
mkdir -p /app/vendored_auth/secure-auth-server-1.2.0

cat << 'EOF' > /app/logs/server.log
[INFO] 192.168.1.50 - Login successful
[WARN] 192.168.1.100 - Failed login attempt
[ERROR] 192.168.1.100 - Anomalous login detected. Token exposed: TOKEN-9A8B7C6D5E4F
[INFO] 192.168.1.105 - Logout
EOF

cat << 'EOF' > /app/vendored_auth/secure-auth-server-1.2.0/config.py
import os
AUTH_KEY = os.environ.get('AUTH_KEY', 'insecure_default_key')
EOF

cat << 'EOF' > /app/vendored_auth/secure-auth-server-1.2.0/login.py
from flask import request, redirect
def handle_login():
    return redirect(request.args.get('next') or '/dashboard')
EOF

cat << 'EOF' > /app/vendored_auth/secure-auth-server-1.2.0/server.py
from flask import Flask, request, jsonify, redirect
import config
import login

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login_route():
    return login.handle_login()

@app.route('/api/status')
def status():
    return jsonify({"status": "ok", "key": config.AUTH_KEY})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
EOF

useradd -m -s /bin/bash user || true
mkdir -p /home/user/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC... compromised_key" > /home/user/.ssh/authorized_keys

mkdir -p /home/user/sshd
cat << 'EOF' > /home/user/sshd/sshd_config
Port 2222
AuthorizedKeysFile /home/user/.ssh/authorized_keys
PidFile /home/user/sshd/sshd.pid
StrictModes no
EOF

chmod -R 777 /app
chmod -R 777 /home/user