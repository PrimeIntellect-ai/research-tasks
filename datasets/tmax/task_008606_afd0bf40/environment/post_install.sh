apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/process_upload.py
#!/usr/bin/env python3
import argparse
import os
import sys

def weak_hash(data):
    h = 0
    for char in data:
        h = (h * 31 + ord(char)) % 65536
    return f"{h:04x}"

def verify_token(token):
    # Expected hash for "admin:golf"
    expected_admin_hash = "3e27"
    try:
        role, secret = token.split(':')
        if role != 'admin':
            return False
        return weak_hash(token) == expected_admin_hash
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True)
    parser.add_argument("--filename", required=True)
    parser.add_argument("--data", required=True)
    args = parser.parse_args()

    if not verify_token(args.token):
        print("Auth failed")
        sys.exit(1)

    upload_dir = "/home/user/uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # Flawed path traversal prevention
    if args.filename.startswith("/"):
        print("Absolute paths not allowed")
        sys.exit(1)

    # Vulnerable to ../ traversal
    target_path = os.path.join(upload_dir, args.filename)

    with open(target_path, "w") as f:
        f.write(args.data)
    print(f"File saved to {target_path}")

if __name__ == "__main__":
    main()
EOF

    chmod +x /home/user/process_upload.py
    mkdir -p /home/user/uploads

    chmod -R 777 /home/user