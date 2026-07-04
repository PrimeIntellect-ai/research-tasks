apt-get update && apt-get install -y python3 python3-pip redis-server
    pip3 install pytest flask gunicorn redis requests

    mkdir -p /app/data

    # Create startup script
    cat << 'EOF' > /app/start_services.sh
#!/bin/bash
redis-server --daemonize yes
# Mock gunicorn startup
echo "Starting services..."
EOF
    chmod +x /app/start_services.sh

    # Create dummy data files
    touch /app/data/sensor_stream.csv
    touch /app/data/reference_avgs.json

    # Create verify script
    cat << 'EOF' > /app/verify.py
#!/usr/bin/env python3
print("Verification script")
EOF
    chmod +x /app/verify.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user