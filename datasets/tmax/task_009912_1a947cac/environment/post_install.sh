apt-get update && apt-get install -y python3 python3-pip curl gcc build-essential rustc cargo
    pip3 install pytest

    mkdir -p /home/user/ticket_4092/repo/src
    mkdir -p /home/user/ticket_4092/lib

    # Create the C library
    cat << 'EOF' > /home/user/ticket_4092/lib/checksum.c
#include <stdint.h>
#include <stddef.h>
uint32_t compute_checksum(const uint8_t* data, size_t len) {
    return 42;
}
EOF
    cd /home/user/ticket_4092/lib
    gcc -c checksum.c -o checksum.o
    ar rcs libchecksum.a checksum.o
    rm checksum.c checksum.o

    # Create Cargo.toml
    cat << 'EOF' > /home/user/ticket_4092/repo/Cargo.toml
[package]
name = "ticket_4092"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    # Create main.rs with the off-by-one error
    cat << 'EOF' > /home/user/ticket_4092/repo/src/main.rs
mod parser;

extern "C" {
    pub fn compute_checksum(data: *const u8, len: usize) -> u32;
}

fn main() {
    let data = vec![10, 20, 30, 40, 50];
    // Off-by-one error here: should be data.len() instead of data.len() - 1
    let result = parser::process_data(&data, 0, data.len() - 1);
    println!("Result: {}", result);
}
EOF

    # Create the disk image with the deleted parser.rs
    cd /home/user/ticket_4092
    dd if=/dev/urandom of=disk.img bs=1K count=1024 2>/dev/null
    echo "// BEGIN PARSER.RS" >> disk.img
    cat << 'EOF' >> disk.img
pub fn process_data(data: &[u8], start: usize, end: usize) -> u32 {
    let mut sum = 0;
    for i in start..end {
        sum += data[i] as u32;
    }
    unsafe {
        sum + crate::compute_checksum(data.as_ptr(), data.len())
    }
}
EOF
    echo "// END PARSER.RS" >> disk.img
    dd if=/dev/urandom bs=1K count=1024 >> disk.img 2>/dev/null

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user