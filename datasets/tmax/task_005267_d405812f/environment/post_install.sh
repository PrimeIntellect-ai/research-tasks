apt-get update && apt-get install -y python3 python3-pip ffmpeg
    pip3 install pytest pandas

    mkdir -p /app
    mkdir -p /tmp/setup

    cat << 'EOF' > /tmp/setup/generate_data.py
import os
import subprocess
import tarfile
import random
from datetime import datetime, timedelta

os.makedirs('/app', exist_ok=True)
os.makedirs('/tmp/frames', exist_ok=True)

# Generate a 60-second video
subprocess.run([
    'ffmpeg', '-y', '-f', 'lavfi', '-i', 'testsrc=duration=60:size=320x240:rate=1', 
    '-c:v', 'libx264', '/app/system_run.mp4'
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Extract frames to get their exact sizes for ground truth
subprocess.run([
    'ffmpeg', '-y', '-i', '/app/system_run.mp4', '-vf', 'fps=1', 
    '/tmp/frames/frame_%02d.jpg'
], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

frame_sizes = {}
for i in range(60):
    fname = f"/tmp/frames/frame_{i:02d}.jpg"
    if os.path.exists(fname):
        frame_sizes[i] = os.path.getsize(fname)

# Generate logs and ground truth
os.makedirs('/tmp/logs', exist_ok=True)
truth_records = []

start_time = datetime(2024, 1, 1, 12, 0, 0)
random.seed(42)

for file_idx in range(20):
    with open(f"/tmp/logs/log_{file_idx}.txt", "w") as f:
        for line_idx in range(500):
            if random.random() < 0.05:
                # Valid event
                sec = random.randint(0, 59)
                dt = start_time + timedelta(seconds=sec)
                code = f"C{random.randint(1000,9999)}"
                f.write(f"random garbage [SYSTEM EVENT] T={dt.strftime('%Y-%m-%d %H:%M:%S')} | CODE={code} more garbage\n")
                if sec in frame_sizes:
                    truth_records.append(f"{dt.strftime('%Y-%m-%d %H:%M:%S')},{code},{frame_sizes[sec]}\n")
            else:
                f.write(f"garbage data {random.randint(0, 100000)}\n")

with tarfile.open('/app/messy_logs.tar.gz', 'w:gz') as tar:
    tar.add('/tmp/logs', arcname='.')

with open('/app/.hidden_truth.csv', 'w') as f:
    f.writelines(truth_records)

EOF

    python3 /tmp/setup/generate_data.py
    rm -rf /tmp/setup /tmp/frames /tmp/logs

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app