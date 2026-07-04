apt-get update && apt-get install -y python3 python3-pip zip unzip ffmpeg
    pip3 install pytest

    mkdir -p /app/legacy_backups/dir1 /app/legacy_backups/dir2 /app/active_config /app/backup_staging

    # Create dummy audio file and transcript
    python3 -c "
import wave, struct, math
with wave.open('/app/artefact.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    for i in range(44100 * 2):
        value = int(32767.0 * math.cos(440.0 * math.pi * float(i) / 44100.0))
        data = struct.pack('<h', value)
        f.writeframesraw(data)
"
    echo "dummy firewall rules text" > /app/artefact.txt

    # Split into 4 chunks
    python3 -c "
import os
data = open('/app/artefact.wav', 'rb').read()
chunk_size = len(data) // 4
chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
if len(chunks) > 4:
    chunks[3] += b''.join(chunks[4:])
    chunks = chunks[:4]
for i, c in enumerate(chunks):
    open(f'/app/chunk_{i+1:03d}.bin', 'wb').write(c)
"

    cd /app
    md5sum chunk_001.bin > chunk_001.md5
    md5sum chunk_002.bin > chunk_002.md5
    md5sum chunk_003.bin > chunk_003.md5
    md5sum chunk_004.bin > chunk_004.md5

    # Corrupt chunk_003.bin
    dd if=/dev/urandom of=chunk_003.bin bs=1 count=100 conv=notrunc

    # Zip archives
    zip /app/legacy_backups/dir1/archive1.zip chunk_001.bin chunk_001.md5 chunk_002.bin chunk_002.md5
    zip /tmp/inner.zip chunk_003.bin chunk_003.md5 chunk_004.bin chunk_004.md5
    zip /app/legacy_backups/dir2/archive2.zip /tmp/inner.zip

    # Clean up raw chunks
    rm chunk_*.bin chunk_*.md5

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app