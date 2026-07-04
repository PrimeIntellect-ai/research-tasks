apt-get update && apt-get install -y python3 python3-pip ffmpeg gcc build-essential
    pip3 install pytest pandas numpy

    mkdir -p /app
    mkdir -p /home/user/analyzer

    # Generate test video
    ffmpeg -y -f lavfi -i testsrc=duration=10:size=640x480:rate=30 -pix_fmt yuv420p /app/test_run.mp4

    # Generate expected truth
    cat << 'EOF' > /app/generate_truth.py
import subprocess
import numpy as np
import pandas as pd

cmd = ['ffmpeg', '-i', '/app/test_run.mp4', '-f', 'image2pipe', '-vcodec', 'rawvideo', '-pix_fmt', 'rgb24', '-']
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
width, height = 640, 480
frames = []
frame_num = 0
while True:
    raw_frame = proc.stdout.read(width * height * 3)
    if not raw_frame:
        break
    frame = np.frombuffer(raw_frame, dtype=np.uint8)
    intensity = np.mean(frame)
    frames.append((frame_num, intensity))
    frame_num += 1

df = pd.DataFrame(frames, columns=['frame', 'intensity'])
df.to_csv('/app/expected_truth.csv', index=False, header=False)
EOF
    python3 /app/generate_truth.py

    # Create buggy main.c
    cat << 'EOF' > /home/user/analyzer/main.c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <stdint.h>

#define WIDTH 640
#define HEIGHT 480
#define NUM_THREADS 4

FILE *out_file;
FILE *in_file;

int current_frame = 0;
uint8_t frame_buffer[WIDTH * HEIGHT * 3]; // Shared buffer, BUG!

void* process_frame(void* arg) {
    int frame_num = *(int*)arg;
    free(arg);

    // Calculate intensity
    double sum = 0;
    for (int i = 0; i < WIDTH * HEIGHT * 3; i++) {
        sum += frame_buffer[i];
    }
    double intensity = sum / (WIDTH * HEIGHT * 3);

    // Write to file without mutex, BUG!
    fprintf(out_file, "%d,%f\n", frame_num, intensity);

    return NULL;
}

int main() {
    in_file = popen("ffmpeg -i /app/test_run.mp4 -f image2pipe -vcodec rawvideo -pix_fmt rgb24 - 2>/dev/null", "r");
    if (!in_file) return 1;
    out_file = fopen("output.csv", "w");
    if (!out_file) return 1;

    pthread_t threads[NUM_THREADS];
    int active_threads = 0;

    while (1) {
        size_t bytes_read = fread(frame_buffer, 1, WIDTH * HEIGHT * 3, in_file);
        if (bytes_read < WIDTH * HEIGHT * 3) break;

        int *arg = malloc(sizeof(int));
        *arg = current_frame;

        pthread_create(&threads[active_threads], NULL, process_frame, arg);
        active_threads++;
        current_frame++;

        if (active_threads == NUM_THREADS) {
            for (int i = 0; i < NUM_THREADS; i++) {
                pthread_join(threads[i], NULL);
            }
            active_threads = 0;
        }
    }

    for (int i = 0; i < active_threads; i++) {
        pthread_join(threads[i], NULL);
    }

    pclose(in_file);
    fclose(out_file);
    return 0;
}
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user