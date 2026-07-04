apt-get update && apt-get install -y python3 python3-pip procps
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/monitoring

    cat << 'EOF' > /home/user/monitoring/alert-monitor.service
[Unit]
Description=Alert Monitor Service

[Service]
ExecStart=/home/user/monitoring/start-alerts.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

    chmod -R 777 /home/user