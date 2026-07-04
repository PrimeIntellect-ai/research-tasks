apt-get update && apt-get install -y python3 python3-pip golang gcc
    pip3 install pytest

    mkdir -p /app

    # Generate the pulse.wav file
    cat << 'EOF' > /tmp/gen_wav.py
import wave
import struct
import math

with wave.open('/app/pulse.wav', 'w') as f:
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(44100)
    for i in range(1000):
        # Create a Gaussian pulse
        val = int(10000 * math.exp(-((i-500)/50.0)**2))
        f.writeframes(struct.pack('<h', val))
EOF
    python3 /tmp/gen_wav.py

    # Create the oracle C program
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[]) {
    if (argc != 5) return 1;
    double c = atof(argv[1]);
    double dt = atof(argv[2]);
    double dx = atof(argv[3]);
    int steps = atoi(argv[4]);

    FILE *f = fopen("/app/pulse.wav", "rb");
    if (!f) return 1;
    fseek(f, 44, SEEK_SET);
    int16_t samples[1000];
    fread(samples, sizeof(int16_t), 1000, f);
    fclose(f);

    double U_prev[1000];
    double U_curr[1000];
    double U_next[1000];

    for (int i = 0; i < 1000; i++) {
        U_prev[i] = (double)samples[i];
        U_curr[i] = (double)samples[i];
    }
    U_curr[0] = 0; U_curr[999] = 0;
    U_prev[0] = 0; U_prev[999] = 0;

    double coeff = (c * dt / dx) * (c * dt / dx);

    for (int t = 0; t < steps; t++) {
        for (int i = 1; i < 999; i++) {
            U_next[i] = 2 * U_curr[i] - U_prev[i] + coeff * (U_curr[i+1] - 2 * U_curr[i] + U_curr[i-1]);
        }
        U_next[0] = 0;
        U_next[999] = 0;
        for (int i = 0; i < 1000; i++) {
            U_prev[i] = U_curr[i];
            U_curr[i] = U_next[i];
        }
    }

    for (int i = 0; i < 1000; i++) {
        printf("%.6f\n", U_curr[i]);
    }

    return 0;
}
EOF
    gcc -O3 /tmp/oracle.c -o /app/oracle_simulator

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app