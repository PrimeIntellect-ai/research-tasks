apt-get update && apt-get install -y python3 python3-pip gcc make
    pip3 install pytest

    mkdir -p /app/vendored/seq_analyzer
    cd /app/vendored/seq_analyzer

    cat << 'EOF' > fft.h
#ifndef FFT_H
#define FFT_H
void compute_fft(const char* seq, float* out_mag, int len);
#endif
EOF

    cat << 'EOF' > fft.c
#include "fft.h"
#include <math.h>
void compute_fft(const char* seq, float* out_mag, int len) {
    for(int i=0; i<len; i++) {
        out_mag[i] = sin(i) * cos(i) + (seq[i] % 10);
    }
}
EOF

    cat << 'EOF' > mc_stats.h
#ifndef MC_STATS_H
#define MC_STATS_H
float compute_mc_significance(float* mag, int len);
#endif
EOF

    cat << 'EOF' > mc_stats.c
#include "mc_stats.h"
#include <math.h>

float compute_mc_significance(float* mag, int len) {
    float total_variance = 0.0f;
    for(int i=0; i<10000; i++) {
        float var = sin(i * 0.1f) * sin(i * 0.1f) * mag[i % len];
        total_variance += var;
    }
    return total_variance;
}
EOF

    cat << 'EOF' > main.c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "fft.h"
#include "mc_stats.h"

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    int len = strlen(argv[1]);
    if (len == 0) return 1;
    float* mag = malloc(len * sizeof(float));
    compute_fft(argv[1], mag, len);
    float sig = compute_mc_significance(mag, len);
    printf("%f\n", sig);
    free(mag);
    return 0;
}
EOF

    cat << 'EOF' > Makefile
CC = gcc
CFLAGS = -O3 -I.

all: seq_analyzer

seq_analyzer: main.o fft.o mc_stats.o
	$(CC) -o seq_analyzer main.o fft.o mc_stats.o
EOF

    # Compile the oracle
    cat << 'EOF' > mc_stats_oracle.c
#include "mc_stats.h"
#include <math.h>

float compute_mc_significance(float* mag, int len) {
    float total_variance = 0.0f;
    float c = 0.0f;
    for(int i=0; i<10000; i++) {
        float var = sin(i * 0.1f) * sin(i * 0.1f) * mag[i % len];
        float y = var - c;
        float t = total_variance + y;
        c = (t - total_variance) - y;
        total_variance = t;
    }
    return total_variance;
}
EOF

    gcc -O3 -I. main.c fft.c mc_stats_oracle.c -lm -o /app/oracle_seq_analyzer
    rm mc_stats_oracle.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app