apt-get update && apt-get install -y python3 python3-pip gcc espeak
    pip3 install pytest

    mkdir -p /app/src /app/lib /app/corpora/clean /app/corpora/evil

    cat << 'EOF' > /app/src/libcwav.c
#include <stdio.h>

int extract_wav(const char* in_path, const char* out_path) {
    FILE* in = fopen(in_path, "rb");
    if (!in) return -1;
    FILE* out = fopen(out_path, "wb");
    if (!out) { fclose(in); return -1; }

    fseek(in, 50, SEEK_SET);
    char buffer[4096];
    size_t bytes;
    while ((bytes = fread(buffer, 1, sizeof(buffer), in)) > 0) {
        fwrite(buffer, 1, bytes, out);
    }

    fclose(in);
    fclose(out);
    return 0;
}
EOF

    # Create 50 bytes of zeros
    dd if=/dev/zero bs=50 count=1 of=/tmp/prefix.bin 2>/dev/null

    # Generate sample
    espeak -w /tmp/sample.wav "initiate the launch sequence"
    cat /tmp/prefix.bin /tmp/sample.wav > /app/sample.cwav

    # Generate clean corpora
    espeak -w /tmp/clean1.wav "testing audio levels"
    cat /tmp/prefix.bin /tmp/clean1.wav > /app/corpora/clean/clean1.cwav
    espeak -w /tmp/clean2.wav "hello world"
    cat /tmp/prefix.bin /tmp/clean2.wav > /app/corpora/clean/clean2.cwav

    # Generate evil corpora
    espeak -w /tmp/evil1.wav "ready to launch"
    cat /tmp/prefix.bin /tmp/evil1.wav > /app/corpora/evil/evil1.cwav
    espeak -w /tmp/evil2.wav "launch the rocket"
    cat /tmp/prefix.bin /tmp/evil2.wav > /app/corpora/evil/evil2.cwav

    # Cleanup
    rm /tmp/*.wav /tmp/prefix.bin

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app