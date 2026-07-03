apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest numpy

    mkdir -p /app/libdatatransform-1.0/src
    mkdir -p /home/user

    cat << 'EOF' > /app/libdatatransform-1.0/Makefile
all: transform

transform: src/main.c src/filter.c
	gcc -O2 -Wall -o transform src/main.c src/filter.c

clean:
	rm -f transform
EOF

    cat << 'EOF' > /app/libdatatransform-1.0/src/filter.h
#ifndef FILTER_H
#define FILTER_H
void apply_filter(double *data, int length);
#endif
EOF

    cat << 'EOF' > /app/libdatatransform-1.0/src/main.c
#include <stdio.h>
#include <stdlib.h>
#include "filter.h"

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <input.bin> <output.bin>\n", argv[0]);
        return 1;
    }
    FILE *fin = fopen(argv[1], "rb");
    if (!fin) return 1;
    fseek(fin, 0, SEEK_END);
    long size = ftell(fin);
    fseek(fin, 0, SEEK_SET);
    int length = size / sizeof(double);
    double *data = malloc(size);
    fread(data, sizeof(double), length, fin);
    fclose(fin);

    apply_filter(data, length);

    FILE *fout = fopen(argv[2], "wb");
    if (!fout) return 1;
    fwrite(data, sizeof(double), length, fout);
    fclose(fout);
    free(data);
    return 0;
}
EOF

    # Write the FIXED filter.c to generate expected output
    cat << 'EOF' > /app/libdatatransform-1.0/src/filter.c
#include "filter.h"

#define ALPHA 0.987654321012345
#define BETA  0.123456789012345

void apply_filter(double *data, int length) {
    double state = 0.0;
    for (int i = 0; i < length; i++) {
        double temp = data[i] * ALPHA + state * BETA;
        data[i] = temp;
        state = data[i];
    }
}
EOF

    # Generate input data
    cat << 'EOF' > /tmp/gen_input.py
import numpy as np
data = np.random.uniform(-1.0, 1.0, 10000).astype(np.float64)
data.tofile('/home/user/sensor_input.bin')
EOF
    python3 /tmp/gen_input.py

    # Compile and generate expected output
    cd /app/libdatatransform-1.0
    make
    ./transform /home/user/sensor_input.bin /home/user/expected_output.bin

    # Now write the PERTURBED filter.c
    cat << 'EOF' > /app/libdatatransform-1.0/src/filter.c
#include "filter.h"

#define ALPHA 0.987654321012345
#define BETA  0.123456789012345

void apply_filter(double *data, int length) {
    double state = 0.0;
    for (int i = 0; i < length; i++) {
        // Perturbation: intermediate calculation cast to float causing precision loss
        float temp = (float)(data[i] * ALPHA + state * BETA);
        data[i] = (double)temp;
        state = data[i];
    }
}
EOF

    # Clean up so the agent has to recompile
    make clean

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app