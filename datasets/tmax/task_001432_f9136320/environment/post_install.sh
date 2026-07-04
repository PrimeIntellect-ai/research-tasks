apt-get update && apt-get install -y python3 python3-pip tesseract-ocr imagemagick gcc strace
    pip3 install pytest

    mkdir -p /app
    mkdir -p /home/user/service

    # Create the watermark image
    convert -size 400x100 xc:white -pointsize 24 -fill black -draw "text 10,50 'MASTER_OFFSET=42'" /app/watermark_config.png

    # Create Oracle C code and compile it
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 0;
    int c;
    while ((c = fgetc(f)) != EOF) {
        if (c == 0) continue;
        printf("%02X", (c + 42) & 0xFF);
    }
    printf("\n");
    fclose(f);
    return 0;
}
EOF
    gcc -O2 /app/oracle.c -o /app/oracle_watermark_extractor
    strip /app/oracle_watermark_extractor
    rm /app/oracle.c

    # Create buggy C code
    cat << 'EOF' > /home/user/service/parser.c
#include <stdio.h>

void process(unsigned char *buf, int len, int offset) {
    int i = 0;
    while (i <= len) { // off-by-one error
        if (buf[i] == 0) {
            // missing i++ causes infinite loop on null bytes
            continue;
        }
        printf("%02X", (buf[i] + offset) & 0xFF);
        i++;
    }
    printf("\n");
}
EOF

    # Create buggy Python code
    cat << 'EOF' > /home/user/service/extractor.py
import sys
import ctypes
import os

def run():
    if len(sys.argv) < 2:
        return
    # Bug: offset is hardcoded and not extracted from image
    offset = 0
    with open(sys.argv[1], 'rb') as f:
        data = f.read()

    so_path = os.path.join(os.path.dirname(__file__), 'parser.so')
    if not os.path.exists(so_path):
        print("Please compile parser.c to parser.so first")
        sys.exit(1)

    lib = ctypes.CDLL(so_path)
    lib.process.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
    lib.process(data, len(data), offset)

if __name__ == '__main__':
    run()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app