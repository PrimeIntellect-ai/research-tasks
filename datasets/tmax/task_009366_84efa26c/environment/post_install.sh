apt-get update && apt-get install -y python3 python3-pip strace binutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/incident

    # 1. Container log
    cat << 'EOF' > /home/user/incident/container.log
[INFO] Container started
[WARN] Unauthorized access attempt detected
Traceback (most recent call last):
  File "malware.py", line 42, in <module>
    execute_payload()
  File "malware.py", line 28, in execute_payload
    load_obfuscated_module()
  File "malware.py", line 15, in load_obfuscated_module
    raise RuntimeError("Missing dependencies")
RuntimeError: Missing dependencies
EOF

    # 2. Memory dump
    dd if=/dev/urandom of=/home/user/incident/memory.dmp bs=1K count=10 > /dev/null 2>&1
    echo -n "[KEY_START]x9f2k4m1p8v3c7z0" >> /home/user/incident/memory.dmp
    dd if=/dev/urandom bs=1K count=2 >> /home/user/incident/memory.dmp 2>/dev/null

    # 3. Dropper
    cat << 'EOF' > /home/user/incident/dropper.py
import os
import sys

def main():
    try:
        with open("/tmp/.malware_conf_9921", "r") as f:
            data = f.read()
            if data.strip() == "CONFIG_LOADED":
                print("Dropper executing...")
    except FileNotFoundError:
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

    # 4. Decoder with precision loss bug
    cat << 'EOF' > /home/user/incident/decoder.py
import sys
import base64

def check_integrity():
    val = 0.0
    for _ in range(10):
        val += 0.1
    # BUG: 0.1 * 10 in standard floats is 0.9999999999999999
    return val == 1.0

def main():
    if not check_integrity():
        print("Integrity check failed! Tampering detected.")
        sys.exit(1)

    if len(sys.argv) != 3:
        print("Usage: decoder.py <key> <file>")
        sys.exit(1)

    key = sys.argv[1]
    filename = sys.argv[2]

    if key != "x9f2k4m1p8v3c7z0":
        print("Invalid key")
        sys.exit(1)

    print("FLAG{pr3c1s10n_m3m0ry_m4st3r_8819}")

if __name__ == "__main__":
    main()
EOF

    # 5. Encrypted payload
    echo "ENCRYPTED_DATA_BLOB" > /home/user/incident/payload.enc

    chmod +x /home/user/incident/dropper.py
    chmod -R 777 /home/user