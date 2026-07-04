apt-get update && apt-get install -y python3 python3-pip gcc make coreutils
    pip3 install --default-timeout=100 pytest

    mkdir -p /app

    # Generate users.csv
    python3 -c "
import random
with open('/app/users.csv', 'w') as f:
    for i in range(1, 10001):
        f.write(f'{i},{random.randint(1, 100)}\n')
"

    # Create data_gen.c
    cat << 'EOF' > /app/data_gen.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#pragma pack(push, 1)
struct Record {
    uint64_t timestamp;
    uint32_t user_id;
    double value;
    uint8_t hash[16];
};
#pragma pack(pop)

int main() {
    srand(42);
    struct Record r;
    uint8_t history[5000][16];
    int hist_idx = 0;
    int hist_count = 0;

    for (int i = 0; i < 2000000; i++) {
        r.timestamp = i;
        r.user_id = (rand() % 10000) + 1;
        r.value = (double)rand() / RAND_MAX * 100.0;

        if (hist_count > 0 && rand() % 10 == 0) {
            int dup_idx = rand() % hist_count;
            for(int j=0; j<16; j++) r.hash[j] = history[dup_idx][j];
        } else {
            for(int j=0; j<16; j++) r.hash[j] = rand() % 256;
            for(int j=0; j<16; j++) history[hist_idx][j] = r.hash[j];
            hist_idx = (hist_idx + 1) % 5000;
            if (hist_count < 5000) hist_count++;
        }
        fwrite(&r, sizeof(struct Record), 1, stdout);
    }
    return 0;
}
EOF

    gcc -O3 /app/data_gen.c -o /app/data_gen
    strip /app/data_gen

    # Create processor.c for golden.csv
    cat << 'EOF' > /app/processor.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#pragma pack(push, 1)
struct Record {
    uint64_t timestamp;
    uint32_t user_id;
    double value;
    uint8_t hash[16];
};
#pragma pack(pop)

int group_map[10001] = {0};
double window[10001][10] = {0};
int window_idx[10001] = {0};
int window_cnt[10001] = {0};

uint8_t hash_window[5000][16] = {0};
int hash_idx = 0;
int hash_cnt = 0;

int main() {
    FILE *f = fopen("/app/users.csv", "r");
    char line[256];
    while (fgets(line, sizeof(line), f)) {
        int u, g;
        if (sscanf(line, "%d,%d", &u, &g) == 2) {
            if (u >= 0 && u <= 10000) group_map[u] = g;
        }
    }
    fclose(f);

    struct Record r;
    FILE *out = fopen("/app/golden.csv", "w");
    while (fread(&r, sizeof(struct Record), 1, stdin) == 1) {
        int dup = 0;
        for (int i = 0; i < hash_cnt; i++) {
            if (memcmp(hash_window[i], r.hash, 16) == 0) {
                dup = 1;
                break;
            }
        }
        if (dup) continue;

        memcpy(hash_window[hash_idx], r.hash, 16);
        hash_idx = (hash_idx + 1) % 5000;
        if (hash_cnt < 5000) hash_cnt++;

        int g = 0;
        if (r.user_id >= 0 && r.user_id <= 10000) g = group_map[r.user_id];

        window[g][window_idx[g]] = r.value;
        window_idx[g] = (window_idx[g] + 1) % 10;
        if (window_cnt[g] < 10) window_cnt[g]++;

        double sum = 0;
        for (int i = 0; i < window_cnt[g]; i++) sum += window[g][i];
        double sma = sum / window_cnt[g];

        fprintf(out, "%lu,%d,%.4f\n", r.timestamp, g, sma);
    }
    fclose(out);
    return 0;
}
EOF

    gcc -O3 /app/processor.c -o /app/processor
    /app/data_gen | /app/processor

    rm /app/data_gen.c /app/processor.c /app/processor

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app