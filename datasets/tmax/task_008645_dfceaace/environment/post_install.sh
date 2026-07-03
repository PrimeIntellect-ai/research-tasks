apt-get update && apt-get install -y python3 python3-pip curl build-essential
    pip3 install pytest

    export RUSTUP_HOME=/opt/rustup
    export CARGO_HOME=/opt/cargo
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    export PATH="/opt/cargo/bin:${PATH}"
    rustup target add riscv64gc-unknown-none-elf

    mkdir -p /home/user/accel_lib/src/c

    cat << 'EOF' > /home/user/accel_lib/Cargo.toml
[package]
name = "accel_lib"
version = "0.1.0"
edition = "2021"

[features]
fast_math = []

[build-dependencies]
cc = "1.0"
EOF

    cat << 'EOF' > /home/user/accel_lib/src/c/accel.c
#include <stdint.h>

#if defined(MATH_X86)
int32_t compute_val() { return 1; }
#elif defined(MATH_ARM)
int32_t compute_val() { return 2; }
#elif defined(MATH_GENERIC)
int32_t compute_val() { return 3; }
#else
#error "No valid math architecture defined"
#endif
EOF

    cat << 'EOF' > /home/user/accel_lib/src/lib.rs
#![no_std]

extern "C" {
    fn compute_val() -> i32;
}

pub fn get_val() -> i32 {
    unsafe { compute_val() }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_val() {
        let val = get_val();
        assert!(val == 1 || val == 2 || val == 3);
    }
}
EOF

    cat << 'EOF' > /home/user/accel_lib/build.rs
use std::env;

fn main() {
    println!("cargo:rerun-if-changed=src/c/accel.c");

    cc::Build::new()
        .file("src/c/accel.c")
        .define("MATH_X86", "1") // HARDCODED BUG
        .define("MATH_FAST", "1") // HARDCODED BUG
        .compile("accel");
}
EOF

    chmod -R 777 /opt/rustup /opt/cargo
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user