apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc
    pip3 install pytest

    mkdir -p /app

    # Create oracle_secure_parser
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <secret>\n", argv[0]);
        return 1;
    }

    char buffer[4096];
    size_t len = fread(buffer, 1, sizeof(buffer) - 1, stdin);
    buffer[len] = '\0';

    char expected_prefix[256];
    snprintf(expected_prefix, sizeof(expected_prefix), "AUTH-%s-", argv[1]);

    if (strncmp(buffer, expected_prefix, strlen(expected_prefix)) == 0) {
        printf("AUTHENTICATED: %s\n", buffer + strlen(expected_prefix));
        return 0;
    } else {
        fprintf(stderr, "DENIED\n");
        return 2;
    }
}
EOF
    gcc -O2 -Wall /app/oracle.c -o /app/oracle_secure_parser
    rm /app/oracle.c

    # Create optical_token.mp4
    cat << 'EOF' > /tmp/gen_vid.py
import os

bits = "10110010101010111100010101101001"
inputs = []
for b in bits:
    color = "white" if b == '1' else "black"
    inputs.append(f"-f lavfi -i color=c={color}:s=100x100:d=1")

filter_complex = "".join([f"[{i}:v]" for i in range(32)]) + "concat=n=32:v=1:a=0[outv]"

cmd = f"ffmpeg -hide_banner -loglevel error {' '.join(inputs)} -filter_complex \"{filter_complex}\" -map \"[outv]\" -r 1 -y /app/optical_token.mp4"
os.system(cmd)
EOF
    python3 /tmp/gen_vid.py
    rm /tmp/gen_vid.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user