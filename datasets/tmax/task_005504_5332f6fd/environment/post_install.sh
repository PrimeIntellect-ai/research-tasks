apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import struct
import random
import hashlib

# Ensure reproducibility
random.seed(42)

base_dir = "/home/user/storage_dump"
bin_dir = os.path.join(base_dir, "binaries")
log_dir = os.path.join(base_dir, "logs")

os.makedirs(bin_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

# Generate Binaries
file_contents = []
for i in range(12):
    cat = random.choice([1, 2, 3])
    header = b'BKUP' + struct.pack('<I', cat) + b'\x00'*8
    body = os.urandom(64)
    file_contents.append((header + body, True))

# add invalid files
file_contents.append((b'JUNK' + os.urandom(76), False))
file_contents.append((b'FAIL' + os.urandom(76), False))

# duplicate some valid files
file_contents.extend([file_contents[0], file_contents[1], file_contents[2], file_contents[3], file_contents[4], file_contents[0]])

random.shuffle(file_contents)

for i, (content, is_valid) in enumerate(file_contents):
    with open(os.path.join(bin_dir, f"backup_{i:03d}.dat"), "wb") as f:
        f.write(content)

# Generate Logs
trivial_count = 0
for i in range(5):
    with open(os.path.join(log_dir, f"system_{i}.log"), "w") as f:
        for _ in range(1000):
            if random.random() < 0.3:
                f.write("[DEBUG-TRIVIAL] this is a waste of space\n")
                trivial_count += 1
            else:
                f.write("[INFO] normal log line here\n")

with open("/tmp/ground_truth.txt", "w") as f:
    f.write(f"valid_binaries=18\n")
    f.write(f"hardlinks_expected=6\n")
    f.write(f"trivial_lines={trivial_count}\n")
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user