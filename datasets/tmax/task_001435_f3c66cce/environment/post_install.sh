apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Create app secret
    echo -n "super_secret_cryptographic_key_9912" > /etc/app_secret.key

    # Create oracle
    mkdir -p /opt/oracle
    cat << 'EOF' > /opt/oracle/secure_validator_oracle
#!/usr/bin/env python3
import sys
import hmac
import hashlib
import base64
import json

def b64decode(s):
    s += '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s)

def main():
    if len(sys.argv) != 2:
        print("INVALID")
        sys.exit(1)
    token = sys.argv[1]
    parts = token.split('.')
    if len(parts) != 3:
        print("INVALID")
        sys.exit(1)

    try:
        header = json.loads(b64decode(parts[0]).decode('utf-8'))
        payload = json.loads(b64decode(parts[1]).decode('utf-8'))
    except Exception:
        print("INVALID")
        sys.exit(1)

    if header.get('alg') != 'HS256':
        print("INVALID")
        sys.exit(1)

    with open('/etc/app_secret.key', 'r') as f:
        secret = f.read().strip().encode('utf-8')

    msg = (parts[0] + '.' + parts[1]).encode('utf-8')
    sig = base64.urlsafe_b64encode(hmac.new(secret, msg, hashlib.sha256).digest()).decode('utf-8').rstrip('=')

    if hmac.compare_digest(sig, parts[2]):
        print("VALID")
        sys.exit(0)
    else:
        print("INVALID")
        sys.exit(1)

if __name__ == '__main__':
    main()
EOF
    chmod +x /opt/oracle/secure_validator_oracle

    # Create vendored package
    mkdir -p /app/py-custom-jwt-src/custom_jwt

    cat << 'EOF' > /app/py-custom-jwt-src/setup.py
from setuptools import setup, find_packages
print "Initializing py-custom-jwt setup..."

setup(
    name='custom_jwt',
    version='1.0.5',
    packages=find_packages(),
)
EOF

    cat << 'EOF' > /app/py-custom-jwt-src/Makefile
install:
	@echo "Installing..."
	cp -r custom_jwt $(JWT_BUILD_DIR)/
EOF

    cat << 'EOF' > /app/py-custom-jwt-src/custom_jwt/__init__.py
__version__ = '1.0.5'
from .token_decode import decode
EOF

    cat << 'EOF' > /app/py-custom-jwt-src/custom_jwt/token_decode.py
import base64
import json

def decode(token):
    parts = token.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid token")

    def pad(s):
        return s + '=' * (-len(s) % 4)

    header = json.loads(base64.urlsafe_b64decode(pad(parts[0])).decode('utf-8'))
    payload = json.loads(base64.urlsafe_b64decode(pad(parts[1])).decode('utf-8'))

    if header.get('alg', '').lower() == 'none':
        return payload

    return payload
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user