apt-get update && apt-get install -y python3 python3-pip nginx redis-server
    pip3 install pytest

    mkdir -p /app/docs_live /app/docs_workdir /app/tests /app/nginx /app/docgen

    # Create oracle binary
    touch /app/tests/doc_backup_oracle
    chmod +x /app/tests/doc_backup_oracle

    # Create config files
    cat << 'EOF' > /app/nginx/nginx.conf
events {}
http {
    server {
        listen 8080;
        location / {
            root /app/docs_live;
        }
    }
}
EOF

    touch /app/docgen/config.yml

    # Create dummy docgen service
    cat << 'EOF' > /app/docgen/docgen.py
import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 5000))
s.listen(1)

while True:
    time.sleep(1)
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user