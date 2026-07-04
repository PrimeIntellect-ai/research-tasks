apt-get update && apt-get install -y python3 python3-pip curl wget gcc g++ make ffmpeg
    pip3 install pytest openai-whisper gTTS

    # Install Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    export PATH="/root/.cargo/bin:${PATH}"
    rustup target add x86_64-unknown-linux-musl

    mkdir -p /app

    # Create whisper-cli wrapper
    cat << 'EOF' > /usr/local/bin/whisper-cli
#!/bin/bash
whisper "$@"
EOF
    chmod +x /usr/local/bin/whisper-cli

    # Generate audio file
    python3 -c "from gtts import gTTS; gTTS('The C bindings need to be compiled with the f P I C flag, and you must cross-compile the rust target to x 86 64 unknown linux musl. Also, make sure to explicitly link the m library for the math functions.').save('/app/dev_note.mp3')"
    ffmpeg -i /app/dev_note.mp3 -ar 16000 /app/dev_note.wav
    rm /app/dev_note.mp3

    # Create oracle
    cat << 'EOF' > /app/oracle_eval
#!/bin/bash
python3 -c "print(eval(r'''$1'''))"
EOF
    chmod +x /app/oracle_eval

    # Create rust project
    mkdir -p /home/user/rust_evaluator/src
    cat << 'EOF' > /home/user/rust_evaluator/Cargo.toml
[package]
name = "rust_evaluator"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    cat << 'EOF' > /home/user/rust_evaluator/src/main.rs
fn main() {
    println!("Hello, world!");
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app