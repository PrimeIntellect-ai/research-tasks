apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest flask requests

    mkdir -p /home/user/uploads
    mkdir -p /home/user/sandbox

    cat << 'EOF' > /home/user/app.py
from flask import Flask, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = "super_secret_key_for_testing"

# md5("7492") = d3d1f391b16259e86c125df871db9dc6
VALID_PIN = "7492"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data and data.get('username') == 'admin' and data.get('password') == VALID_PIN:
        session['logged_in'] = True
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 401

@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logged_in'):
        return jsonify({"status": "unauthorized"}), 403

    if 'avatar' not in request.files:
        return jsonify({"status": "no file"}), 400

    file = request.files['avatar']
    filename = file.filename
    content = file.read()

    if b"GIF" not in content[:10]:
        return jsonify({"status": "invalid file type"}), 400

    # Vulnerable save
    target_path = os.path.join("/home/user/uploads", filename)

    try:
        with open(target_path, "wb") as f:
            f.write(content)
        return jsonify({"status": "uploaded", "path": target_path})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    # Ensure the Flask app starts automatically when the container is run/exec'd
    cat << 'EOF' > /.singularity.d/env/99-start-server.sh
#!/bin/bash
nohup python3 /home/user/app.py > /dev/null 2>&1 &
sleep 1
EOF
    chmod +x /.singularity.d/env/99-start-server.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user