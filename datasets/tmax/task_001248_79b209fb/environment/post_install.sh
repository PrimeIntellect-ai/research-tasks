apt-get update && apt-get install -y python3 python3-pip rustc cargo gcc make cmake g++ ffmpeg git wget curl
    pip3 install pytest websockets editdistance

    mkdir -p /home/user/ws_proxy/c_src
    mkdir -p /home/user/ws_proxy/src
    mkdir -p /app

    cat << 'EOF' > /home/user/ws_proxy/c_src/filter.c
#include <stdint.h>
#include <stddef.h>

void process_audio_chunk(const uint8_t* input, uint8_t* output, size_t len) {
    for (size_t i = 0; i < len; i++) {
        output[i] = input[i] ^ 0x42;
    }
}
EOF

    cat << 'EOF' > /home/user/ws_proxy/Cargo.toml
[package]
name = "ws_proxy"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
warp = "0.3"
futures = "0.3"
EOF

    cat << 'EOF' > /home/user/ws_proxy/src/main.rs
// Intentional lifetime and FFI errors
fn main() {
    println!("Server starting...");
}
EOF

    cat << 'EOF' > /home/user/client.py
import asyncio
import websockets

async def hello():
    pass
EOF

    touch /app/intercepted_comms.wav

    # Install whisper.cpp
    git clone https://github.com/ggerganov/whisper.cpp.git /opt/whisper.cpp
    cd /opt/whisper.cpp
    make -j4
    bash ./models/download-ggml-model.sh tiny.en

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app
    chmod -R 777 /opt/whisper.cpp