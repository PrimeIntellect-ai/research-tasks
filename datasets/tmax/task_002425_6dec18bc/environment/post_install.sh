apt-get update && apt-get install -y python3 python3-pip gcc gdb strace sudo
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Allow passwordless sudo for convenience
    echo "user ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

    # Create the malware source code file
    cat << 'EOF' > /home/user/dropper.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

void decrypt_payload(const char* key) {
    char decrypted_url[128];
    snprintf(decrypted_url, sizeof(decrypted_url), "https://malicious-c2.local/gate/%s/cmd", key);

    // Intentional crash after "decryption" to simulate anti-tamper failure
    int *anti_tamper = NULL;
    *anti_tamper = 0xbadc0de;

    printf("Payload extracted: %s\n", decrypted_url); // Never reached
}

int main() {
    // Environment check
    char *env = getenv("SANDBOX_ENV");
    if (env != NULL) {
        printf("Sandbox detected! Exiting cleanly.\n");
        exit(0);
    }

    int fd = open("/tmp/.sys_mutex_lock", O_RDONLY);
    if (fd < 0) {
        // Segfault to hide true behavior if mutex not found
        int *ptr = NULL;
        *ptr = 1;
    }
    close(fd);

    decrypt_payload("v2_init");

    return 0;
}
EOF

    # Add environment misconfiguration
    echo 'export SANDBOX_ENV=1' >> /home/user/.bashrc

    chmod -R 777 /home/user