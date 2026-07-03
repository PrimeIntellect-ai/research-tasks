apt-get update && apt-get install -y python3 python3-pip gcc make gdb xxd
pip3 install pytest

mkdir -p /home/user/sensor_pipeline
cd /home/user/sensor_pipeline

# 1. Create signal.h (missing packed attribute)
cat << 'EOF' > signal.h
#ifndef SIGNAL_H
#define SIGNAL_H
#include <stdint.h>

struct SensorRecord {
    uint8_t type;
    uint32_t id;
    float value;
};

void process_record(struct SensorRecord *rec);

#endif
EOF

# 2. Create signal.c
cat << 'EOF' > signal.c
#include "signal.h"
#include <math.h>

void process_record(struct SensorRecord *rec) {
    rec->value = roundf(rec->value * 100.0f) / 100.0f;
}
EOF

# 3. Create main.c (contains segfault bug)
cat << 'EOF' > main.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "signal.h"

int main(int argc, char **argv) {
    if (argc != 3) {
        printf("Usage: %s <input.csv> <output.bin>\n", argv[0]);
        return 1;
    }

    FILE *in = fopen(argv[1], "r");
    if (!in) return 1;

    FILE *out = fopen(argv[2], "wb");
    if (!out) return 1;

    char line[256];
    while (fgets(line, sizeof(line), in)) {
        if (line[0] == '\n' || line[0] == '\r') continue;

        struct SensorRecord rec;
        memset(&rec, 0, sizeof(rec));

        char *token = strtok(line, ",");
        rec.type = (uint8_t)atoi(token);

        token = strtok(NULL, ",");
        rec.id = (uint32_t)atoi(token);

        token = strtok(NULL, ",");
        rec.value = (float)atof(token);

        process_record(&rec);

        fwrite(&rec, sizeof(struct SensorRecord), 1, out);
    }

    fclose(in);
    fclose(out);
    return 0;
}
EOF

# 4. Create Makefile (missing signal.c and -lm)
cat << 'EOF' > Makefile
CC=gcc
CFLAGS=-g -Wall

SRCS=main.c
OBJS=$(SRCS:.c=.o)

sensor_proc: $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

clean:
	rm -f *.o sensor_proc output.bin
EOF

# 5. Create input.csv (contains a malformed line to trigger segfault)
cat << 'EOF' > input.csv
1,1001,45.234
2,1002,12.891
MALFORMED_LINE_WITHOUT_COMMAS
3,1003,78.119
EOF

# 6. Generate golden expected.bin
cat << 'EOF' > expected_gen.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

struct __attribute__((packed)) SensorRecord {
    uint8_t type;
    uint32_t id;
    float value;
};

int main() {
    FILE *out = fopen("expected.bin", "wb");
    struct SensorRecord recs[3] = {
        {1, 1001, 45.23f},
        {2, 1002, 12.89f},
        {3, 1003, 78.12f}
    };
    fwrite(recs, sizeof(struct SensorRecord), 3, out);
    fclose(out);
    return 0;
}
EOF
gcc -o expected_gen expected_gen.c -lm
./expected_gen
rm expected_gen.c expected_gen

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user