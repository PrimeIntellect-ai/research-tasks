apt-get update && apt-get install -y python3 python3-pip clang build-essential cargo rustc
    pip3 install pytest

    mkdir -p /home/user
    cd /home/user
    cargo new wav_filter
    cd wav_filter

    mkdir -p src lib

    cat << 'EOF' > src/wavcheck.c
#include <stdint.h>
int check_header_integrity(const uint8_t* header) {
    return 1;
}
EOF

    gcc -c src/wavcheck.c -o src/wavcheck.o
    ar rcs lib/libwavcheck.a src/wavcheck.o

    cat << 'EOF' > build.rs
fn main() {
    // Intentionally misconfigured: missing link search and link lib
}
EOF

    cat << 'EOF' > src/main.rs
extern "C" {
    fn check_header_integrity(header: *const u8) -> i32;
}

fn main() {
    let header = [0u8; 44];
    unsafe {
        check_header_integrity(header.as_ptr());
    }
}
EOF

    mkdir -p /app/corpus/clean /app/corpus/evil /app/quarantine

    # Create dummy WAV file for the quarantine fixture
    touch /app/quarantine/incident_099.wav

    # Create user
    useradd -m -s /bin/bash user || true

    chmod -R 777 /home/user /app