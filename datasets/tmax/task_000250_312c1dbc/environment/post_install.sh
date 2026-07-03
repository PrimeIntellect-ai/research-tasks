apt-get update && apt-get install -y python3 python3-pip wget build-essential
    pip3 install pytest

    useradd -m -s /bin/bash user || true
    mkdir -p /app/.backup

    # Download cJSON 1.7.15
    wget https://github.com/DaveGamble/cJSON/archive/refs/tags/v1.7.15.tar.gz -O /tmp/cjson.tar.gz
    tar -xzf /tmp/cjson.tar.gz -C /app
    rm /tmp/cjson.tar.gz

    # Build cJSON for oracle
    cd /app/cJSON-1.7.15
    make

    # Create Oracle code
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "cJSON.h"

typedef struct {
    double timestamp;
} Record;

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    cJSON *json = cJSON_Parse(argv[1]);
    if (!json) return 1;
    int size = cJSON_GetArraySize(json);
    double prev = 0.0;
    for (int i = 0; i < size; i++) {
        cJSON *item = cJSON_GetArrayItem(json, i);
        Record r;
        r.timestamp = item->valuedouble;
        if (i > 0) {
            assert(r.timestamp > prev);
        }
        prev = r.timestamp;
        printf("%.6f\n", r.timestamp);
    }
    cJSON_Delete(json);
    return 0;
}
EOF

    # Build Oracle
    gcc -o /app/oracle_time_series_filter /app/oracle.c -I/app/cJSON-1.7.15 -L/app/cJSON-1.7.15 -lcjson -Wl,-rpath=/app/cJSON-1.7.15 -lm
    chmod +x /app/oracle_time_series_filter

    # Apply Perturbations
    # 1. Move cJSON.c to backup
    mv /app/cJSON-1.7.15/cJSON.c /app/.backup/cJSON.c.bak

    # 2. Break Makefile by removing -lm
    sed -i 's/-lm//g' /app/cJSON-1.7.15/Makefile

    # 3. Clean cJSON build so agent has to rebuild it
    make clean || true

    # Create buggy time_series_filter.c
    cat << 'EOF' > /home/user/time_series_filter.c
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "cJSON.h"

typedef struct {
    float timestamp;
} Record;

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    cJSON *json = cJSON_Parse(argv[1]);
    if (!json) return 1;
    int size = cJSON_GetArraySize(json);
    double prev = 0.0;
    for (int i = 0; i < size; i++) {
        cJSON *item = cJSON_GetArrayItem(json, i);
        Record r;
        r.timestamp = item->valuedouble;
        if (i > 0) {
            assert(r.timestamp > prev);
        }
        prev = r.timestamp;
        printf("%.6f\n", r.timestamp);
    }
    cJSON_Delete(json);
    return 0;
}
EOF

    chmod -R 777 /home/user
    chmod -R 777 /app