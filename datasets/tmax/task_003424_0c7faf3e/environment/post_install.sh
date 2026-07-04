apt-get update && apt-get install -y python3 python3-pip gcc wget curl tar
pip3 install pytest

mkdir -p /app/bin
mkdir -p /app/construct-2.10.68

cd /tmp
wget https://files.pythonhosted.org/packages/source/c/construct/construct-2.10.68.tar.gz
tar -xzf construct-2.10.68.tar.gz
cp -r construct-2.10.68/* /app/construct-2.10.68/

sed -i '1i raise RuntimeError("Anti-analysis protection triggered")' /app/construct-2.10.68/construct/__init__.py

cat << 'EOF' > /tmp/alert_processor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

int hex_char_to_int(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return -1;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        return 1;
    }
    char *hex_str = argv[1];
    size_t len = strlen(hex_str);
    if (len % 2 != 0) {
        return 1;
    }
    size_t byte_len = len / 2;
    uint8_t *bytes = malloc(byte_len);
    for (size_t i = 0; i < byte_len; i++) {
        int hi = hex_char_to_int(hex_str[i*2]);
        int lo = hex_char_to_int(hex_str[i*2+1]);
        if (hi == -1 || lo == -1) {
            free(bytes);
            return 1;
        }
        bytes[i] = (hi << 4) | lo;
    }

    int found = 0;
    size_t marker_idx = 0;
    for (size_t i = 0; i < byte_len; i++) {
        if (i + 2 < byte_len && bytes[i] == 0x49 && bytes[i+1] == 0x44 && bytes[i+2] == 0x53) {
            found = 1;
            marker_idx = i;
            break;
        }
    }

    if (!found || byte_len - (marker_idx + 3) < 4) {
        printf("NO_ALERT\n");
        free(bytes);
        return 0;
    }

    uint16_t port = (bytes[marker_idx+3] << 8) | bytes[marker_idx+4];
    uint16_t target_hash = (bytes[marker_idx+5] << 8) | bytes[marker_idx+6];

    printf("PORT:%u", port);

    int cracked = 0;
    char c1_ans, c2_ans;
    for (char c1 = 'A'; c1 <= 'Z'; c1++) {
        for (char c2 = 'A'; c2 <= 'Z'; c2++) {
            uint16_t h = ((c1 * 256) + c2) ^ port;
            if (h == target_hash) {
                cracked = 1;
                c1_ans = c1;
                c2_ans = c2;
                break;
            }
        }
        if (cracked) break;
    }

    if (cracked) {
        printf(" - CRACKED:%c%c\n", c1_ans, c2_ans);
    } else {
        printf(" - UNCRACKED\n");
    }

    free(bytes);
    return 0;
}
EOF

gcc -O2 /tmp/alert_processor.c -o /app/bin/alert_processor
chmod +x /app/bin/alert_processor

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user