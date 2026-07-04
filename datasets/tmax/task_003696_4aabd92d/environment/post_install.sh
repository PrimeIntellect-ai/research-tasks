apt-get update && apt-get install -y python3 python3-pip gcc
    pip3 install pytest

    mkdir -p /app

    # Create dummy video file
    dd if=/dev/zero of=/app/dataset_video.mp4 bs=1M count=1

    # Create oracle C program
    cat << 'EOF' > /app/oracle_recommend.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef struct {
    float q1, q2, q3, q4;
} Record;

typedef struct {
    float d1, d2;
} Point;

int main() {
    uint32_t N;
    if (fread(&N, sizeof(uint32_t), 1, stdin) != 1) return 0;
    if (N == 0) return 0;

    Point *train = malloc(N * sizeof(Point));
    if (!train) return 1;

    double sum1 = 0, sum2 = 0;

    for (uint32_t i = 0; i < N; i++) {
        Record r;
        if (fread(&r, sizeof(Record), 1, stdin) != 1) {
            free(train);
            return 0;
        }
        float d1 = r.q1 + r.q2;
        float d2 = r.q3 + r.q4;
        train[i].d1 = d1;
        train[i].d2 = d2;
        sum1 += d1;
        sum2 += d2;
    }

    float m1 = sum1 / N;
    float m2 = sum2 / N;

    for (uint32_t i = 0; i < N; i++) {
        train[i].d1 -= m1;
        train[i].d2 -= m2;
    }

    Record r;
    while (fread(&r, sizeof(Record), 1, stdin) == 1) {
        float d1 = r.q1 + r.q2 - m1;
        float d2 = r.q3 + r.q4 - m2;

        uint32_t best_idx = 0;
        float best_dist = -1;

        for (uint32_t i = 0; i < N; i++) {
            float diff1 = d1 - train[i].d1;
            float diff2 = d2 - train[i].d2;
            float dist = diff1 * diff1 + diff2 * diff2;
            if (best_dist < 0 || dist < best_dist) {
                best_dist = dist;
                best_idx = i;
            }
        }
        fwrite(&best_idx, sizeof(uint32_t), 1, stdout);
    }

    free(train);
    return 0;
}
EOF

    gcc -O3 -o /app/oracle_recommend /app/oracle_recommend.c
    chmod +x /app/oracle_recommend

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user