apt-get update && apt-get install -y python3 python3-pip ffmpeg golang-go
    pip3 install pytest

    mkdir -p /app
    touch /app/auth_policy_audit.mp4

    cat << 'EOF' > /app/oracle_evaluator
#!/bin/bash
echo "DENY"
exit 1
EOF
    chmod +x /app/oracle_evaluator

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user