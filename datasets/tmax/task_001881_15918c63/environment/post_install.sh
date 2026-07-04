apt-get update && apt-get install -y python3 python3-pip gcc make espeak
    pip3 install pytest

    # Create app directory
    mkdir -p /app

    # Create the oracle C source and compile it
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
int main() {
    int c;
    while ((c = getchar()) != EOF) {
        putchar(c ^ 0x42);
    }
    return 0;
}
EOF
    gcc -O2 /app/oracle.c -o /app/oracle_cleaner
    chmod +x /app/oracle_cleaner

    # Generate the clean audio and corrupt it with the oracle (XOR is its own inverse)
    espeak -w /tmp/clean.wav "project blackbird activated"
    cat /tmp/clean.wav | /app/oracle_cleaner > /app/voicemail.wav

    # Create user and directories
    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/src
    mkdir -p /home/user/bin

    # Create the buggy C source
    cat << 'EOF' > /home/user/src/audio_cleaner.c
#include <stdio.h>
#include <stdlib.h>

int main() {
    // BUG: Fixed size buffer, will overflow on large inputs
    int *buf = malloc(1024 * sizeof(int));
    int c;
    int i = 0;

    while ((c = getchar()) != EOF) {
        buf[i++] = c ^ 0x42;
    }

    // BUG: Off-by-one error in loop condition
    for (int j = 0; j <= i; j++) {
        putchar(buf[j]);
    }

    // BUG: Memory leak (missing free)
    return 0;
}
EOF

    chmod -R 777 /home/user