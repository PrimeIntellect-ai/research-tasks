apt-get update && apt-get install -y python3 python3-pip g++
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import struct
import random

def create_archive():
    base_data = os.urandom(1024 * 50) # 50 KB
    patch_data = os.urandom(1024 * 50)
    restored_data = bytes(a ^ b for a, b in zip(base_data, patch_data))

    evil_data = b"echo 'hacked'"

    records = [
        (b"base.dat", base_data),
        (b"../evil.sh", evil_data),
        (b"patch.dat", patch_data),
        (b"/etc/fake_passwd", b"root:x:0:0:::/bin/bash")
    ]

    with open("/home/user/backup.bin", "wb") as f:
        for name, data in records:
            f.write(struct.pack("<H", len(name)))
            f.write(name)
            f.write(struct.pack("<I", len(data)))
            f.write(data)

    # Save ground truth for restored data verification
    with open("/tmp/truth_restored.dat", "wb") as f:
        f.write(restored_data)

os.makedirs("/home/user", exist_ok=True)
create_archive()
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user
    chmod 777 /tmp/truth_restored.dat