apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-numpy \
    python3-scipy \
    gcc \
    make \
    libwebsockets-dev

pip3 install pytest websockets

mkdir -p /app/audio_math_server

cat << 'EOF' > /app/audio_math_server/audio_buffer.h
#ifndef AUDIO_BUFFER_H
#define AUDIO_BUFFER_H

#include "router.h"

typedef struct {
    float* data;
    int length;
} AudioBuffer;

#endif
EOF

cat << 'EOF' > /app/audio_math_server/router.h
#ifndef ROUTER_H
#define ROUTER_H

#include "state_machine.h"

void handle_route(const char* url);

#endif
EOF

cat << 'EOF' > /app/audio_math_server/state_machine.h
#ifndef STATE_MACHINE_H
#define STATE_MACHINE_H

#include "audio_buffer.h"

void apply_filter(const char* command, AudioBuffer* buffer);

#endif
EOF

cat << 'EOF' > /app/audio_math_server/state_machine.c
#include "state_machine.h"
#include <string.h>

void apply_filter(const char* command, AudioBuffer* buffer) {
    // TODO: Implement moving_average (MA) parsing and logic
}
EOF

cat << 'EOF' > /app/audio_math_server/main.c
#include <stdio.h>
#include "router.h"

int main(int argc, char** argv) {
    printf("Server started\n");
    return 0;
}
EOF

cat << 'EOF' > /app/audio_math_server/Makefile
CC=gcc
CFLAGS=-I.

all: dsp_server

dsp_server: main.c state_machine.c
	$(CC) $(CFLAGS) -o dsp_server main.c state_machine.c -lwebsockets

clean:
	rm -f dsp_server
EOF

python3 -c "
import numpy as np
import scipy.io.wavfile as wav

sr = 16000
t = np.linspace(0, 1, sr, endpoint=False)
clean = np.sin(2 * np.pi * 1000 * t)
noise = np.random.uniform(-0.5, 0.5, sr)
noisy = clean + noise

clean_int = np.int16(clean * 32767)
noisy_int = np.int16(noisy * 32767)

wav.write('/tmp/clean_reference.wav', sr, clean_int)
wav.write('/app/noisy_speech.wav', sr, noisy_int)
"

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user
chmod -R 777 /app