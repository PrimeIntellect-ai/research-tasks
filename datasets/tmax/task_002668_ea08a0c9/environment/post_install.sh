apt-get update
    apt-get install -y --no-install-recommends python3 python3-pip ffmpeg gcc libc6-dev
    pip3 install --no-cache-dir pytest numpy opencv-python-headless scipy

    # Generate the video
    mkdir -p /app
    cat << 'EOF' > /tmp/gen_video.py
import cv2
import numpy as np
import math

out = cv2.VideoWriter('/app/reaction.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (100, 100), False)
for i in range(300):
    # Base intensity oscillates with period = 24
    intensity = int(127.5 * (1 + math.sin(2 * math.pi * i / 24.0)))
    # Clamp to 0-255 just in case
    intensity = max(0, min(255, intensity))
    frame = np.full((100, 100), intensity, dtype=np.uint8)
    out.write(frame)
out.release()
EOF
    python3 /tmp/gen_video.py
    rm /tmp/gen_video.py

    # Build the oracle
    mkdir -p /opt/verifier
    cat << 'EOF' > /opt/verifier/oracle_sim.c
#include <stdio.h>
#include <math.h>

int main() {
    double x, y;
    if (scanf("%lf %lf", &x, &y) != 2) return 1;

    double dt = 0.1;
    double omega = 2.0 * M_PI / 24.0;
    double omega2 = omega * omega;

    for (int i = 0; i < 100; i++) {
        double k1x = y;
        double k1y = -omega2 * x;

        double k2x = y + 0.5 * dt * k1y;
        double k2y = -omega2 * (x + 0.5 * dt * k1x);

        double k3x = y + 0.5 * dt * k2y;
        double k3y = -omega2 * (x + 0.5 * dt * k2x);

        double k4x = y + dt * k3y;
        double k4y = -omega2 * (x + dt * k3x);

        x += (dt / 6.0) * (k1x + 2*k2x + 2*k3x + k4x);
        y += (dt / 6.0) * (k1y + 2*k2y + 2*k3y + k4y);
    }

    printf("%.6f %.6f\n", x, y);
    return 0;
}
EOF
    gcc -O3 /opt/verifier/oracle_sim.c -o /opt/verifier/oracle_sim -lm

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user