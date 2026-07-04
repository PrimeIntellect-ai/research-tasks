apt-get update && apt-get install -y \
        python3 python3-pip \
        ffmpeg \
        squashfuse \
        squashfs-tools \
        socat \
        espeak \
        gcc \
        g++ \
        make \
        cmake \
        git \
        wget

    pip3 install pytest

    mkdir -p /app

    # Generate voicenote
    espeak -w /app/voicenote.wav "Listen carefully. Set up the monitor on the mount point /home/user/data_mount. The quota threshold is exactly 85 percent. Port forward the alert endpoint to port 8080. The parser needs to output the filtered log."

    # Install whisper.cpp
    cd /opt
    git clone https://github.com/ggerganov/whisper.cpp.git
    cd whisper.cpp
    make
    # Download a small model
    bash ./models/download-ggml-model.sh tiny.en
    ln -s /opt/whisper.cpp/main /usr/local/bin/whisper

    # Create oracle parser
    cat << 'EOF' > /app/oracle_parser.c
#include <stdio.h>
#include <string.h>

int main() {
    char line[256];
    char device[128];
    long long used, total;
    while (fgets(line, sizeof(line), stdin)) {
        if (sscanf(line, "%127s %lld %lld", device, &used, &total) == 3) {
            if (total > 0) {
                long long pct = (used * 100) / total;
                if (pct > 85) {
                    printf("ALERT: [%s] usage is %lld%%\n", device, pct);
                }
            }
        }
    }
    return 0;
}
EOF
    gcc -O2 /app/oracle_parser.c -o /app/oracle_parser
    rm /app/oracle_parser.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user