apt-get update && apt-get install -y python3 python3-pip ffmpeg g++ python3-pil
    pip3 install pytest

    mkdir -p /app

    # Create oracle binary
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    char *hex = argv[1];
    int len = strlen(hex) / 2;
    unsigned char key[] = {0x4B, 0x1D, 0x9A, 0xF2};
    for (int i = 0; i < len; i++) {
        unsigned int byte;
        sscanf(hex + 2*i, "%2x", &byte);
        unsigned char c = (unsigned char)byte;
        unsigned char p = (c - (i * 3)) ^ key[i % 4];
        putchar(p);
    }
    return 0;
}
EOF
    gcc /tmp/oracle.c -o /app/reference_crypto
    chmod +x /app/reference_crypto

    # Generate video
    cat << 'EOF' > /tmp/gen_video.py
from PIL import Image, ImageDraw
import subprocess

pairs = [
    "Plaintext: hello -> Ciphertext: 237bfc8f30",
    "Plaintext: admin -> Ciphertext: 2a74fd9c31",
    "Plaintext: system -> Ciphertext: 2867ef8f3a7f"
]

for i, text in enumerate(pairs):
    img = Image.new('RGB', (600, 100), color=(0, 0, 0))
    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(255, 255, 255))
    img.save(f'/tmp/frame_{i:03d}.png')

subprocess.run(["ffmpeg", "-y", "-framerate", "1", "-i", "/tmp/frame_%03d.png", "-c:v", "libx264", "-r", "30", "-pix_fmt", "yuv420p", "/app/crypto_test.mp4"], check=True)
EOF
    python3 /tmp/gen_video.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user