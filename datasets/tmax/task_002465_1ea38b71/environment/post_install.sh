apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        gcc \
        ffmpeg \
        python3-opencv \
        python3-numpy \
        libgl1-mesa-glx \
        libglib2.0-0

    pip3 install --default-timeout=100 pytest

    mkdir -p /app

    # Create oracle
    cat << 'EOF' > /app/oracle_simulate_growth.c
#include <stdio.h>
#include <stdlib.h>

double f(double y, int L) {
    double a = 0.5;
    double K = 100.0;
    double b = 0.001;
    return a * y * (1.0 - y / K) - b * (double)L * y;
}

int main(int argc, char *argv[]) {
    if (argc != 3) return 1;
    int L = atoi(argv[1]);
    double y = atof(argv[2]);
    double T = 76.0;
    double dt = 0.01;
    int steps = (int)(T / dt + 0.5);

    for (int i = 0; i < steps; i++) {
        double k1 = f(y, L);
        double k2 = f(y + 0.5 * dt * k1, L);
        double k3 = f(y + 0.5 * dt * k2, L);
        double k4 = f(y + dt * k3, L);
        y += (dt / 6.0) * (k1 + 2.0*k2 + 2.0*k3 + k4);
    }

    printf("%.6f\n", y);
    return 0;
}
EOF

    gcc -O2 /app/oracle_simulate_growth.c -o /app/oracle_simulate_growth -lm

    # Generate video
    cat << 'EOF' > /app/generate_video.py
import cv2
import numpy as np

width, height = 320, 240
fps = 30
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/app/cell_timelapse.mp4', fourcc, fps, (width, height))

for i in range(200):
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    if 45 <= i <= 120:
        frame[0:10, 0:10] = [0, 255, 0] # BGR in OpenCV
    out.write(frame)

out.release()
EOF

    python3 /app/generate_video.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user