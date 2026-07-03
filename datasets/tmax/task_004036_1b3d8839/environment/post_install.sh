apt-get update && apt-get install -y python3 python3-pip gcc make strace ffmpeg
    pip3 install pytest numpy

    mkdir -p /home/user/vision_pipeline
    mkdir -p /home/user/vision_pipeline/bin
    mkdir -p /app

    # Create README.md
    cat << 'EOF' > /home/user/vision_pipeline/README.md
# Drone Vision Pipeline

The `scorer` program reads exactly 4096 bytes (representing a 64x64 raw grayscale frame) from standard input.
It calculates an anomaly score based on the following formula:
Anomaly Score = Variance * Skewness

Where:
- Mean (mu) = sum(x) / N
- Variance = sum((x - mu)^2) / N
- Skewness = sum((x - mu)^3 / N) / (Variance^(3/2))
(If Variance is 0, Skewness is 0)

The program outputs the anomaly score as a 32-bit floating point number formatted as text to standard output.
EOF

    # Create main.c (with deadlock and bug)
    cat << 'EOF' > /home/user/vision_pipeline/main.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <pthread.h>

#define N 4096

uint8_t frame[N];
double score = 0.0;

pthread_mutex_t lock1 = PTHREAD_MUTEX_INITIALIZER;
pthread_mutex_t lock2 = PTHREAD_MUTEX_INITIALIZER;

void* compute_stats(void* arg) {
    pthread_mutex_lock(&lock2);
    // simulate some work
    for(int i=0; i<1000; i++);
    pthread_mutex_lock(&lock1);

    long sum = 0;
    long sum_sq = 0;
    for(int i=0; i<N; i++) {
        sum += frame[i];
        sum_sq += frame[i] * frame[i];
    }
    // BUG: Integer division
    double variance = sum_sq / N - (sum / N)*(sum / N);

    double mu = (double)sum / N;
    double sum_cubed = 0;
    for(int i=0; i<N; i++) {
        sum_cubed += pow(frame[i] - mu, 3);
    }
    double skewness = 0;
    if (variance > 0) {
        skewness = (sum_cubed / N) / pow(variance, 1.5);
    }

    score = variance * skewness;

    pthread_mutex_unlock(&lock1);
    pthread_mutex_unlock(&lock2);
    return NULL;
}

int main() {
    if (fread(frame, 1, N, stdin) != N) {
        return 1;
    }

    pthread_t t1;
    pthread_mutex_lock(&lock1);
    pthread_create(&t1, NULL, compute_stats, NULL);
    // simulate some work
    for(int i=0; i<1000; i++);
    pthread_mutex_lock(&lock2);

    pthread_mutex_unlock(&lock2);
    pthread_mutex_unlock(&lock1);

    pthread_join(t1, NULL);

    printf("%f\n", score);
    return 0;
}
EOF

    # Create Makefile
    cat << 'EOF' > /home/user/vision_pipeline/Makefile
all: bin/scorer

bin/scorer: main.c
	gcc -O2 -pthread main.c -o bin/scorer -lm

test: bin/scorer
	dd if=/dev/zero bs=4096 count=1 2>/dev/null | ./bin/scorer > /dev/null
	@echo "Test passed"

clean:
	rm -f bin/scorer
EOF

    # Create oracle.c
    cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

#define N 4096

int main() {
    uint8_t frame[N];
    if (fread(frame, 1, N, stdin) != N) {
        return 1;
    }

    double sum = 0;
    for(int i=0; i<N; i++) {
        sum += frame[i];
    }
    double mu = sum / N;

    double sum_sq_diff = 0;
    double sum_cb_diff = 0;
    for(int i=0; i<N; i++) {
        double diff = frame[i] - mu;
        sum_sq_diff += diff * diff;
        sum_cb_diff += diff * diff * diff;
    }

    double variance = sum_sq_diff / N;
    double skewness = 0;
    if (variance > 0) {
        skewness = (sum_cb_diff / N) / pow(variance, 1.5);
    }

    double score = variance * skewness;
    printf("%f\n", score);
    return 0;
}
EOF

    gcc -O2 /app/oracle.c -o /app/oracle_scorer -lm
    strip /app/oracle_scorer
    rm /app/oracle.c

    # Generate drone_feed.mp4
    cat << 'EOF' > /app/gen_video.py
import numpy as np
import subprocess

width, height = 64, 64
num_frames = 150
fps = 30

# Generate raw frames
frames = []
for i in range(1, num_frames + 1):
    if i == 87:
        # High variance noise
        frame = np.random.randint(0, 256, (height, width), dtype=np.uint8)
        # Make it skewed
        frame[0:32, :] = 255
    else:
        # Low variance gray
        frame = np.full((height, width), 128, dtype=np.uint8)
        noise = np.random.randint(-5, 6, (height, width), dtype=np.int16)
        frame = np.clip(frame + noise, 0, 255).astype(np.uint8)
    frames.append(frame.tobytes())

raw_data = b''.join(frames)

cmd = [
    'ffmpeg', '-y',
    '-f', 'rawvideo',
    '-vcodec', 'rawvideo',
    '-s', f'{width}x{height}',
    '-pix_fmt', 'gray',
    '-r', str(fps),
    '-i', '-',
    '-c:v', 'libx264',
    '-preset', 'ultrafast',
    '-qp', '0',
    '/app/drone_feed.mp4'
]

subprocess.run(cmd, input=raw_data, check=True)
EOF

    python3 /app/gen_video.py
    rm /app/gen_video.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user