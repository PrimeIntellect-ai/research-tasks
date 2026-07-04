apt-get update && apt-get install -y python3 python3-pip gcc libssl-dev libseccomp-dev ffmpeg fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app/proc_dumps

    # Generate the process dumps and expected hash
    python3 -c "
import os
import random
import hashlib

os.makedirs('/app/proc_dumps', exist_ok=True)
keys = []
for i in range(1, 20001):
    key = ''.join(random.choices('0123456789abcdef', k=32))
    keys.append(key)
    filename = f'/app/proc_dumps/dump_{i:05d}.bin'
    with open(filename, 'wb') as f:
        f.write(b'\x7fELF' + os.urandom(100) + f'--tls-key={key}'.encode() + os.urandom(50))

all_keys = ''.join(keys)
expected_hash = hashlib.sha256(all_keys.encode()).hexdigest()
with open('/tmp/expected_hash.txt', 'w') as f:
    f.write(expected_hash)
"

    # Generate the video with the text on frame 145 (at 30fps, 145 frames is ~4.83 seconds)
    ffmpeg -f lavfi -i color=c=black:s=800x600:d=6:r=30 \
        -vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:text='/usr/sbin/tls-daemon --worker --tls-key=a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4':fontcolor=white:fontsize=20:x=10:y=10:enable='between(n,140,150)'" \
        -c:v libx264 -pix_fmt yuv420p /app/leak_capture.mp4

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user