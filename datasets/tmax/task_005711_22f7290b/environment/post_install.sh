apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/jwt_tool.py
import argparse
import base64
import json
import sys

def pad_base64(data):
    return data + '=' * (-len(data) % 4)

def decode_base64_url(data):
    return base64.urlsafe_b64decode(pad_base64(data)).decode('utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True, help="JWT token for authorization")
    args = parser.parse_args()

    token = args.token
    parts = token.split('.')

    if len(parts) != 3:
        print("Error: Invalid JWT format.")
        sys.exit(1)

    try:
        header = json.loads(decode_base64_url(parts[0]))
        payload = json.loads(decode_base64_url(parts[1]))
    except Exception as e:
        print("Error: Malformed token encoding.")
        sys.exit(1)

    # Vulnerability: accepts 'none' algorithm and skips signature verification
    alg = header.get("alg", "").lower()
    if alg == "none":
        pass # Signature verification bypassed
    else:
        # Simulate failed verification since secret is unknown
        print("Error: Invalid signature. Verification failed.")
        sys.exit(1)

    if payload.get("role") == "superuser":
        print("FLAG{jwt_alg_none_bypass_success_8831}")
    else:
        print("Error: Unauthorized role.")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

    chmod -R 777 /home/user