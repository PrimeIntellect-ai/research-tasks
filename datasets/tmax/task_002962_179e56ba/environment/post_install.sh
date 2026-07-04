apt-get update && apt-get install -y python3 python3-pip curl build-essential tar
    pip3 install pytest

    # Install Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    export PATH="/root/.cargo/bin:${PATH}"

    # Setup vendored package
    mkdir -p /app/vendor
    cd /app/vendor
    curl -L https://crates.io/api/v1/crates/regex/1.10.4/download | tar -xz
    # Perturbation
    sed -i 's/name = "regex"/name = "regex-broken"/' /app/vendor/regex-1.10.4/Cargo.toml

    # Setup oracle binary
    mkdir -p /app/oracle_build
    cd /app/oracle_build
    cargo new oracle_bin
    cd oracle_bin
    cargo add regex@1.10.4

    cat << 'EOF' > src/main.rs
use std::io::{self, BufRead};
use regex::Regex;

fn main() {
    let re = Regex::new(r"(pin=)\d+").unwrap();
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        if let Ok(mut text) = line {
            if text.contains("CWE-79") || text.contains("CWE-89") {
                text = format!("[ALERT] {}", text);
            }
            let sanitized = re.replace_all(&text, "${1}XXXX");
            println!("{}", sanitized);
        }
    }
}
EOF

    cargo build --release
    mkdir -p /app/oracle
    cp target/release/oracle_bin /app/oracle/audit_sanitizer

    # Cleanup build dir
    cd /
    rm -rf /app/oracle_build

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chmod -R 777 /app
    chmod -R 777 /home/user