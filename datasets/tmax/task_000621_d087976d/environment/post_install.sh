apt-get update && apt-get install -y python3 python3-pip
pip3 install pytest

# Install task dependencies
apt-get install -y espeak rustc cargo ffmpeg

mkdir -p /app
espeak -w /app/voicemail.wav "Use a base frequency of two point five, and a damping coefficient of zero point one five."

mkdir -p /app/oracle_src/src
cat << 'EOF' > /app/oracle_src/Cargo.toml
[package]
name = "oracle"
version = "0.1.0"
edition = "2021"
EOF

cat << 'EOF' > /app/oracle_src/src/main.rs
use std::env;
use std::f64::consts::PI;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 5 { return; }

    let n: usize = args[1].parse().unwrap();
    let f0: f64 = args[2].parse().unwrap();
    let damping: f64 = args[3].parse().unwrap();
    let steps: usize = args[4].parse().unwrap();
    let dt = 0.01;

    let mut x: Vec<f64> = (0..n)
        .map(|i| (2.0 * PI * f0 * (i as f64) / (n as f64)).sin())
        .collect();
    let mut v: Vec<f64> = vec![0.0; n];

    for _ in 0..steps {
        let mut v_new = vec![0.0; n];
        for i in 0..n {
            let left = (i + n - 1) % n;
            let right = (i + 1) % n;
            let force = (x[left] - 2.0 * x[i] + x[right]) - damping * v[i];
            v_new[i] = v[i] + force * dt;
        }
        for i in 0..n {
            x[i] += v_new[i] * dt;
            v[i] = v_new[i];
        }
    }

    let out: Vec<String> = x.iter().map(|val| format!("{:.6}", val)).collect();
    println!("{}", out.join(","));
}
EOF

cd /app/oracle_src && cargo build --release
cp target/release/oracle /app/oracle_bin
chmod +x /app/oracle_bin

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user