apt-get update && apt-get install -y python3 python3-pip gcc imagemagick tesseract-ocr fonts-dejavu-core
    pip3 install pytest

    mkdir -p /app

    # Create oracle source
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <string.h>
int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    char *input = argv[1];
    int len = strlen(input);
    for (int i = 0; i < len; i++) {
        unsigned char c = input[i];
        unsigned char out = (c ^ 0x5F) + (i * 7);
        printf("%02X", out);
    }
    printf("\n");
    return 0;
}
EOF

    gcc -o /app/oracle_token_gen /app/oracle.c
    chmod +x /app/oracle_token_gen

    # Generate the image
    cat << 'EOF' > /app/image_content.txt
// Backdoor Token Derivation Function
// Apply to each character of the username
unsigned char out_byte = (username[i] ^ 0x5F) + (i * 7);
EOF

    # Fix ImageMagick policy to allow label
    sed -i 's/rights="none" pattern="LABEL"/rights="read|write" pattern="LABEL"/g' /etc/ImageMagick-6/policy.xml || true
    sed -i 's/rights="none" pattern="@\*"/rights="read|write" pattern="@\*"/g' /etc/ImageMagick-6/policy.xml || true

    convert -background white -fill black -font DejaVu-Sans-Mono -pointsize 24 label:@"/app/image_content.txt" /app/evidence.png

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user