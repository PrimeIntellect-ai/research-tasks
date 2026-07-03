apt-get update && apt-get install -y python3 python3-pip gcc valgrind
pip3 install pytest

mkdir -p /app/src

cat << 'EOF' > /app/ref_filter.py
import sys
import wave
import struct

def process(in_wav, out_bin):
    with wave.open(in_wav, 'rb') as w:
        frames = w.readframes(w.getnframes())
        samples = struct.unpack(f"<{w.getnframes()}h", frames)

    out = []
    acc = 0.0
    for s in samples:
        acc = acc * 0.9 + s * 0.1
        out.append(acc)

    with open(out_bin, 'wb') as f:
        f.write(struct.pack(f"<{len(out)}d", *out))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(1)
    process(sys.argv[1], sys.argv[2])
EOF

cat << 'EOF' > /app/src/audio_filter.c
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char** argv) {
    if (argc < 3) return 1;
    FILE* fin = fopen(argv[1], "rb");
    if (!fin) return 1;
    FILE* fout = fopen(argv[2], "wb");
    if (!fout) {
        fclose(fin);
        return 1;
    }

    // skip wav header (44 bytes)
    fseek(fin, 44, SEEK_SET);

    int16_t sample;
    float acc = 0.0; // precision loss here, should be double
    while (fread(&sample, sizeof(int16_t), 1, fin) == 1) {
        // memory leak here
        int* temp_buffer = malloc(10 * sizeof(int));

        acc = acc * 0.9f + sample * 0.1f;
        double out_val = (double)acc; 
        fwrite(&out_val, sizeof(double), 1, fout);
    }

    fclose(fin);
    fclose(fout);
    return 0;
}
EOF

gcc -O0 -g /app/src/audio_filter.c -o /app/audio_filter

cat << 'EOF' > /app/generate_wav.py
import wave
import struct
import math

with wave.open('/app/sample_recording.wav', 'wb') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(44100)
    # 5 seconds of a 440Hz sine wave
    samples = [int(32767 * math.sin(2 * math.pi * 440 * i / 44100)) for i in range(44100 * 5)]
    w.writeframes(struct.pack(f"<{len(samples)}h", *samples))
EOF

python3 /app/generate_wav.py

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app