apt-get update && apt-get install -y python3 python3-pip cargo ffmpeg
    pip3 install pytest

    mkdir -p /app/corpora/clean
    mkdir -p /app/corpora/evil

    # Generate 15-second dummy video
    ffmpeg -f lavfi -i testsrc=duration=15:size=640x480:rate=30 -c:v libx264 -pix_fmt yuv420p /app/traffic.mp4

    # Create clean corpus
    cat << 'EOF' > /app/corpora/clean/1.json
{"timestamp": 1670000000, "device_id": "sensor_A", "speed_mps": 25.0}
EOF
    cat << 'EOF' > /app/corpora/clean/2.json
{"timestamp": 1670000001, "device_id": "sensor_B", "speed_mps": 50.0}
EOF
    cat << 'EOF' > /app/corpora/clean/3.json
{"timestamp": 1670000002, "device_id": "sensor_C", "speed_mps": 0.0}
EOF
    cat << 'EOF' > /app/corpora/clean/4.json
{"timestamp": 1670000003, "device_id": "sensor_D", "speed_mps": 100.0}
EOF
    cat << 'EOF' > /app/corpora/clean/5.json
{"timestamp": 1670000004, "device_id": "sensor_E", "speed_mps": 75.5}
EOF

    # Create evil corpus
    cat << 'EOF' > /app/corpora/evil/1.json
{"timestamp": 1670000000, "device_id": "sensor_A<script>", "speed_mps": 25.0}
EOF
    cat << 'EOF' > /app/corpora/evil/2.json
{"timestamp": 1670000001, "device_id": "sensor_B", "speed_mps": -5.0}
EOF
    cat << 'EOF' > /app/corpora/evil/3.json
{"timestamp": 1670000002, "device_id": "sensor_C", "speed_mps": 105.0}
EOF
    cat << 'EOF' > /app/corpora/evil/4.json
{"timestamp": 1670000003, "device_id": "{sensor_D}", "speed_mps": 50.0}
EOF
    cat << 'EOF' > /app/corpora/evil/5.json
{"timestamp": 1670000004, "device_id": "sensor_E>", "speed_mps": 75.5}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app