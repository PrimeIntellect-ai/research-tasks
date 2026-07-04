apt-get update && apt-get install -y python3 python3-pip gcc golang-go
    pip3 install pytest

    mkdir -p /app
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define MAX_RECORDS 100000

typedef struct {
    long timestamp;
    char sensor_id[64];
    double value;
} Record;

int cmp_record(const void *a, const void *b) {
    Record *ra = (Record *)a;
    Record *rb = (Record *)b;
    int cmp = strcmp(ra->sensor_id, rb->sensor_id);
    if (cmp != 0) return cmp;
    if (ra->timestamp < rb->timestamp) return -1;
    if (ra->timestamp > rb->timestamp) return 1;
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;
    char line[256];
    Record *records = malloc(sizeof(Record) * MAX_RECORDS);
    int count = 0;

    if (fgets(line, sizeof(line), f) == NULL) {
        free(records);
        printf("CLEAN\n");
        return 0;
    }

    while (fgets(line, sizeof(line), f) && count < MAX_RECORDS) {
        char *ts_str = strtok(line, ",");
        char *id_str = strtok(NULL, ",");
        char *val_str = strtok(NULL, "\r\n");
        if (ts_str && id_str && val_str) {
            records[count].timestamp = atol(ts_str);
            strncpy(records[count].sensor_id, id_str, 63);
            records[count].sensor_id[63] = '\0';
            records[count].value = atof(val_str);
            count++;
        }
    }
    fclose(f);

    qsort(records, count, sizeof(Record), cmp_record);

    for (int i = 1; i < count; i++) {
        if (strcmp(records[i].sensor_id, records[i-1].sensor_id) == 0) {
            if (fabs(records[i].value - records[i-1].value) > 42.5) {
                printf("EVIL\n");
                free(records);
                return 1;
            }
        }
    }
    printf("CLEAN\n");
    free(records);
    return 0;
}
EOF

    gcc -O3 -o /app/telemetry_oracle /app/oracle.c -lm
    strip /app/telemetry_oracle
    rm /app/oracle.c

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/data

    cat << 'EOF' > /home/user/data/sensors.csv
timestamp,sensor_A,sensor_B
1600000000,10.0,20.0
1600000010,12.0,21.0
EOF

    cat << 'EOF' > /home/user/data/sensors.json
[
  {"timestamp": 1600000000, "sensor_C": 10.5, "sensor_D": -3.2},
  {"timestamp": 1600000010, "sensor_C": 11.5, "sensor_D": -2.2}
]
EOF

    chmod -R 777 /home/user