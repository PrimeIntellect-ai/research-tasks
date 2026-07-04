apt-get update && apt-get install -y python3 python3-pip gcc make gdb valgrind diffutils
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/sensor_processor
    mkdir -p /home/user/data

    cat << 'EOF' > /home/user/sensor_processor/main.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_RECORDS 1000

typedef struct {
    int id;
    double raw_value;
} Record;

void process_data(Record* records, int count, const char* out_file) {
    FILE* fp = fopen(out_file, "w");
    if (!fp) return;

    for (int i = 0; i < count; i++) {
        // BUG 2: Precision loss here. 'float' is used instead of 'double'
        float intermediate = records[i].raw_value * 3.14159265358979323846;
        double final_val = (double)intermediate / 2.0;

        fprintf(fp, "%d,%.6f\n", records[i].id, final_val);
    }
    fclose(fp);
}

int main(int argc, char** argv) {
    if (argc != 3) {
        printf("Usage: %s <input.csv> <output.csv>\n", argv[0]);
        return 1;
    }

    FILE* fp = fopen(argv[1], "r");
    if (!fp) {
        perror("Failed to open input");
        return 1;
    }

    // BUG 1: Static array of 1000, but input has 2000 records
    Record records[MAX_RECORDS];
    int count = 0;
    char line[256];

    while (fgets(line, sizeof(line), fp)) {
        int id;
        double val;
        if (sscanf(line, "%d,%lf", &id, &val) == 2) {
            records[count].id = id;
            records[count].raw_value = val;
            count++; // This will write out of bounds and segfault
        }
    }
    fclose(fp);

    process_data(records, count, argv[2]);
    return 0;
}
EOF

    cat << 'EOF' > /home/user/sensor_processor/Makefile
CC=gcc
CFLAGS=-O2 -Wall

all: sensor_processor

sensor_processor: main.c
	$(CC) $(CFLAGS) -o sensor_processor main.c

clean:
	rm -f sensor_processor
EOF

    cat << 'EOF' > /home/user/sensor_processor/gen_data.c
#include <stdio.h>

int main() {
    FILE* in = fopen("/home/user/data/input.csv", "w");
    FILE* out = fopen("/home/user/data/expected_output.csv", "w");

    for(int i=0; i<2000; i++) {
        double raw = i * 1.1234567;
        fprintf(in, "%d,%.7f\n", i, raw);

        // Correct calculation
        double intermediate = raw * 3.14159265358979323846;
        double final_val = intermediate / 2.0;
        fprintf(out, "%d,%.6f\n", i, final_val);
    }

    fclose(in);
    fclose(out);
    return 0;
}
EOF

    gcc /home/user/sensor_processor/gen_data.c -o /home/user/sensor_processor/gen_data
    /home/user/sensor_processor/gen_data
    rm /home/user/sensor_processor/gen_data /home/user/sensor_processor/gen_data.c

    chown -R user:user /home/user/sensor_processor /home/user/data
    chmod -R 777 /home/user