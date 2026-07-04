apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        git \
        wget \
        build-essential \
        cmake \
        pkg-config \
        libgrpc++-dev \
        libprotobuf-dev \
        protobuf-compiler \
        protobuf-compiler-grpc \
        ffmpeg \
        espeak \
        zlib1g-dev

    pip3 install pytest

    # Install RapidCheck
    cd /opt
    git clone https://github.com/emil-e/rapidcheck.git
    cd rapidcheck
    mkdir build && cd build
    cmake ..
    make -j4
    make install

    # Install whisper.cpp
    cd /opt
    git clone https://github.com/ggerganov/whisper.cpp.git
    cd whisper.cpp
    git checkout v1.5.0
    make
    cp main /usr/local/bin/whisper

    # Download whisper model
    mkdir -p /app/models
    bash ./models/download-ggml-model.sh base
    cp models/ggml-base.bin /app/models/

    # Create libecc
    mkdir -p /app/lib /app/include
    cat << 'EOF' > /app/include/ecc_lib.h
#ifndef ECC_LIB_H
#define ECC_LIB_H
#include <stdint.h>
#include <stddef.h>
#ifdef __cplusplus
extern "C" {
#endif
uint32_t calculate_asset_crc(const uint8_t* data, size_t length);
#ifdef __cplusplus
}
#endif
#endif
EOF

    cat << 'EOF' > /opt/ecc_lib.c
#include "ecc_lib.h"
uint32_t calculate_asset_crc(const uint8_t* data, size_t length) {
    uint32_t crc = 0xFFFFFFFF;
    for (size_t i = 0; i < length; i++) {
        crc ^= data[i];
        for (int j = 0; j < 8; j++) {
            if (crc & 1) crc = (crc >> 1) ^ 0xEDB88320;
            else crc >>= 1;
        }
    }
    return ~crc;
}
EOF
    gcc -shared -fPIC -o /app/lib/libecc.so /opt/ecc_lib.c -I/app/include

    # Create config_memo.wav
    mkdir -p /app/assets
    espeak -w /tmp/temp.wav "The build token is alpha bravo charlie niner."
    ffmpeg -i /tmp/temp.wav -ar 16000 -ac 1 -c:a pcm_s16le /app/assets/config_memo.wav

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/workspace
    chmod -R 777 /home/user
    chmod -R 777 /app