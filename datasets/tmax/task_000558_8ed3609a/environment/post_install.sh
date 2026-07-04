apt-get update && apt-get install -y python3 python3-pip python3-numpy python3-scipy ffmpeg espeak gcc
    pip3 install pytest

    mkdir -p /app/corpus/clean /app/corpus/evil

    # Generate audio_filter.c
    cat << 'EOF' > /app/audio_filter.c
#include <stdio.h>
#include <math.h>

void process_audio(float* input, float* output, int length, float cutoff, float resonance) {
    // biquad filter implementation
    float c = 1.0f / tanf(3.14159265f * cutoff / 44100.0f);
    float a1 = 1.0f / (1.0f + resonance * c + c * c);
    float a2 = 2.0f * a1;
    float a3 = a1;
    float b1 = 2.0f * (1.0f - c * c) * a1;
    float b2 = (1.0f - resonance * c + c * c) * a1;

    float z1 = 0.0f, z2 = 0.0f;
    for (int i = 0; i < length; i++) {
        float in = input[i];
        float out = a1 * in + z1;
        z1 = a2 * in + z2 - b1 * out;
        z2 = a3 * in - b2 * out;
        output[i] = out;
    }
}
EOF

    # Generate voicemail
    espeak -w /app/ticket_1492_voicemail.wav "The system crashes when the resonance is set to zero point nine nine five and the cutoff is four thousand."

    # Generate test corpus
    cat << 'EOF' > /tmp/gen_audio.py
import numpy as np
from scipy.io import wavfile
import os

sr = 44100
duration = 5
t = np.linspace(0, duration, sr * duration, endpoint=False)

for i in range(10):
    # Clean: low amplitude noise
    clean_data = np.random.uniform(-1000, 1000, len(t)).astype(np.int16)
    wavfile.write(f'/app/corpus/clean/clean_{i}.wav', sr, clean_data)

    # Evil: 4000Hz sine wave, full scale
    evil_data = (32767 * np.sin(2 * np.pi * 4000 * t)).astype(np.int16)
    wavfile.write(f'/app/corpus/evil/evil_{i}.wav', sr, evil_data)
EOF
    python3 /tmp/gen_audio.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app