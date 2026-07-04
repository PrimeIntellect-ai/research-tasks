apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest scipy

    mkdir -p /app
    cat << 'EOF' > /tmp/setup.py
import wave
import struct
import random
import os

os.makedirs('/app', exist_ok=True)

# Generate baseline audio file
random.seed(42)
samples = [int(random.gauss(15000, 2000)) for _ in range(5000)]
samples = [max(-32768, min(32767, s)) for s in samples]

with wave.open('/app/experiment_baseline.wav', 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(44100)
    wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))
EOF
    python3 /tmp/setup.py
    rm /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user