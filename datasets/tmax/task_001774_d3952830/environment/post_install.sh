apt-get update && apt-get install -y python3 python3-pip gcc gdb ltrace strace
    pip3 install pytest

    mkdir -p /app

    # Create oracle_bin source
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdint.h>
#include <string.h>

int main() {
    uint32_t h = 0x811c9dc5;
    double f = 0.5;
    char buf[4096];
    if (fgets(buf, sizeof(buf), stdin)) {
        size_t len = strlen(buf);
        if (len > 0 && buf[len-1] == '\n') buf[len-1] = '\0';
        len = strlen(buf);
        for (size_t i = 0; i < len; i++) {
            h = (h ^ (uint8_t)buf[i]) * 0x01000193;
            f = 3.9 * f * (1.0 - f);
        }
    }
    uint32_t mod = (uint32_t)(f * 1000000.0);
    printf("0x%08x\n", h ^ mod);
    return 0;
}
EOF

    # Create suspicious_bin source
    cat << 'EOF' > /app/suspicious.c
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>

uint32_t h = 0x811c9dc5;
double f = 0.5;
char buf[4096];

void* worker(void* arg) {
    size_t start = (size_t)arg;
    for (size_t i = start; i < start + 1 && buf[i] != '\0'; i++) {
        h = (h ^ (uint8_t)buf[i]) * 0x01000193;
        f = 3.9 * f * (1.0 - f);
    }
    return NULL;
}

int main() {
    if (fgets(buf, sizeof(buf), stdin)) {
        size_t len = strlen(buf);
        if (len > 0 && buf[len-1] == '\n') buf[len-1] = '\0';
        len = strlen(buf);
        pthread_t threads[4096];
        for (size_t i = 0; i < len; i++) {
            pthread_create(&threads[i], NULL, worker, (void*)i);
        }
        for (size_t i = 0; i < len; i++) {
            pthread_join(threads[i], NULL);
        }
    }
    uint32_t mod = (uint32_t)(f * 1000000.0);
    printf("0x%08x\n", h ^ mod);
    return 0;
}
EOF

    gcc -O2 /app/oracle.c -o /app/oracle_bin
    gcc -O2 /app/suspicious.c -o /app/suspicious_bin -lpthread
    strip /app/suspicious_bin

    rm /app/oracle.c /app/suspicious.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user