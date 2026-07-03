apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        gcc \
        gawk \
        bc \
        ffmpeg \
        python3-numpy \
        python3-opencv

    pip3 install pytest

    mkdir -p /app

    # Create the oracle binary
    cat << 'EOF' > /tmp/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char **argv) {
    if (argc != 3) return 1;
    FILE *f1 = fopen(argv[1], "r");
    FILE *f2 = fopen(argv[2], "r");
    if (!f1 || !f2) return 1;

    int p_counts[10000];
    int q_counts[10000];
    int n = 0;
    int val;

    while (fscanf(f1, "%d", &val) == 1) {
        p_counts[n] = val + 1;
        n++;
    }

    int m = 0;
    while (fscanf(f2, "%d", &val) == 1) {
        q_counts[m] = val + 1;
        m++;
    }

    if (n != m || n == 0) return 1;

    double p_sum = 0, q_sum = 0;
    for (int i = 0; i < n; i++) {
        p_sum += p_counts[i];
        q_sum += q_counts[i];
    }

    double kl = 0;
    for (int i = 0; i < n; i++) {
        double p = p_counts[i] / p_sum;
        double q = q_counts[i] / q_sum;
        kl += p * log2(p / q);
    }

    printf("%.4f\n", kl);
    return 0;
}
EOF
    gcc -O3 /tmp/oracle.c -o /app/oracle_kl -lm
    chmod +x /app/oracle_kl

    # Generate a synthetic video for the fixture
    python3 -c "
import cv2
import numpy as np

out = cv2.VideoWriter('/app/sequencer_run.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, (100, 100), False)
np.random.seed(42)
for i in range(100):
    intensity = int(128 + 50 * np.sin(i * 0.2) + np.random.normal(0, 10))
    intensity = max(0, min(255, intensity))
    frame = np.full((100, 100), intensity, dtype=np.uint8)
    out.write(frame)
out.release()
"

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user