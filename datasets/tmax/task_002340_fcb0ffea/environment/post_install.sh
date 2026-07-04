apt-get update && apt-get install -y python3 python3-pip gcc ffmpeg
pip3 install pytest

mkdir -p /app

# Create oracle source code
cat << 'EOF' > /app/oracle.c
#include <stdio.h>
#include <stdint.h>

int main() {
    uint8_t image[4096];
    size_t bytes_read = fread(image, 1, 4096, stdin);
    if (bytes_read != 4096) return 1;

    float blocks[64] = {0};
    uint32_t total_sum = 0;

    for (int y = 0; y < 64; y++) {
        for (int x = 0; x < 64; x++) {
            int block_idx = (y / 8) * 8 + (x / 8);
            uint8_t pixel = image[y * 64 + x];
            blocks[block_idx] += pixel;
            total_sum += pixel;
        }
    }

    for (int i = 0; i < 64; i++) {
        blocks[i] /= 64.0f;
    }

    unsigned int seed = total_sum;
    float boot_means[100];
    float min_mean = 1e9, max_mean = -1e9, sum_mean = 0;

    for (int s = 0; s < 100; s++) {
        float sample_sum = 0;
        for (int i = 0; i < 64; i++) {
            seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF;
            int idx = seed % 64;
            sample_sum += blocks[idx];
        }
        float sample_mean = sample_sum / 64.0f;
        boot_means[s] = sample_mean;
        if (sample_mean < min_mean) min_mean = sample_mean;
        if (sample_mean > max_mean) max_mean = sample_mean;
        sum_mean += sample_mean;
    }

    printf("Min: %.4f, Max: %.4f, Avg: %.4f\n", min_mean, max_mean, sum_mean / 100.0f);
    return 0;
}
EOF

# Compile oracle
gcc -O3 /app/oracle.c -o /app/oracle_process_frame

# Create dummy video
ffmpeg -f lavfi -i testsrc=duration=5:size=320x240:rate=30 -c:v libx264 /app/raw_footage.mp4

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app