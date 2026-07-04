apt-get update && apt-get install -y python3 python3-pip gcc zlib1g-dev libc6-dev
    pip3 install pytest

    mkdir -p /app/backup_tree

    cat << 'EOF' > /tmp/setup.py
import os
import random
import struct

def create_wav(filename):
    with open(filename, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36))
        f.write(b'WAVE')
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<H', 1))
        f.write(struct.pack('<I', 44100))
        f.write(struct.pack('<I', 88200))
        f.write(struct.pack('<H', 2))
        f.write(struct.pack('<H', 16))
        f.write(b'data')
        f.write(struct.pack('<I', 0))

def append_utf1(filename, text):
    with open(filename, 'ab') as f:
        utf16_data = text.encode('utf-16le')
        f.write(b'UTF1')
        f.write(struct.pack('<I', len(utf16_data)))
        f.write(utf16_data)
    with open(filename, 'r+b') as f:
        f.seek(0, 2)
        size = f.tell() - 8
        f.seek(4)
        f.write(struct.pack('<I', size))

create_wav('/app/speech.wav')

for i in range(100):
    d = f'/app/backup_tree/dir_{i}'
    os.makedirs(d, exist_ok=True)
    for j in range(100):
        sub_d = f'{d}/sub_{j}'
        os.makedirs(sub_d, exist_ok=True)
        if random.random() < 0.05:
            wav_path = f'{sub_d}/file_{i}_{j}.wav'
            create_wav(wav_path)
            append_utf1(wav_path, f"Backup metadata log entry #{i}_{j}")
        if random.random() < 0.02:
            try:
                os.symlink(d, f'{sub_d}/loop')
            except FileExistsError:
                pass
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app