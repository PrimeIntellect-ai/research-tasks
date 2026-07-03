apt-get update && apt-get install -y python3 python3-pip gcc netcat build-essential
    pip3 install pytest

    mkdir -p /home/user

    cat << 'EOF' > /home/user/auth_proxy.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SECRET "FLAG{c3rt_byp4ss_s3cc0mp_fw}"
#define MAGIC 0xC0DEBABE

struct Certificate {
    uint32_t magic;
    uint8_t alg; // 1 = RSA-SHA256, 0 = NONE
    uint16_t target_port;
    uint8_t signature[32];
} __attribute__((packed));

void apply_firewall_policy(uint16_t port) {
    // Simulated egress firewall policy
    if (port < 8000 || port > 8005) {
        fprintf(stderr, "Policy Violation: Port %d blocked by internal firewall rules.\n", port);
        exit(1);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <token_file>\n", argv[0]);
        return 1;
    }

    FILE *f = fopen(argv[1], "rb");
    if (!f) {
        perror("fopen");
        return 1;
    }

    struct Certificate cert;
    if (fread(&cert, 1, sizeof(cert), f) != sizeof(cert)) {
        fprintf(stderr, "Invalid token size.\n");
        fclose(f);
        return 1;
    }
    fclose(f);

    if (cert.magic != MAGIC) {
        fprintf(stderr, "Invalid magic bytes.\n");
        return 1;
    }

    // Vulnerability: alg=0 bypasses signature check
    if (cert.alg != 0) {
        // Mock signature check
        fprintf(stderr, "Signature verification failed for alg %d.\n", cert.alg);
        return 1;
    }

    apply_firewall_policy(cert.target_port);

    // Isolated transmission
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in serv_addr;
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(cert.target_port);
    inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr);

    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        fprintf(stderr, "Connection failed to port %d.\n", cert.target_port);
        return 1;
    }

    send(sock, SECRET, strlen(SECRET), 0);
    close(sock);
    printf("Authentication bypass successful. Secret transmitted.\n");

    return 0;
}
EOF

    gcc /home/user/auth_proxy.c -o /home/user/auth_proxy
    chmod +x /home/user/auth_proxy

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user