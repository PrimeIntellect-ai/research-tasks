apt-get update && apt-get install -y python3 python3-pip python3-venv gcc upx-ucl binutils
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/telemetry_parser.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <unistd.h>

char dummy[65536] = {1}; // Padding to ensure UPX compressibility

int main() {
    uint8_t type;
    uint16_t length;
    printf("{\"records\": [");
    int first = 1;
    while (fread(&type, 1, 1, stdin) == 1) {
        if (fread(&length, 2, 1, stdin) != 1) break;
        uint16_t len = (length >> 8) | (length << 8); // Big endian
        if (type == 0xFF) {
            char *buf = malloc(len);
            fread(buf, 1, len, stdin);
            free(buf);
            continue;
        }
        char *val = malloc(len + 1);
        fread(val, 1, len, stdin);
        val[len] = 0;
        if (!first) printf(", ");
        if (type == 1) {
            printf("{\"type\": 1, \"value\": \"%s\"}", val);
        } else if (type == 2) {
            long v = 0;
            for(int i=0; i<len; i++) v = (v<<8) | (uint8_t)val[i];
            printf("{\"type\": 2, \"value\": %ld}", v);
        }
        free(val);
        first = 0;
    }
    printf("]}\n");
    return 0;
}
EOF

    gcc -O0 -o /app/telemetry_parser /app/telemetry_parser.c
    strip /app/telemetry_parser
    upx /app/telemetry_parser || true
    rm /app/telemetry_parser.c

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/project

    cat << 'EOF' > /home/user/project/requirements.txt
Flask==2.0.1
Werkzeug==3.0.0
gunicorn==20.1.0
EOF

    printf "\x01\x00\x04test\x02\x00\x02\x10\x20" > /home/user/valid_telemetry.dat
    printf "\x01\x00\x04data\xff\xff\xff" > /home/user/crashing_telemetry.dat
    head -c 10000 /dev/urandom >> /home/user/crashing_telemetry.dat

    chown -R user:user /home/user
    chmod -R 777 /home/user