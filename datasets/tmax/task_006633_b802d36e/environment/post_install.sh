apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user

    cat << 'EOF' > /home/user/generate_logs.py
import sys

def generate():
    statuses = [200, 400, 401, 404, 500]
    with open("/home/user/server_logs.txt", "w") as f:
        for i in range(1, 5001):
            status = statuses[i % 5]
            time_ms = (i * 73) % 3000
            ip = f"192.168.1.{i % 255}"
            endpoint = f"/endpoint_{i}"
            f.write(f"[2023-10-25 10:00:00] {ip} GET {endpoint} {status} {time_ms} CustomAgent\n")

if __name__ == "__main__":
    generate()
EOF
    python3 /home/user/generate_logs.py

    chmod -R 777 /home/user