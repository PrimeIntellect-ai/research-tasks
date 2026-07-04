apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        gcc \
        imagemagick \
        fonts-dejavu-core \
        tesseract-ocr \
        libtesseract-dev
    pip3 install pytest pytesseract Pillow

    mkdir -p /app /verify

    # Generate whiteboard image
    convert -size 800x200 xc:white -font DejaVu-Sans -pointsize 24 -fill black -annotate +20+50 "Algorithm step 1: XOR each char with the key (cycling).\nStep 2: ADD the offset 42.\nOutput as HEX." /app/whiteboard.png

    # Generate crash dump
    dd if=/dev/urandom of=/app/crash.dmp bs=1K count=10 2>/dev/null
    echo -n "XOR_KEY_SIG: S3cr3tM4g1c" >> /app/crash.dmp
    dd if=/dev/urandom bs=1K count=10 >> /app/crash.dmp 2>/dev/null

    # Create and compile oracle.c
    cat << 'EOF' > /verify/oracle.c
#include <stdio.h>
#include <string.h>
int main(int argc, char** argv) {
    if (argc != 2) return 1;
    char* key = "S3cr3tM4g1c";
    int key_len = strlen(key);
    for(int i = 0; i < strlen(argv[1]); i++) {
        unsigned char c = argv[1][i];
        unsigned char k = key[i % key_len];
        unsigned char out = (c ^ k) + 42;
        printf("%02x", out);
    }
    printf("\n");
    return 0;
}
EOF
    gcc -o /verify/oracle.bin /verify/oracle.c

    # Create and compile legacy_tool.c
    cat << 'EOF' > /app/legacy_tool.c
#include <stdio.h>
#include <string.h>
int main(int argc, char** argv) {
    if (argc != 2) return 1;
    if (strlen(argv[1]) > 10) {
        char *crash = NULL;
        *crash = 1; // trigger segfault
    }
    char* key = "S3cr3tM4g1c";
    int key_len = strlen(key);
    for(int i = 0; i < strlen(argv[1]); i++) {
        unsigned char c = argv[1][i];
        unsigned char k = key[i % key_len];
        unsigned char out = (c ^ k) + 42;
        printf("%02x", out);
    }
    printf("\n");
    return 0;
}
EOF
    gcc -o /app/legacy_tool.bin /app/legacy_tool.c
    chmod +x /app/legacy_tool.bin

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user