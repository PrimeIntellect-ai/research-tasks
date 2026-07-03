apt-get update && apt-get install -y python3 python3-pip cargo
    pip3 install pytest

    mkdir -p /home/user/sim/src
    cd /home/user/sim

    cat << 'EOF' > Cargo.toml
[package]
name = "sim"
version = "0.1.0"
edition = "2021"

[dependencies]
rayon = "1.7"
rand = "0.8"
EOF

    cat << 'EOF' > src/main.rs
use rayon::prelude::*;
use rand::{SeedableRng, Rng};
use rand::rngs::StdRng;

fn main() {
    let mut rng = StdRng::seed_from_u64(42); // Fixed seed for array generation
    let mut data: Vec<f64> = (0..1_000_000).map(|_| {
        let v: f64 = rng.gen_range(-1000.0..1000.0);
        v.exp() * 1e-10 // Creates varying magnitudes
    }).collect();

    // Sort to make magnitudes wildly different
    data.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());

    // Parallel sum introduces reduction order non-determinism
    let sum: f64 = data.par_iter().cloned().sum();

    println!("{:.10}", sum);
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user