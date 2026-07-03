apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc
    pip3 install pytest

    mkdir -p /app

    # Generate the experiment video
    ffmpeg -f lavfi -i "color=c=gray:s=64x64:r=10:d=3" -pix_fmt gray /app/experiment.mp4

    # Write the oracle C program
    cat << 'EOF' > /app/oracle_analyze.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

uint32_t state = 42;
uint32_t next_rand() {
    state = (state * 1103515245 + 12345) & 0x7FFFFFFF;
    return state;
}

int cmp(const void *a, const void *b) {
    double da = *(double*)a;
    double db = *(double*)b;
    if (da < db) return -1;
    if (da > db) return 1;
    return 0;
}

int main() {
    double y[10000];
    int N = 0;
    while (scanf("%lf", &y[N]) == 1) {
        N++;
    }
    if (N < 2) return 0;

    double sum_x = 0, sum_y = 0, sum_xy = 0, sum_xx = 0;
    for (int i = 0; i < N; i++) {
        sum_x += i;
        sum_y += y[i];
        sum_xy += i * y[i];
        sum_xx += i * i;
    }
    double mean_x = sum_x / N;
    double mean_y = sum_y / N;
    double denominator = sum_xx - N * mean_x * mean_x;
    double m = (sum_xy - N * mean_x * mean_y) / denominator;
    double c = mean_y - m * mean_x;

    double m_boots[1000];
    for (int b = 0; b < 1000; b++) {
        double bx = 0, by = 0, bxy = 0, bxx = 0;
        for (int i = 0; i < N; i++) {
            int idx = next_rand() % N;
            bx += idx;
            by += y[idx];
            bxy += idx * y[idx];
            bxx += idx * idx;
        }
        double bmean_x = bx / N;
        double bmean_y = by / N;
        double bdenom = bxx - N * bmean_x * bmean_x;
        if (bdenom == 0.0) {
            m_boots[b] = 0.0;
        } else {
            m_boots[b] = (bxy - N * bmean_x * bmean_y) / bdenom;
        }
    }

    qsort(m_boots, 1000, sizeof(double), cmp);

    printf("m: %.4f, c: %.4f, m_lower: %.4f, m_upper: %.4f\n", m, c, m_boots[24], m_boots[974]);
    return 0;
}
EOF

    # Compile oracle
    gcc -O3 -o /app/oracle_analyze /app/oracle_analyze.c

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user