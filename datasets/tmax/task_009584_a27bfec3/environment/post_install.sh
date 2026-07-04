apt-get update && apt-get install -y python3 python3-pip gcc libc6-dev
    pip3 install pytest

    mkdir -p /home/user
    cat << 'EOF' > /home/user/latency_monitor.c
#include <stdio.h>
#include <stdlib.h>

int cmp(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <file>\n", argv[0]);
        return 1;
    }
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    int latencies[1000];
    int count = 0;
    while (fscanf(f, "%d", &latencies[count]) == 1 && count < 1000) {
        count++;
    }
    fclose(f);

    if (count == 0) return 0;

    // BUG: sorts the entire 1000-element array including uninitialized garbage
    qsort(latencies, 1000, sizeof(int), cmp);

    int p99_idx = (int)(count * 0.99);
    printf("Count: %d, P99 Latency: %d\n", count, latencies[p99_idx]);
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user