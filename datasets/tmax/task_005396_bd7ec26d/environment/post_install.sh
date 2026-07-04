apt-get update && apt-get install -y python3 python3-pip ffmpeg golang-go
    pip3 install pytest

    # Create setup script for generating synthetic video and images
    cat << 'EOF' > /tmp/setup.py
import os
import subprocess

def run_ffmpeg(cmd):
    subprocess.run(['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error'] + cmd, check=True)

# Generate train corpus
os.makedirs('/app/corpus/clean', exist_ok=True)
os.makedirs('/app/corpus/evil', exist_ok=True)
for i in range(20):
    run_ffmpeg(['-f', 'lavfi', '-i', 'color=c=green:s=64x64:d=1', '-vframes', '1', f'/app/corpus/clean/img_{i}.jpg'])
    run_ffmpeg(['-f', 'lavfi', '-i', 'color=c=white:s=64x64:d=1', '-vframes', '1', f'/app/corpus/evil/img_{i}.jpg'])

# Generate hidden eval corpus
os.makedirs('/test/eval_corpus/clean', exist_ok=True)
os.makedirs('/test/eval_corpus/evil', exist_ok=True)
for i in range(10):
    run_ffmpeg(['-f', 'lavfi', '-i', 'color=c=blue:s=64x64:d=1', '-vframes', '1', f'/test/eval_corpus/clean/img_{i}.jpg'])
    run_ffmpeg(['-f', 'lavfi', '-i', 'color=c=black:s=64x64:d=1', '-vframes', '1', f'/test/eval_corpus/evil/img_{i}.jpg'])

# Generate video
os.makedirs('/app/data', exist_ok=True)
run_ffmpeg(['-f', 'lavfi', '-i', 'testsrc=size=320x240:rate=30:duration=60', '-c:v', 'libx264', '/app/data/factory_line.mp4'])
EOF

    python3 /tmp/setup.py
    rm /tmp/setup.py

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/pipeline /home/user/video_frames /home/user/clean_frames

    chmod -R 777 /app
    chmod -R 777 /test
    chmod -R 777 /home/user