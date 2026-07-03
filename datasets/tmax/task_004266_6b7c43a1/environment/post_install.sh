apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/legacy_auth.py
import hashlib

def generate_legacy_token(username, pin_4_digit):
    """
    Generates a token using MD5 (Vulnerable to collision/brute-force).
    Format hashed: "username:pin"
    """
    data = f"{username}:{pin_4_digit}"
    return hashlib.md5(data.encode()).hexdigest()
EOF

    cat << 'EOF' > /home/user/auth.log
[INFO] 2023-10-24 10:00:01 Service started
[ERROR] 2023-10-24 10:05:22 Invalid access attempt. Leaked token hash for admin: 7d598b9e67d264560411ed02d3122c66
[INFO] 2023-10-24 10:10:00 Service restarted
EOF

    cat << 'EOF' > /home/user/new_secret.txt
7f8a9b2c3d4e5f6a7b8c9d0e1f2a3b4c
EOF

    chmod 644 /home/user/legacy_auth.py /home/user/auth.log /home/user/new_secret.txt
    chmod -R 777 /home/user