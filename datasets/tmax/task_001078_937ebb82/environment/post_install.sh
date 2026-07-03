apt-get update && apt-get install -y python3 python3-pip cargo rustc
    pip3 install pytest

    # Create vendored package
    mkdir -p /app/welford_cli/src

    cat << 'EOF' > /app/welford_cli/Cargo.toml
[package]
name = "welford_cli"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    cat << 'EOF' > /app/welford_cli/build.rs
fn main() {
    println!("cargo:rustc-link-lib=nonexistent_mathlib");
}
EOF

    cat << 'EOF' > /app/welford_cli/src/main.rs
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut count: u64 = 0;
    let mut sum: f64 = 0.0;
    let mut sum_sq: f64 = 0.0;

    for line in stdin.lock().lines() {
        let line = line.unwrap();
        if let Ok(x) = line.trim().parse::<f64>() {
            count += 1;
            sum += x;
            sum_sq += x * x;

            let variance = if count > 1 {
                (sum_sq - (sum * sum) / (count as f64)) / (count as f64 - 1.0)
            } else {
                0.0
            };

            println!("{},{},{}", count, sum / (count as f64), variance);
        }
    }
}
EOF

    # Create oracle
    mkdir -p /opt/oracle/src

    cat << 'EOF' > /opt/oracle/Cargo.toml
[package]
name = "oracle"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    cat << 'EOF' > /opt/oracle/src/main.rs
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    let mut count: u64 = 0;
    let mut mean: f64 = 0.0;
    let mut m2: f64 = 0.0;

    for line in stdin.lock().lines() {
        let line = line.unwrap();
        if let Ok(x) = line.trim().parse::<f64>() {
            count += 1;
            let delta = x - mean;
            mean += delta / (count as f64);
            let delta2 = x - mean;
            m2 += delta * delta2;

            let variance = if count > 1 {
                m2 / (count as f64 - 1.0)
            } else {
                0.0
            };

            println!("{},{},{}", count, mean, variance);
        }
    }
}
EOF

    cd /opt/oracle
    cargo build --release
    mv target/release/oracle /opt/oracle/welford_cli
    rm -rf target src Cargo.toml Cargo.lock
    chmod +x /opt/oracle/welford_cli

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user