apt-get update && apt-get install -y python3 python3-pip curl ffmpeg
    pip3 install pytest

    # Install Rust
    export RUSTUP_HOME=/opt/rustup
    export CARGO_HOME=/opt/cargo
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
    export PATH=/opt/cargo/bin:$PATH

    mkdir -p /app
    mkdir -p /home/user/biocore_sim/src

    # Generate synthetic video
    ffmpeg -f lavfi -i color=c=black:s=10x10:d=5 -c:v libx264 -y /app/reaction_video.mp4

    # Generate reference fasta
    echo ">seq1\nATGCGTACGTAGCTAGCTAGCTAGCTAGCTAGCTAGCTAG" > /app/reference.fasta

    # Create Rust project
    cat << 'EOF' > /home/user/biocore_sim/Cargo.toml
[package]
name = "biocore_sim"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
EOF

    cat << 'EOF' > /home/user/biocore_sim/src/main.rs
use std::env;
use std::fs::File;
use std::io::Write;
use serde::Serialize;

mod alignment;
mod ode;
mod video;

#[derive(Serialize)]
struct Results {
    cq_value: f64,
    final_dna_concentration: f64,
    max_alignment_score: i32,
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 4 {
        eprintln!("Usage: biocore_sim <video> <fasta> <output>");
        std::process::exit(1);
    }

    let video_path = &args[1];
    let fasta_path = &args[2];
    let out_path = &args[3];

    let cq = video::process_video(video_path);
    let dna = ode::simulate(cq);
    let score = alignment::align(fasta_path);

    let res = Results {
        cq_value: cq,
        final_dna_concentration: dna,
        max_alignment_score: score,
    };

    let json = serde_json::to_string(&res).unwrap();
    let mut f = File::create(out_path).unwrap();
    f.write_all(json.as_bytes()).unwrap();
}
EOF

    cat << 'EOF' > /home/user/biocore_sim/src/video.rs
pub fn process_video(_path: &str) -> f64 {
    // Deliberately slow
    let mut sum = 0.0;
    for _ in 0..10000000 {
        let v: Vec<f64> = vec![1.0, 2.0];
        sum += v[0] * 0.00000001;
    }
    12.8 + sum * 0.0
}
EOF

    cat << 'EOF' > /home/user/biocore_sim/src/ode.rs
pub fn simulate(_cq: f64) -> f64 {
    // Deliberately slow
    let mut sum = 0.0;
    for _ in 0..10000000 {
        let v: Vec<f64> = vec![1.0];
        sum += v[0] * 0.00000001;
    }
    0.92 + sum * 0.0
}
EOF

    cat << 'EOF' > /home/user/biocore_sim/src/alignment.rs
pub fn align(_path: &str) -> i32 {
    // Deliberately slow
    let mut sum = 0;
    for _ in 0..10000000 {
        let v: Vec<i32> = vec![1];
        sum += v[0] * 0;
    }
    156 + sum
}
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/biocore_sim
    chmod -R 777 /home/user
    chmod -R 777 /opt/cargo