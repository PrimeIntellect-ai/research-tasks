apt-get update && apt-get install -y python3 python3-pip git build-essential gdb libsndfile1-dev libsndfile1
    pip3 install pytest numpy scipy

    mkdir -p /app
    mkdir -p /home/user/noise-filter

    # Generate noisy input audio
    cat << 'EOF' > /app/generate_audio.py
import numpy as np
from scipy.io import wavfile

sample_rate = 16000
t = np.linspace(0, 1, sample_rate, endpoint=False)
# Speech-like signal + noise
clean = 0.5 * np.sin(2 * np.pi * 440 * t)
noise = 0.2 * np.sin(2 * np.pi * 60 * t) + 0.1 * np.random.randn(sample_rate)
noisy = clean + noise

# Save as 16-bit PCM
wavfile.write('/app/noisy_input.wav', sample_rate, np.int16(noisy * 32767))
EOF
    python3 /app/generate_audio.py

    # Create C project files
    cat << 'EOF' > /home/user/noise-filter/lms_filter.h
#ifndef LMS_FILTER_H
#define LMS_FILTER_H

#define DEFAULT_MU 0.01f

void update_weights(float *weights, float error, float ref_val);
void lms_filter(const float *input, float *output, int length);

#endif
EOF

    cat << 'EOF' > /home/user/noise-filter/lms_filter.c
#include "lms_filter.h"

void update_weights(float *weights, float error, float ref_val) {
    float step_size = DEFAULT_MU;
    weights[0] += step_size * error * ref_val;
}

void lms_filter(const float *input, float *output, int length) {
    float weights[1] = {0.0f};
    for(int i=0; i<length; i++) {
        float error = input[i] - weights[0]*input[i];
        output[i] = error;
        update_weights(weights, error, input[i]);
    }
}
EOF

    cat << 'EOF' > /home/user/noise-filter/main.c
#include <stdio.h>
#include <stdlib.h>
#include <sndfile.h>
#include "lms_filter.h"

int main(int argc, char **argv) {
    if (argc < 3) {
        printf("Usage: %s <input.wav> <output.wav>\n", argv[0]);
        return 1;
    }
    SNDFILE *infile, *outfile;
    SF_INFO sfinfo;
    infile = sf_open(argv[1], SFM_READ, &sfinfo);
    if (!infile) return 1;

    float *buffer = malloc(sfinfo.frames * sfinfo.channels * sizeof(float));
    sf_readf_float(infile, buffer, sfinfo.frames * sfinfo.channels);
    sf_close(infile);

    float *out_buffer = malloc(sfinfo.frames * sfinfo.channels * sizeof(float));
    lms_filter(buffer, out_buffer, sfinfo.frames * sfinfo.channels);

    outfile = sf_open(argv[2], SFM_WRITE, &sfinfo);
    sf_writef_float(outfile, out_buffer, sfinfo.frames * sfinfo.channels);
    sf_close(outfile);
    free(buffer);
    free(out_buffer);
    return 0;
}
EOF

    cat << 'EOF' > /home/user/noise-filter/Makefile
all:
	gcc -g -o filter main.c lms_filter.c -lsndfile
EOF

    # Compile and generate clean reference
    cd /home/user/noise-filter
    make
    ./filter /app/noisy_input.wav /app/clean_reference.wav

    # Setup git repo and history
    git config --global user.email "dev@example.com"
    git config --global user.name "Dev"
    git init
    git add .
    git commit -m "Initial commit: working LMS filter"

    # Add some dummy commits
    echo "/* cleanup */" >> main.c
    git commit -am "Minor cleanup in main"

    # Introduce the bug
    cat << 'EOF' > /home/user/noise-filter/lms_filter.c
#include "lms_filter.h"

void update_weights(float *weights, float error, float ref_val) {
    float step_size;
    weights[0] += step_size * error * ref_val;
}

void lms_filter(const float *input, float *output, int length) {
    float weights[1] = {0.0f};
    for(int i=0; i<length; i++) {
        float error = input[i] - weights[0]*input[i];
        output[i] = error;
        update_weights(weights, error, input[i]);
    }
}
EOF
    git commit -am "Optimize learning rate scaling"

    # Add more commits to bury the bug
    echo "/* update */" >> main.c
    git commit -am "Update main.c comments"
    echo "/* another update */" >> main.c
    git commit -am "Refactor main.c slightly"

    # Clean up build artifacts
    rm filter

    # Create verifier script
    cat << 'EOF' > /app/verify_mse.py
import sys
import os
import numpy as np
from scipy.io import wavfile

def main():
    fixed_path = '/home/user/fixed_output.wav'
    ref_path = '/app/clean_reference.wav'

    if not os.path.exists(fixed_path):
        print(f"Error: {fixed_path} not found.")
        sys.exit(1)

    rate1, data1 = wavfile.read(fixed_path)
    rate2, data2 = wavfile.read(ref_path)

    # Normalize
    data1 = data1.astype(np.float32) / 32768.0
    data2 = data2.astype(np.float32) / 32768.0

    mse = np.mean((data1 - data2)**2)
    print(f"MSE: {mse}")

    if mse < 0.005:
        print("Success: MSE is within threshold.")
        sys.exit(0)
    else:
        print("Failure: MSE exceeds threshold.")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user