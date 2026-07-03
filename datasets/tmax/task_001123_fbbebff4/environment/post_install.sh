apt-get update && apt-get install -y python3 python3-pip gcc make cargo
    pip3 install pytest python-dotenv requests

    mkdir -p /home/user/project/legacy_c
    mkdir -p /home/user/project/rust_wrapper/src
    mkdir -p /home/user/project/services

    # Create C Library files
    cat << 'EOF' > /home/user/project/legacy_c/checksum.c
#include <stdint.h>
#include <stddef.h>

uint32_t compute_checksum(const uint8_t* data, size_t len) {
    uint32_t sum = 0;
    for(size_t i=0; i<len; i++) {
        sum += data[i];
    }
    return sum;
}
EOF

    cat << 'EOF' > /home/user/project/legacy_c/Makefile
all:
	gcc -shared -o libchecksum.so checksum.c
EOF

    # Create Rust wrapper files
    cat << 'EOF' > /home/user/project/rust_wrapper/Cargo.toml
[package]
name = "rust_wrapper"
version = "0.1.0"
edition = "2021"

[dependencies]
hex = "0.4"
EOF

    cat << 'EOF' > /home/user/project/rust_wrapper/build.rs
fn main() {
    // Missing link directives
}
EOF

    cat << 'EOF' > /home/user/project/rust_wrapper/src/main.rs
use std::env;

extern "C" {
    fn compute_checksum(data: *const u8, len: usize) -> u32;
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <hex_string>", args[0]);
        std::process::exit(1);
    }
    let hex_str = &args[1];
    let bytes = hex::decode(hex_str).expect("Invalid hex string");

    let sum = unsafe { compute_checksum(bytes.as_ptr(), bytes.len()) };
    println!("{}", sum);
}
EOF

    # Create Services files
    cat << 'EOF' > /home/user/project/services/.env
VALIDATOR_BIN=
LD_LIBRARY_PATH=
EOF

    cat << 'EOF' > /home/user/project/services/start.sh
#!/bin/bash
# Mock start script
echo "Starting services..."
EOF
    chmod +x /home/user/project/services/start.sh

    cat << 'EOF' > /home/user/project/services/test_flow.py
import pytest
import os

def test_flow():
    # Mock test flow
    assert True
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user