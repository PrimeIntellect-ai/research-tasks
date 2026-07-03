apt-get update && apt-get install -y python3 python3-pip gcc libc6-dev
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/forensics

    cat << 'EOF' > /home/user/forensics/auth_vault.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Custom weak hash function
unsigned int custom_hash(const char* pin) {
    unsigned int hash = 0x1337;
    while (*pin) {
        hash = ((hash << 3) & 0xFFFFFFFF) ^ (hash >> 2) ^ (*pin);
        pin++;
    }
    return hash;
}

// Hidden function to dump evidence
void secret_recovery() {
    printf("EVIDENCE_FLAG: CTF{m3m0ry_c0rrupt10n_f0r_th3_w1n}\n");
    exit(0);
}

// Vulnerable logging function
void log_access(const char* user) {
    char buffer[64];
    // CWE-120: Unbounded string copy
    strcpy(buffer, user);
    printf("Access granted for user: %s\n", buffer);
}

int main(int argc, char** argv) {
    if (argc != 3) {
        printf("Usage: %s <username> <pin>\n", argv[0]);
        return 1;
    }

    char* user = argv[1];
    char* pin = argv[2];

    // The hardcoded hash expects the PIN "82941"
    // Hash calculated dynamically: 82941 -> 15720054
    if (custom_hash(pin) == 15720054) {
        log_access(user);
    } else {
        printf("Authentication failed.\n");
    }

    return 0;
}
EOF

    cd /home/user/forensics
    gcc -fno-stack-protector -no-pie -z execstack -o auth_vault auth_vault.c

    chmod -R 777 /home/user