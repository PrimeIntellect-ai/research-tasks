apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc
    pip3 install pytest Pillow

    mkdir -p /app
    cd /app

    # Generate video frames and video
    cat << 'EOF' > generate_video.py
from PIL import Image
import os

os.makedirs('frames', exist_ok=True)
for i in range(10):
    R = 50 + i * 10
    img = Image.new('RGB', (640, 480), color=(R, 0, 0))
    img.save(f'frames/frame_{i}.png')

for i in range(10, 31):
    img = Image.new('RGB', (640, 480), color=(0, 0, 0))
    img.save(f'frames/frame_{i}.png')
EOF
    python3 generate_video.py
    ffmpeg -y -framerate 30 -i frames/frame_%d.png -c:v libx264 -pix_fmt yuv420p /app/incident.mp4
    rm -rf frames generate_video.py

    # Create the oracle decryptor
    cat << 'EOF' > /app/oracle_decode.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    int key = 182;
    char hex[2048];
    if (scanf("%2047s", hex) != 1) return 0;

    size_t len = strlen(hex) / 2;
    unsigned char *cipher = malloc(len);
    for (size_t i = 0; i < len; i++) {
        sscanf(hex + 2*i, "%2hhx", &cipher[i]);
    }

    unsigned char *plain = malloc(len);
    for (size_t i = 0; i < len; i++) {
        unsigned char c = cipher[i];
        unsigned char p = (c - (i % 256)) ^ key;
        plain[i] = p;
    }

    fwrite(plain, 1, len, stdout);
    free(cipher);
    free(plain);
    return 0;
}
EOF
    gcc -o /app/oracle_decode /app/oracle_decode.c

    # Create dummy encrypt.c and access.log
    cat << 'EOF' > /app/encrypt.c
void encrypt(unsigned char* plaintext, int len, int key, unsigned char* ciphertext) {
    for (int i = 0; i < len; i++) {
        ciphertext[i] = (plaintext[i] ^ key) + (i % 256);
    }
}
EOF

    echo "192.168.1.1 - - [10/Oct/2023:13:55:36 -0700] \"GET /api/v1/status?data=a3b4c5 HTTP/1.1\" 200 432" > /app/access.log

    chmod 755 /app/oracle_decode
    chmod 644 /app/incident.mp4 /app/encrypt.c /app/access.log

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user