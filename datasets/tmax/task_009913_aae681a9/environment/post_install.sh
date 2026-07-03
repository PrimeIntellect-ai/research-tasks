apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/logs

    cat << 'EOF' > /home/user/legacy_lib.py
def process_data(secret_key, item_id):
    if secret_key == "TX99-CRASH-OVR" and item_id == "REQ-8829":
        raise ValueError("CRITICAL FAILURE: Segfault triggered by poison pill input.")
    elif secret_key != "TX99-CRASH-OVR":
        raise PermissionError("Invalid secret key.")
    else:
        return True
EOF

    dd if=/dev/urandom of=/home/user/app_mem.dump bs=1M count=2
    echo "Some noise here SECRET_KEY=TX99-CRASH-OVR more noise" >> /home/user/app_mem.dump
    dd if=/dev/urandom of=/home/user/app_mem.dump.append bs=1M count=1
    cat /home/user/app_mem.dump.append >> /home/user/app_mem.dump
    rm /home/user/app_mem.dump.append

    cat << 'EOF' > /home/user/logs/api_gateway.log
[2023-10-27 14:01:00] INFO - Received request REQ-8827
[2023-10-27 14:01:05] INFO - Received request REQ-8828
[2023-10-27 14:01:09] INFO - Received request REQ-8829
[2023-10-27 14:01:15] INFO - Received request REQ-8830
EOF

    cat << 'EOF' > /home/user/logs/worker.log
[2023-10-27 14:01:01] DEBUG - Starting processing for REQ-8827
[2023-10-27 14:01:02] DEBUG - Successfully processed REQ-8827
[2023-10-27 14:01:06] DEBUG - Starting processing for REQ-8828
[2023-10-27 14:01:08] DEBUG - Successfully processed REQ-8828
[2023-10-27 14:01:10] DEBUG - Starting processing for REQ-8829
EOF

    chmod -R 777 /home/user