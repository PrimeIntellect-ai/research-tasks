apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc
    pip3 install pytest

    # Create directories
    mkdir -p /app
    mkdir -p /opt/oracle
    mkdir -p /home/user

    # Generate telemetry.wav
    ffmpeg -f lavfi -i "sine=frequency=440:duration=5" -ar 8000 -ac 1 /app/telemetry.wav

    # Create and compile oracle
    cat << 'EOF' > /opt/oracle/bayesian_filter_reference.c
#include <stdio.h>

int main() {
    int L = 0;
    int c;
    while ((c = getchar()) != EOF) {
        if (c < 64) {
            L -= 2;
        } else if (c >= 64 && c <= 192) {
            L += 0;
        } else if (c > 192) {
            L += 3;
        }

        if (L < -10) L = -10;
        if (L > 10) L = 10;

        unsigned char out = (L > 0) ? 1 : 0;
        putchar(out);
    }
    return 0;
}
EOF
    gcc -O2 /opt/oracle/bayesian_filter_reference.c -o /opt/oracle/bayesian_filter_reference
    chmod +x /opt/oracle/bayesian_filter_reference

    # Create user
    useradd -m -s /bin/bash user || true

    # Set permissions
    chmod -R 777 /home/user