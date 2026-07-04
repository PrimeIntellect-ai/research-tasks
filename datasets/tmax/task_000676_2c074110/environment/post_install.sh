apt-get update && apt-get install -y python3 python3-pip tesseract-ocr gcc python3-pil
pip3 install pytest

mkdir -p /app

cat << 'EOF' > /app/crc.c
#include <stdint.h>

uint16_t compute_crc(uint16_t current_crc, uint8_t data, uint16_t poly) {
    uint8_t bits[8];
    uint16_t crc = current_crc;

    // INTENTIONAL BUG: Loop goes up to 8 (out of bounds)
    for(int i=0; i<=8; i++) {
        bits[i] = (data >> (7 - i)) & 1;
    }

    for(int i=0; i<8; i++) {
        uint16_t bit = bits[i];
        uint16_t c15 = (crc >> 15) & 1;
        crc <<= 1;
        if (c15 ^ bit) {
            crc ^= poly;
        }
    }
    return crc;
}
EOF

cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

uint16_t compute_crc(uint16_t current_crc, uint8_t data, uint16_t poly) {
    uint16_t crc = current_crc;
    for(int i=0; i<8; i++) {
        uint16_t bit = (data >> (7 - i)) & 1;
        uint16_t c15 = (crc >> 15) & 1;
        crc <<= 1;
        if (c15 ^ bit) {
            crc ^= poly;
        }
    }
    return crc;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    char* hex = argv[1];
    int len = strlen(hex);
    uint8_t A = 0;
    uint16_t CRC = 0xFFFF;
    uint16_t POLY = 0x1021;
    for (int i=0; i<len; i+=4) {
        if (i+3 >= len) break;
        char op_str[3] = {hex[i], hex[i+1], 0};
        char val_str[3] = {hex[i+2], hex[i+3], 0};
        uint8_t op = strtol(op_str, NULL, 16);
        uint8_t val = strtol(val_str, NULL, 16);
        if (op == 1) A += val;
        else if (op == 2) A -= val;
        else if (op == 3) A ^= val;
        CRC = compute_crc(CRC, A, POLY);
    }
    printf("%04X\n", CRC);
    return 0;
}
EOF

gcc /app/oracle.c -o /app/oracle
chmod +x /app/oracle

cat << 'EOF' > /tmp/gen_img.py
import PIL.Image
import PIL.ImageDraw
img = PIL.Image.new('RGB', (400, 200), color=(255, 255, 255))
d = PIL.ImageDraw.Draw(img)
text = "VM SPECIFICATION V1.0\nINIT=0xFFFF\nPOLY=0x1021\nOPCODES:\n01: ADD\n02: SUB\n03: XOR"
d.text((10,10), text, fill=(0,0,0))
img.save('/app/spec.png')
EOF

python3 /tmp/gen_img.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app