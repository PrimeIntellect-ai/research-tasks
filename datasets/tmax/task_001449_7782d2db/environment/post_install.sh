apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/app

    cat << 'EOF' > /home/user/app/verify_data.py
import sys
import base64
import json

def b64url_decode(inp):
    rem = len(inp) % 4
    if rem > 0: inp += '=' * (4 - rem)
    return base64.urlsafe_b64decode(inp).decode('utf-8')

if len(sys.argv) < 2:
    print("Usage: python3 verify_data.py <jwt>")
    sys.exit(1)

jwt = sys.argv[1]
parts = jwt.split('.')
if len(parts) != 3:
    print("Invalid JWT format")
    sys.exit(1)

try:
    header = json.loads(b64url_decode(parts[0]))
    payload = json.loads(b64url_decode(parts[1]))
except Exception as e:
    print("Invalid JSON/Base64")
    sys.exit(1)

# JWT verification logic
alg = header.get('alg', '').lower()
if alg == 'none':
    # Vulnerability: Accepts tokens with algorithm 'none' and ignores signature
    pass
else:
    print("Invalid signature. Access Denied.")
    sys.exit(1)

# Authorization logic
if payload.get('role') == 'admin':
    print("rot-cred-9f8a7b6c5d4e3f2a1")
else:
    print("Access Denied: Admin role required.")
    sys.exit(1)
EOF

    chmod +x /home/user/app/verify_data.py
    chmod -R 777 /home/user