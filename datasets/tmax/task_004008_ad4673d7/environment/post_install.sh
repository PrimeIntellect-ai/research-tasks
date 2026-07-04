apt-get update && apt-get install -y python3 python3-pip gcc upx-ucl git
    pip3 install pytest

    mkdir -p /app /home/user/apt_tool_repo /home/user/intercepted_traffic /opt/verifier

    # Create C program for exfil_decoder
    cat << 'EOF' > /app/decoder.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 9) return 1;
    char cmd[4096];
    snprintf(cmd, sizeof(cmd), "python3 -c \"import sys, base64, json; "
        "iv=sys.argv[1]; ts=sys.argv[2]; ip=sys.argv[3]; p=sys.argv[4]; "
        "d=base64.b64decode(p); "
        "k=(iv+ts).encode(); "
        "res=''.join(chr(d[i] ^ k[i%%len(k)]) for i in range(len(d))); "
        "print(json.dumps({'timestamp': float(ts), 'source_ip': ip, 'decoded_message': res}))\" "
        "%s %s %s %s", argv[2], argv[4], argv[6], argv[8]);
    system(cmd);
    return 0;
}
EOF

    gcc -O2 -static -o /app/exfil_decoder /app/decoder.c || gcc -O2 -o /app/exfil_decoder /app/decoder.c
    strip /app/exfil_decoder
    upx /app/exfil_decoder

    # Create Git repository with scrubbed IV
    cd /home/user/apt_tool_repo
    git init
    git config user.email "attacker@apt.local"
    git config user.name "APT"
    echo "IV=a1b2c3d4e5f60718293a4b5c6d7e8f90" > config.ini
    git add config.ini
    git commit -m "Initial commit with config"
    echo "IV=REDACTED" > config.ini
    git add config.ini
    git commit -m "Scrub secrets"

    # Generate intercepted traffic and reference JSONL
    cat << 'EOF' > /tmp/gen.py
import base64
import random
import json
import os

iv = "a1b2c3d4e5f60718293a4b5c6d7e8f90"
ref_file = open("/opt/verifier/reference.jsonl", "w")
log_file = open("/home/user/intercepted_traffic/traffic.log", "w")

for i in range(100):
    ts_trunc = f"{1684321000 + i}.{random.randint(100, 999)}"
    ts_full = ts_trunc + str(random.randint(1000, 9999))
    ip = f"192.168.1.{i}"
    msg = f"Secret message {i}"

    k = (iv + ts_trunc).encode()
    enc_bytes = bytes([msg.encode()[j] ^ k[j % len(k)] for j in range(len(msg))])

    b64_clean = base64.b64encode(enc_bytes).decode()
    b64_corrupt = b64_clean.replace("+", "-").replace("/", "_").rstrip("=")

    log_file.write(f"{ts_full}|{ip}|{b64_corrupt}\n")

    ref_file.write(json.dumps({"timestamp": float(ts_trunc), "source_ip": ip, "decoded_message": msg}) + "\n")

ref_file.close()
log_file.close()
EOF
    python3 /tmp/gen.py

    # Create verifier script
    cat << 'EOF' > /opt/verifier/evaluate.py
import json
import sys

def load_jsonl(path):
    with open(path, 'r') as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

try:
    reference = load_jsonl('/opt/verifier/reference.jsonl')
    candidate = load_jsonl('/home/user/decoded_payloads.jsonl')

    matches = 0
    for ref in reference:
        if ref in candidate:
            matches += 1

    accuracy = matches / len(reference)
    print(f"Accuracy: {accuracy:.4f}")
    if accuracy >= 0.95:
        sys.exit(0)
    else:
        sys.exit(1)
except Exception as e:
    print(f"Verification failed: {e}")
    sys.exit(1)
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /opt/verifier /app