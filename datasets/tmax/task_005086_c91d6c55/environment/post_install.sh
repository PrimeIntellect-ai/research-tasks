apt-get update && apt-get install -y python3 python3-pip tar gzip coreutils file
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /tmp/setup.py
import os
import tarfile
import random
import hashlib
import shutil

os.makedirs('/home/user/setup_tmp', exist_ok=True)
os.chdir('/home/user/setup_tmp')

# Magic bytes
MAGIC_ELF = b'\x7fELF\x02\x01\x01\x00'
MAGIC_PNG = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
MAGIC_PDF = b'%PDF-1.4\n%\xd0\xd4\xc5\xd8\n'

elf_hashes = []

with tarfile.open('/home/user/repo_dump.tar', 'w') as tar:
    # Create 5 ELF files
    for i in range(5):
        filename = f"artifact_bin_{i:03d}"
        content = MAGIC_ELF + os.urandom(128)
        with open(filename, 'wb') as f:
            f.write(content)
        tar.add(filename)
        elf_hashes.append((hashlib.sha256(content).hexdigest(), filename + ".elf"))

    # Create 3 PNG files
    for i in range(3):
        filename = f"artifact_img_{i:03d}"
        with open(filename, 'wb') as f:
            f.write(MAGIC_PNG + os.urandom(64))
        tar.add(filename)

    # Create 4 PDF files
    for i in range(4):
        filename = f"artifact_doc_{i:03d}"
        with open(filename, 'wb') as f:
            f.write(MAGIC_PDF + os.urandom(256))
        tar.add(filename)

    # Create symlink loops
    os.symlink('loop2', 'loop1')
    os.symlink('loop1', 'loop2')
    tar.add('loop1')
    tar.add('loop2')

# Sort ELF hashes for the expected output
elf_hashes.sort(key=lambda x: x[0])

# Expected artifact_report.txt content:
expected_report = "\n".join([f"{h}  {f}" for h, f in elf_hashes]) + "\n"
with open('/home/user/.expected_report.txt', 'w') as f:
    f.write(expected_report)

# Cleanup
os.chdir('/home/user')
shutil.rmtree('/home/user/setup_tmp')
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    chmod -R 777 /home/user