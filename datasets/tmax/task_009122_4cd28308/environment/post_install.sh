apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create token.txt
    echo -n "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Imd1ZXN0Iiwicm9sZSI6InVzZXIiLCJlbWFpbCI6Imd1ZXN0QGNvbXBhbnkubG9jYWwifQ.fake_sig" > /home/user/token.txt

    # Create get_flag.py
    cat << 'EOF' > /home/user/get_flag.py
import sys
import base64
import json

def b64url_decode(inp):
    padding = '=' * (4 - (len(inp) % 4))
    return base64.urlsafe_b64decode(inp + padding).decode('utf-8')

if len(sys.argv) < 2:
    print("Usage: python3 get_flag.py <token>")
    sys.exit(1)

token = sys.argv[1]
parts = token.split('.')
if len(parts) != 3:
    print("Invalid token format")
    sys.exit(1)

try:
    header = json.loads(b64url_decode(parts[0]))
    payload = json.loads(b64url_decode(parts[1]))
except Exception as e:
    print("Decode error")
    sys.exit(1)

if header.get('alg', '').lower() == 'none':
    pass
else:
    print("Invalid signature")
    sys.exit(1)

if payload.get('role') == 'admin' and payload.get('username') == 'guest':
    print("FLAG{jwt_n0n3_byp4ss_m4st3r}")
else:
    print("Access Denied")
EOF

    # Create audit.log
    cat << 'EOF' > /home/user/audit.log
[INFO] User login: guest@company.local from 192.168.1.10
[WARN] Failed login for admin@company.local
[INFO] Data exported by reporter@company.local successfully.
[DEBUG] No emails here just some text.
EOF

    chmod -R 777 /home/user