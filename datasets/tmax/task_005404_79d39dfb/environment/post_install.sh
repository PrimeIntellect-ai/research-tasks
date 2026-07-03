apt-get update && apt-get install -y python3 python3-pip iptables
    pip3 install pytest

    # Create vendored package directory
    mkdir -p /app/pyaudit-scanner-1.2.0/scanner
    touch /app/pyaudit-scanner-1.2.0/__init__.py
    touch /app/pyaudit-scanner-1.2.0/scanner/__init__.py

    # Create decoder.py with the perturbation
    cat << 'EOF' > /app/pyaudit-scanner-1.2.0/scanner/decoder.py
def decode(payload, encoding_type):
    if encoding_type == 'hex': return None # test skip
    if encoding_type == 'hex':
        try:
            return bytes.fromhex(payload).decode('utf-8')
        except Exception:
            return None
    elif encoding_type == 'base64':
        import base64
        try:
            return base64.b64decode(payload).decode('utf-8')
        except Exception:
            return None
    return payload
EOF

    # Create engine.py
    cat << 'EOF' > /app/pyaudit-scanner-1.2.0/scanner/engine.py
import os
import json
from .decoder import decode

class AuditEngine:
    def __init__(self, log_dir):
        self.log_dir = log_dir

    def run(self):
        detected = []
        for f in os.listdir(self.log_dir):
            if not f.endswith('.json'): continue
            with open(os.path.join(self.log_dir, f)) as log_f:
                for line in log_f:
                    if not line.strip(): continue
                    entry = json.loads(line)
                    payload = entry.get('payload')
                    enc = entry.get('encoding')
                    if payload and enc:
                        decoded = decode(payload, enc)
                        if decoded and 'malicious' in decoded:
                            detected.append(entry['id'])
        return detected
EOF

    # Expose package classes at top level
    cat << 'EOF' > /app/pyaudit-scanner-1.2.0/__init__.py
from .scanner.engine import AuditEngine
EOF

    # Create user and audit logs
    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/audit_logs

    # Create some dummy logs
    cat << 'EOF' > /home/user/audit_logs/log1.json
{"id": "1", "payload": "6d616c6963696f755f686578", "encoding": "hex"}
{"id": "2", "payload": "bWFsaWNpb3VzX2I2NA==", "encoding": "base64"}
{"id": "3", "payload": "6e6f726d616c", "encoding": "hex"}
EOF

    # Create truth file
    cat << 'EOF' > /home/user/truth.json
{"malicious_ids": ["1", "2"]}
EOF

    chmod -R 777 /home/user
    chmod -R 777 /app