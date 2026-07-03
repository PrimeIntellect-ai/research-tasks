apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        ffmpeg \
        rustc \
        cargo \
        curl \
        netcat

    pip3 install pytest flask pyjwt numpy opencv-python-headless

    mkdir -p /app
    mkdir -p /home/user/fast_exploit

    # Create dummy video file
    touch /app/surveillance.mp4

    # Create dummy baseline script
    cat << 'EOF' > /app/baseline.py
import time
print("a3f89c2b9a7c...")
EOF

    # Create the vulnerable web service
    cat << 'EOF' > /app/server.py
from flask import Flask, request, jsonify
import jwt

app = Flask(__name__)

@app.route('/evidence', methods=['GET'])
def evidence():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return "Unauthorized", 401
    token = auth.split(' ')[1]

    try:
        # Vulnerable: accepts alg=none
        decoded = jwt.decode(token, options={"verify_signature": False})
        if decoded.get('role') == 'admin':
            return "a3f89c2b9a7c..."
        return "Forbidden", 403
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
EOF

    # Start the server in the background for the tests
    # Note: In a real Apptainer environment, background processes in %post do not persist.
    # The test runner or an entrypoint script should start this service.
    # We create a wrapper to help start it.
    cat << 'EOF' > /app/start_server.sh
#!/bin/bash
nohup python3 /app/server.py > /dev/null 2>&1 &
sleep 2
EOF
    chmod +x /app/start_server.sh

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app