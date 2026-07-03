apt-get update && apt-get install -y python3 python3-pip tesseract-ocr gcc
    pip3 install pytest Pillow

    mkdir -p /app

    # Generate the secret config image
    python3 -c "
from PIL import Image, ImageDraw
img = Image.new('RGB', (200, 50), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10, 10), 'API_KEY: X7f9A2mP', fill=(0, 0, 0))
img.save('/app/secret_config.png')
"

    # Create the buggy server.c skeleton
    cat << 'EOF' > /app/server.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

// Intentionally buggy url_decode
void url_decode(char *dst, const char *src) {
    while (*src) {
        if (*src == '%') {
            int val;
            sscanf(src + 1, "%2x", &val);
            *dst++ = (char)val;
            src += 3;
        } else if (*src == '+') {
            *dst++ = ' ';
            src++;
        } else {
            *dst++ = *src++;
        }
    }
    *dst = '\0';
}

// Intentionally buggy base64_encode
char *base64_encode(const unsigned char *src, size_t len) {
    char *out = malloc(len); // Off-by-one / insufficient allocation
    // Dummy implementation
    strcpy(out, "dummy");
    return out;
}

int main() {
    // Basic socket setup placeholder
    printf("Server starting...\n");
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app