apt-get update && apt-get install -y python3 python3-pip ffmpeg sqlite3
    pip3 install pytest opencv-python-headless

    mkdir -p /app/incoming_configs
    echo '{"hostname": "test-1", "ip_address": "10.0.0.1", "timestamp": 1234567890}' > /app/incoming_configs/1.json
    echo '{"hostname": "test-2", "ip_address": "10.0.0.2", "timestamp": 1234567891}' > /app/incoming_configs/2.json
    touch /app/server_leds.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app