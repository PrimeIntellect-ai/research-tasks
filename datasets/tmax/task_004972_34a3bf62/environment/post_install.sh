apt-get update && apt-get install -y python3 python3-pip gcc libsndfile1-dev
    pip3 install pytest numpy scipy

    mkdir -p /app /opt
    useradd -m -s /bin/bash user || true

    cat << 'EOF' > /home/user/telemetry_processor.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sndfile.h>

#define BUFFER_SIZE 1024

void process_audio(float *buffer, int count) {
    static float accumulator = 0.0f; // BUG: single precision accumulator
    float alpha = 0.99f;

    for (int i = 0; i < count; i++) {
        // BUG: missing isnan/isinf check
        accumulator = alpha * accumulator + (1.0f - alpha) * buffer[i];
        buffer[i] = accumulator;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) {
        printf("Usage: %s <input.wav> <output.wav>\n", argv[0]);
        return 1;
    }

    SNDFILE *infile, *outfile;
    SF_INFO sfinfo;

    sfinfo.format = 0;
    infile = sf_open(argv[1], SFM_READ, &sfinfo);
    if (!infile) {
        printf("Error opening input file\n");
        return 1;
    }

    sfinfo.format = SF_FORMAT_WAV | SF_FORMAT_PCM_16;
    outfile = sf_open(argv[2], SFM_WRITE, &sfinfo);
    if (!outfile) {
        printf("Error opening output file\n");
        sf_close(infile);
        return 1;
    }

    float buffer[BUFFER_SIZE];
    int read_count;

    while ((read_count = sf_read_float(infile, buffer, BUFFER_SIZE)) > 0) {
        process_audio(buffer, read_count);
        sf_write_float(outfile, buffer, read_count);
    }

    sf_close(infile);
    sf_close(outfile);
    return 0;
}
EOF

    cat << 'EOF' > /tmp/generate_data.py
import numpy as np
import scipy.io.wavfile as wav
import math

sample_rate = 16000
duration = 2.0
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
signal = 0.5 * np.sin(2 * np.pi * 440 * t) + 0.1 * np.sin(2 * np.pi * 5000 * t)

# Inject NaNs
corrupted_signal = signal.copy()
corrupted_signal[5000:5010] = np.nan
corrupted_signal[12000:12010] = np.inf

# Save corrupted as float32 WAV so libsndfile can read NaNs
wav.write('/app/corrupted_telemetry.wav', sample_rate, corrupted_signal.astype(np.float32))

# Generate reference clean
clean_signal = signal.copy()
clean_signal[np.isnan(corrupted_signal) | np.isinf(corrupted_signal)] = 0.0

# Process reference with double precision
accumulator = 0.0
alpha = 0.99
processed = np.zeros_like(clean_signal)
for i in range(len(clean_signal)):
    accumulator = alpha * accumulator + (1.0 - alpha) * clean_signal[i]
    processed[i] = accumulator

# Save reference as 16-bit PCM
processed_int16 = np.clip(processed * 32768.0, -32768, 32767).astype(np.int16)
wav.write('/opt/reference_clean_telemetry.wav', sample_rate, processed_int16)

EOF

    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    chmod -R 777 /home/user
    chmod -R 777 /app