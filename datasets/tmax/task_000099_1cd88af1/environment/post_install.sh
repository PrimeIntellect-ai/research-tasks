apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest

    mkdir -p /app/libcsv_ext-1.0.0

    cat << 'EOF' > /app/libcsv_ext-1.0.0/csv.h
#ifndef CSV_H
#define CSV_H
void dummy_csv_func();
#endif
EOF

    cat << 'EOF' > /app/libcsv_ext-1.0.0/csv.c
#include "csv.h"
void dummy_csv_func() {}
EOF

    cat << 'EOF' > /app/libcsv_ext-1.0.0/Makefile
CC=gcc
CFLAGS=-Wall -O2

all: libcsv_ext.a

libcsv_ext.a: csv.c
	$(CC) $(CFLAGS) -c csv.c
	ar rcs libcsv_ext.a cvs.o

clean:
	rm -f *.o *.a
EOF

    cat << 'EOF' > /app/oracle_processor.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char line[256];
    while (fgets(line, sizeof(line), stdin)) {
        int id;
        float value;
        char category;
        float model_score;

        if (sscanf(line, "%d,%f,%c,%f", &id, &value, &category, &model_score) == 4) {
            if (id < 0) continue;
            float value_squared = value * value;
            int enc = 0;
            if (category == 'A') enc = 1;
            else if (category == 'B') enc = 2;
            else if (category == 'C') enc = 3;

            const char* status = (model_score > 0.5f) ? "VALID" : "INVALID";
            printf("%d,%f,%d,%s\n", id, value_squared, enc, status);
        }
    }
    return 0;
}
EOF

    gcc -O2 /app/oracle_processor.c -o /app/oracle_processor
    chmod +x /app/oracle_processor

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user