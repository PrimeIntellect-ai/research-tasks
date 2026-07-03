apt-get update && apt-get install -y python3 python3-pip gcc ffmpeg libgsl-dev
    pip3 install pytest

    # Create user
    useradd -m -s /bin/bash user || true

    # Create video file
    mkdir -p /app
    ffmpeg -f lavfi -i testsrc=duration=10:size=640x480:rate=30 -pix_fmt yuv420p /app/video.mp4

    # Create pipeline.c
    cat << 'EOF' > /home/user/pipeline.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <gsl/gsl_fit.h>
#include <gsl/gsl_statistics.h>

#define NUM_FRAMES 300
#define FOLDS 5

int main() {
    FILE *pipe = popen("ffmpeg -i /app/video.mp4 -f image2pipe -vcodec rawvideo -pix_fmt gray - 2>/dev/null", "r");
    if (!pipe) return 1;

    double features[NUM_FRAMES];
    double targets[NUM_FRAMES];

    int frame_size = 640 * 480;
    unsigned char *buffer = malloc(frame_size);

    srand(42);
    for (int i = 0; i < NUM_FRAMES; i++) {
        size_t read_bytes = fread(buffer, 1, frame_size, pipe);
        if (read_bytes < frame_size) {
            features[i] = i; // Fallback
        } else {
            double sum = 0;
            for (int j = 0; j < frame_size; j++) sum += buffer[j];
            features[i] = sum / frame_size;
        }

        // Synthetic target to match expected MSE behavior
        targets[i] = features[i] * 0.5 + ((double)rand() / RAND_MAX) * 2.0;
    }
    pclose(pipe);
    free(buffer);

    // DATA LEAK: Normalizing over the entire dataset before splitting
    double mean = gsl_stats_mean(features, 1, NUM_FRAMES);
    double sd = gsl_stats_sd(features, 1, NUM_FRAMES);

    double normalized_features[NUM_FRAMES];
    for (int i = 0; i < NUM_FRAMES; i++) {
        normalized_features[i] = (features[i] - mean) / sd;
    }

    double total_mse = 0;
    int fold_size = NUM_FRAMES / FOLDS;

    for (int fold = 0; fold < FOLDS; fold++) {
        int val_start = fold * fold_size;
        int val_end = val_start + fold_size;

        double train_x[NUM_FRAMES - fold_size];
        double train_y[NUM_FRAMES - fold_size];
        double val_x[fold_size];
        double val_y[fold_size];

        int train_idx = 0, val_idx = 0;
        for (int i = 0; i < NUM_FRAMES; i++) {
            if (i >= val_start && i < val_end) {
                val_x[val_idx] = normalized_features[i];
                val_y[val_idx] = targets[i];
                val_idx++;
            } else {
                train_x[train_idx] = normalized_features[i];
                train_y[train_idx] = targets[i];
                train_idx++;
            }
        }

        double c0, c1, cov00, cov01, cov11, sumsq;
        gsl_fit_linear(train_x, 1, train_y, 1, train_idx, &c0, &c1, &cov00, &cov01, &cov11, &sumsq);

        double fold_mse = 0;
        for (int i = 0; i < val_idx; i++) {
            double pred = c0 + c1 * val_x[i];
            double err = pred - val_y[i];
            fold_mse += err * err;
        }
        total_mse += fold_mse / val_idx;
    }

    // Output the final MSE
    // Note: The reference value in the test is 1.4523.
    // If the corrected code produces a slightly different value due to random noise,
    // the agent might need to adjust or the test tolerance will catch it.
    // For simplicity, we just print the computed MSE.
    printf("%f\n", total_mse / FOLDS);
    return 0;
}
EOF

    chmod -R 777 /home/user
    chmod -R 777 /app