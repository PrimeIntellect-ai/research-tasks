apt-get update && apt-get install -y python3 python3-pip tesseract-ocr imagemagick fonts-dejavu gcc
    pip3 install pytest

    mkdir -p /app
    convert -size 400x100 xc:white -font DejaVu-Sans -pointsize 20 -fill black -draw "text 10,50 'Protocol v2 requires MAGIC_HEADER: WsB3nCh_2024!'" /app/protocol_spec.png

    cat << 'EOF' > /app/oracle_ws_normalizer.c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, char *argv[]) {
    if (argc != 2) return 1;
    printf("WsB3nCh_2024!: ");
    for (int i = 0; argv[1][i]; i++) {
        char c = argv[1][i];
        if (c == ' ') c = '_';
        else c = toupper(c);
        putchar(c);
    }
    putchar('\n');
    return 0;
}
EOF
    gcc -O3 /app/oracle_ws_normalizer.c -o /app/oracle_ws_normalizer
    chmod +x /app/oracle_ws_normalizer

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user