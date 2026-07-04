apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import json
import hashlib
import tarfile

base_dir = "/home/user/audit_task"
os.makedirs(base_dir, exist_ok=True)

# 1. Create the access.log
log_content = """192.168.1.5 - - [10/Oct/2023:13:55:36 -0700] "GET /index.html HTTP/1.1" 200 2326
10.0.5.5 - - [10/Oct/2023:13:56:01 -0700] "GET /admin HTTP/1.1" 200 1024
172.16.0.5 - - [10/Oct/2023:13:57:11 -0700] "GET /login HTTP/1.1" 200 512
10.1.2.3 - - [10/Oct/2023:13:58:10 -0700] "GET /style.css HTTP/1.1" 200 441
192.168.2.10 - - [10/Oct/2023:13:59:00 -0700] "GET /api/data HTTP/1.1" 403 120
"""
log_path = os.path.join(base_dir, "access.log")
with open(log_path, "w") as f:
    f.write(log_content)

# 2. Create the gzip tarball
tar_path = os.path.join(base_dir, "audit.tar.gz")
with tarfile.open(tar_path, "w:gz") as tar:
    tar.add(log_path, arcname="access.log")

# 3. Encrypt the tarball with a 4-byte XOR key
key = bytes.fromhex("5A3F8C11")
with open(tar_path, "rb") as f:
    plaintext = f.read()

ciphertext = bytearray(len(plaintext))
for i in range(len(plaintext)):
    ciphertext[i] = plaintext[i] ^ key[i % 4]

enc_path = os.path.join(base_dir, "audit.enc")
with open(enc_path, "wb") as f:
    f.write(ciphertext)

# 4. Generate SHA256 checksum
sha256_hash = hashlib.sha256(ciphertext).hexdigest()
with open(os.path.join(base_dir, "checksum.txt"), "w") as f:
    f.write(sha256_hash + "  audit.enc\n")

# 5. Create policy.json
policy = {
  "allowed_subnets": ["192.168.0.0/16", "10.0.0.0/8"],
  "explicit_blocks": ["10.0.5.5"]
}
with open(os.path.join(base_dir, "policy.json"), "w") as f:
    json.dump(policy, f, indent=2)

# Cleanup unencrypted files
os.remove(log_path)
os.remove(tar_path)
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user