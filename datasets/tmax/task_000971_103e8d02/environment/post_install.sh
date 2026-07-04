apt-get update && apt-get install -y python3 python3-pip gcc espeak
    pip3 install pytest

    mkdir -p /app

    # Generate audio briefing
    espeak -w /app/briefing.wav "Attention log analyst. We need to standardize our metrics. Reshape the wide system metrics into long format using the exact metric names: cpu, mem, disk, and net. Bucket the logs into sixty-second tumbling windows based on the timestamp. For each user and metric combination, calculate the rolling sum over a three-minute window—that is, the current sixty-second bucket plus the previous two buckets. Output the bucket start time, user ID, metric name, and the rolling sum."

    # Create oracle C program
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RECORDS 100000

typedef struct {
    long long bucket;
    char user_id[32];
    double cpu;
    double mem;
    double disk;
    double net;
} Record;

Record records[MAX_RECORDS];
int num_records = 0;

int find_or_create_record(long long bucket, const char* user_id) {
    for (int i = 0; i < num_records; i++) {
        if (records[i].bucket == bucket && strcmp(records[i].user_id, user_id) == 0) {
            return i;
        }
    }
    records[num_records].bucket = bucket;
    strcpy(records[num_records].user_id, user_id);
    records[num_records].cpu = 0;
    records[num_records].mem = 0;
    records[num_records].disk = 0;
    records[num_records].net = 0;
    return num_records++;
}

int cmp_records(const void* a, const void* b) {
    Record* ra = (Record*)a;
    Record* rb = (Record*)b;
    if (ra->bucket != rb->bucket) {
        return (ra->bucket > rb->bucket) - (ra->bucket < rb->bucket);
    }
    return strcmp(ra->user_id, rb->user_id);
}

int main() {
    long long ts;
    char uid[32];
    double c, m, d, n;
    while (scanf("%lld %31s %lf %lf %lf %lf", &ts, uid, &c, &m, &d, &n) == 6) {
        long long b = (ts / 60) * 60;
        int idx = find_or_create_record(b, uid);
        records[idx].cpu += c;
        records[idx].mem += m;
        records[idx].disk += d;
        records[idx].net += n;
    }

    qsort(records, num_records, sizeof(Record), cmp_records);

    for (int i = 0; i < num_records; i++) {
        double r_cpu = records[i].cpu;
        double r_mem = records[i].mem;
        double r_disk = records[i].disk;
        double r_net = records[i].net;

        for (int j = 0; j < i; j++) {
            if (strcmp(records[j].user_id, records[i].user_id) == 0) {
                if (records[j].bucket == records[i].bucket - 60 || records[j].bucket == records[i].bucket - 120) {
                    r_cpu += records[j].cpu;
                    r_mem += records[j].mem;
                    r_disk += records[j].disk;
                    r_net += records[j].net;
                }
            }
        }

        printf("%lld %s cpu %.2f\n", records[i].bucket, records[i].user_id, r_cpu);
        printf("%lld %s disk %.2f\n", records[i].bucket, records[i].user_id, r_disk);
        printf("%lld %s mem %.2f\n", records[i].bucket, records[i].user_id, r_mem);
        printf("%lld %s net %.2f\n", records[i].bucket, records[i].user_id, r_net);
    }
    return 0;
}
EOF

    gcc -O3 /app/oracle.c -o /app/oracle_log_processor
    rm /app/oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user