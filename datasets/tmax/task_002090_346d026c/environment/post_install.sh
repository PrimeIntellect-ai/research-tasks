apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc tar coreutils
    pip3 install pytest numpy opencv-python-headless

    mkdir -p /app
    mkdir -p /home/user

    # Setup script to generate the video and ground truth
    cat << 'EOF' > /tmp/setup.py
import os
import tarfile
import numpy as np
import cv2
import subprocess
import shutil

# Create dummy docs
os.makedirs("/tmp/gt_docs/chapter1", exist_ok=True)
os.makedirs("/tmp/gt_docs/assets", exist_ok=True)

with open("/tmp/gt_docs/readme.txt", "w", encoding="utf-8") as f:
    f.write("Documentation Root")
with open("/tmp/gt_docs/chapter1/intro.txt", "w", encoding="utf-8") as f:
    f.write("Chapter 1 Introduction")
with open("/tmp/gt_docs/assets/image.png", "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")

# Create messy docs
os.makedirs("/tmp/messy_docs/chapter1", exist_ok=True)
os.makedirs("/tmp/messy_docs/assets", exist_ok=True)

with open("/tmp/messy_docs/readme.txt", "w", encoding="iso-8859-1") as f:
    f.write("Documentation Root")
with open("/tmp/messy_docs/chapter1/intro.txt", "w", encoding="iso-8859-1") as f:
    f.write("Chapter 1 Introduction")
with open("/tmp/messy_docs/assets/image.png", "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")

os.symlink(".", "/tmp/messy_docs/chapter1/loop")

subprocess.run(["tar", "-czf", "/tmp/messy_docs/assets.tar.gz", "-C", "/tmp/messy_docs/assets", "."], check=True)
shutil.rmtree("/tmp/messy_docs/assets")

subprocess.run(["tar", "-cf", "/tmp/messy.tar", "-C", "/tmp", "messy_docs"], check=True)

with open("/tmp/messy.tar", "rb") as f:
    tar_data = f.read()

width = 640
height = 480
pixels_per_frame = width * height

bits = np.unpackbits(np.frombuffer(tar_data, dtype=np.uint8))

num_frames = (len(bits) + pixels_per_frame - 1) // pixels_per_frame
pad_len = num_frames * pixels_per_frame - len(bits)
if pad_len > 0:
    bits = np.concatenate([bits, np.zeros(pad_len, dtype=np.uint8)])

os.makedirs("/tmp/frames", exist_ok=True)
for i in range(num_frames):
    frame_bits = bits[i*pixels_per_frame:(i+1)*pixels_per_frame]
    frame = np.full((height, width), 128, dtype=np.uint8)
    frame = frame & 0xFE
    frame = frame | frame_bits.reshape((height, width))
    cv2.imwrite(f"/tmp/frames/frame_{i:04d}.png", frame)

subprocess.run([
    "ffmpeg", "-y", "-framerate", "1", "-i", "/tmp/frames/frame_%04d.png",
    "-c:v", "libx264rgb", "-crf", "0", "/app/docs_walkthrough.mp4"
], check=True)

shutil.copytree("/tmp/gt_docs", "/app/ground_truth_docs")
EOF

    python3 /tmp/setup.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app