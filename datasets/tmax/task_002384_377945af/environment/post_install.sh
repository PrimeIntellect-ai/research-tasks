apt-get update && apt-get install -y python3 python3-pip git gcc ffmpeg
    pip3 install pytest

    mkdir -p /app

    # Create diagnostic video (4 seconds at 30fps = 120 frames)
    ffmpeg -f lavfi -i color=c=blue:s=320x240:d=4 -r 30 /app/diagnostic_clip.mp4

    # Create working oracle binary
    cat << 'EOF' > /app/working.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    int32_t input_int = atoi(argv[1]);
    uint32_t res = ((input_int ^ 0x5A) << 2) & 0xFFFFFFFF;
    printf("%08X\n", res);
    return 0;
}
EOF
    gcc /app/working.c -o /app/telemetry_encoder_working
    strip /app/telemetry_encoder_working
    rm /app/working.c

    # Set up user and git repo
    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/telemetry_pipeline
    cd /home/user/telemetry_pipeline
    git init
    git config user.email "admin@example.com"
    git config user.name "Admin"

    # Commit 1: Working encoder
    cat << 'EOF' > telemetry_encoder.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    int32_t input_int = atoi(argv[1]);
    uint32_t res = ((input_int ^ 0x5A) << 2) & 0xFFFFFFFF;
    printf("%08X\n", res);
    return 0;
}
EOF
    gcc telemetry_encoder.c -o telemetry_encoder
    git add telemetry_encoder.c telemetry_encoder
    git commit -m "Initial commit: working encoder"

    # Commit 2: Leaked API key
    cat << 'EOF' > config.py
DIAGNOSTIC_API_KEY="AKIA_DIAG_9982AB84C9"
EOF
    git add config.py
    git commit -m "Add config"

    # Commit 3: Remove API key
    cat << 'EOF' > config.py
# API key removed for security
EOF
    git add config.py
    git commit -m "Remove API key"

    # Commit 4: Broken encoder
    cat << 'EOF' > telemetry_encoder.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    int32_t input_int = atoi(argv[1]);
    uint32_t res = ((input_int ^ 0xA5) << 2) & 0xFFFFFFFF;
    printf("%08X\n", res);
    return 0;
}
EOF
    gcc telemetry_encoder.c -o telemetry_encoder
    git add telemetry_encoder.c telemetry_encoder
    git commit -m "Refactor encoder bitwise logic"

    chmod -R 777 /app
    chmod -R 777 /home/user