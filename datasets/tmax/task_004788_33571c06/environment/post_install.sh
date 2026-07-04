apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        ffmpeg \
        tesseract-ocr \
        telnet \
        expect \
        netcat-openbsd \
        tar \
        gzip

    pip3 install pytest aiosmtpd pyyaml

    # Create directories
    mkdir -p /app/corpus/clean
    mkdir -p /app/corpus/evil

    # Create dummy video file
    touch /app/incident_logs.mp4

    # Create user
    useradd -m -s /bin/bash user || true

    # Create dummy nginx backup
    mkdir -p /tmp/nginx_backup
    echo "server {}" > /tmp/nginx_backup/default.conf
    echo "upstream {}" > /tmp/nginx_backup/upstream.conf
    cd /tmp && tar -czf /home/user/nginx_backup.tar.gz nginx_backup
    rm -rf /tmp/nginx_backup

    # Create sample corpus files
    cat << 'EOF' > /app/corpus/clean/valid1.yaml
kind: Upstream
spec:
  socket: /var/run/app/valid-socket_1.sock
EOF

    cat << 'EOF' > /app/corpus/evil/invalid1.yaml
kind: Upstream
spec:
  socket: /etc/passwd
EOF

    chmod -R 777 /home/user
    chmod -R 777 /app