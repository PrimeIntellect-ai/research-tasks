apt-get update && apt-get install -y python3 python3-pip gcc libc6-dev
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/secret_permissions.txt
FLAG{perm1ss10ns_byp4ss3d_v1a_b0f}
EOF

    cat << 'EOF' > /home/user/validator.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void grant_access() {
    FILE *f = fopen("/home/user/secret_permissions.txt", "r");
    if (f == NULL) {
        printf("Error reading secret.\n");
        exit(1);
    }
    char buf[128];
    fgets(buf, 128, f);
    printf("%s", buf);
    fclose(f);
    exit(0);
}

void process_payload(const unsigned char *decoded_payload) {
    char buffer[64];
    // Vulnerability: strcpy into a 64-byte buffer
    strcpy(buffer, (const char *)decoded_payload);
    printf("Payload processed.\n");
}

int hex_char_to_int(char c) {
    if (c >= '0' && c <= '9') return c - '0';
    if (c >= 'a' && c <= 'f') return c - 'a' + 10;
    if (c >= 'A' && c <= 'F') return c - 'A' + 10;
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <hex_encoded_token>\n", argv[0]);
        return 1;
    }

    size_t len = strlen(argv[1]);
    if (len % 2 != 0) {
        printf("Invalid hex length.\n");
        return 1;
    }

    size_t decoded_len = len / 2;
    unsigned char *decoded = malloc(decoded_len + 1);

    for (size_t i = 0; i < decoded_len; i++) {
        decoded[i] = (hex_char_to_int(argv[1][i*2]) << 4) | hex_char_to_int(argv[1][i*2+1]);
        decoded[i] ^= 0x5A; // XOR decoding
    }
    decoded[decoded_len] = '\0';

    process_payload(decoded);
    free(decoded);

    return 0;
}
EOF

    chmod -R 777 /home/user