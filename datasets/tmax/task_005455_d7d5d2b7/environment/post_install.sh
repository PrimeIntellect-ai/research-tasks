apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/validator.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// The real key used in production
const unsigned char KEY[4] = {0xDE, 0xAD, 0xBE, 0xEF};

void decrypt(unsigned char* data, int len) {
    for(int i = 0; i < len; i++) {
        data[i] ^= KEY[i % 4];
    }
}

int main(int argc, char** argv) {
    if (argc != 2) return 1;

    char* hex_str = argv[1];
    int len = strlen(hex_str) / 2;
    unsigned char* decrypted = malloc(len + 1);

    for(int i = 0; i < len; i++) {
        sscanf(hex_str + 2*i, "%2hhx", &decrypted[i]);
    }
    decrypted[len] = '\0';

    decrypt(decrypted, len);

    // VULNERABILITY: Only checks the first 16 bytes for path traversal!
    char buffer[17] = {0};
    strncpy(buffer, (char*)decrypted, 16);

    if (strstr(buffer, "../") != NULL) {
        printf("DENIED\n");
        return 1;
    }

    printf("ALLOWED: %s\n", decrypted);
    free(decrypted);
    return 0;
}
EOF

    echo -n "safefile_image.png" > /home/user/sample.txt
    echo -n "adace88998c4d28aa7c1d781bfa0cdd8bbdb" > /home/user/sample.enc

    chmod -R 777 /home/user