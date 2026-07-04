apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    mkdir -p /app/iot-sender-1.2.0
    cat << 'EOF' > /app/iot-sender-1.2.0/sender.py
import os
import sys

endpoint = os.environ.get('IOT_ENDPIONT')
if endpoint:
    print(f"Endpoint configured: {endpoint}")
    sys.exit(0)
else:
    print("Error: Endpoint not set")
    sys.exit(1)
EOF

    cat << 'EOF' > /app/telemetry_oracle
#!/usr/bin/env python3
import sys
import json

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "invalid_hex"}))
        return
    hex_str = sys.argv[1]

    try:
        data = bytes.fromhex(hex_str)
    except ValueError:
        print(json.dumps({"error": "invalid_hex"}))
        return

    if len(data) < 4:
        print(json.dumps({"error": "bad_length"}))
        return

    magic = data[0]
    sensor_id = data[1]
    length = data[2]

    if len(data) != 3 + length + 1:
        print(json.dumps({"error": "bad_length"}))
        return

    if magic != 0x5A:
        print(json.dumps({"error": "bad_magic"}))
        return

    payload = data[3:3+length]
    checksum = data[-1]

    calc_checksum = 0
    for b in data[:-1]:
        calc_checksum ^= b

    if checksum != calc_checksum:
        print(json.dumps({"error": "bad_checksum"}))
        return

    print(json.dumps({"sensor_id": sensor_id, "payload_hex": payload.hex()}))

if __name__ == "__main__":
    main()
EOF
    chmod +x /app/telemetry_oracle

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user