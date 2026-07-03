apt-get update && apt-get install -y python3 python3-pip tesseract-ocr gcc imagemagick fonts-dejavu-core
    pip3 install pytest pillow

    mkdir -p /app

    # Generate the image with the hex dump
    python3 -c "
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (800, 100), color = (255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10,10), '0A 01 FF FF 41 41 41 41 41 41 41 41 41 41 41 41', fill=(0,0,0))
img = img.resize((1600, 200), Image.NEAREST)
img.save('/app/packet_dump.png')
"

    # Create the vulnerable C parser
    cat << 'EOF' > /app/parser.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void parse_packet(const char* filepath) {
    FILE *f = fopen(filepath, "rb");
    if(!f) return;

    unsigned char header[2];
    fread(header, 1, 2, f);

    short length;
    fread(&length, 1, sizeof(short), f);

    // VULNERABILITY: signed integer comparison bypass
    if (length < 1024) {
        char *buf = malloc(1024);
        // VULNERABILITY: implicit cast to size_t (unsigned), so -1 becomes 0xFFFFFFFF
        fread(buf, 1, length, f); 
        free(buf);
    }
    fclose(f);
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    parse_packet(argv[1]);
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app