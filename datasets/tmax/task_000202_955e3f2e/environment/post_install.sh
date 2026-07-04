apt-get update && apt-get install -y python3 python3-pip gcc procps
    pip3 install pytest

    mkdir -p /home/user/src
    cat << 'EOF' > /home/user/src/audit_daemon.c
#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <secret_token>\n", argv[0]);
        return 1;
    }

    // Simulate daemon initialization and binding to a port
    printf("Audit daemon initialized. Listening for events...\n");
    fflush(stdout);

    // Sleep to simulate a long-running background process
    sleep(3600);

    return 0;
}
EOF

    gcc /home/user/src/audit_daemon.c -o /home/user/audit_daemon

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user