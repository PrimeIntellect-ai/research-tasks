apt-get update && apt-get install -y python3 python3-pip gcc gdb binutils
    pip3 install pytest

    mkdir -p /home/user

    cat << 'EOF' > /home/user/vault_checker.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
    FILE *f = fopen("/home/user/payload.bin", "rb");
    if (!f) {
        printf("Error: Could not open /home/user/payload.bin\n");
        return 1;
    }

    char buf[32] = {0};
    size_t bytes_read = fread(buf, 1, 25, f);
    fclose(f);

    if (bytes_read < 25) {
        printf("Access Denied: Payload too short.\n");
        return 1;
    }

    // Custom decoding loop: XOR with a rolling key
    for (int i = 0; i < 25; i++) {
        buf[i] = buf[i] ^ ((i * 3 + 7) & 0xFF);
    }

    // Check against expected decoded string
    if (strncmp(buf, "AUTH_GRANTED_ADMIN_XYZ123", 25) == 0) {
        printf("FLAG{R3v3rs3_3ng1n33r1ng_M4st3r}\n");
    } else {
        printf("Access Denied: Invalid Payload.\n");
    }

    return 0;
}
EOF

    gcc -O0 -fno-stack-protector /home/user/vault_checker.c -o /home/user/vault_checker
    strip /home/user/vault_checker
    rm /home/user/vault_checker.c

    useradd -m -s /bin/bash user || true
    chown user:user /home/user/vault_checker
    chmod 755 /home/user/vault_checker
    chmod -R 777 /home/user