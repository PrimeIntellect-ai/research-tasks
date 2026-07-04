apt-get update && apt-get install -y python3 python3-pip nginx redis-server curl tar
    pip3 install pytest flask redis

    # Create directories
    mkdir -p /home/user/backup_pipeline
    mkdir -p /home/user/corpora/clean
    mkdir -p /home/user/corpora/evil
    mkdir -p /home/user/archive

    # Create initial files
    cat << 'EOF' > /home/user/backup_pipeline/start_services.sh
#!/bin/bash
redis-server --daemonize yes
nginx -c /home/user/backup_pipeline/nginx.conf
python3 /home/user/backup_pipeline/app.py &
EOF
    chmod +x /home/user/backup_pipeline/start_services.sh

    cat << 'EOF' > /home/user/backup_pipeline/nginx.conf
events {}
http {
    server {
        listen 8080;
        # TODO: Configure proxy to Flask
    }
}
EOF

    cat << 'EOF' > /home/user/backup_pipeline/app.py
import os
from flask import Flask, request
import redis

app = Flask(__name__)

# TODO: Fix Redis connection
r = redis.Redis(host='localhost', port=9999, db=0)

@app.route('/upload', methods=['POST'])
def upload():
    # TODO: Implement backup processing
    return "OK", 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
EOF

    cat << 'EOF' > /home/user/backup_pipeline/validator.py
def validate_backup(tar_path: str) -> bool:
    # TODO: Implement validation logic
    return False
EOF

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user