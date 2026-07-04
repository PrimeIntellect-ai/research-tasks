apt-get update && apt-get install -y python3 python3-pip cargo
    pip3 install pytest

    mkdir -p /home/user/ticket_4092
    cd /home/user/ticket_4092
    cargo new sensor_stats

    cat << 'EOF' > /home/user/ticket_4092/sensor_stats/src/main.rs
use std::env;
use std::fs::File;
use std::io::{self, BufRead};

fn compute_statistics(data: &[f64]) -> (f64, f64) {
    let n = data.len() as f64;
    if n == 0.0 {
        return (0.0, 0.0);
    }

    let mut sum = 0.0;
    let mut sum_sq = 0.0;

    for &val in data {
        sum += val;
        sum_sq += val * val;
    }

    let mean = sum / n;
    let variance = (sum_sq / n) - (mean * mean);

    // The bug: variance can be slightly negative due to floating point inaccuracies
    let std_dev = variance.sqrt();

    if std_dev.is_nan() {
        panic!("Numerical instability detected: standard deviation is NaN");
    }

    (mean, std_dev)
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <data.csv>", args[0]);
        std::process::exit(1);
    }

    let file = File::open(&args[1]).expect("Failed to open file");
    let mut data = Vec::new();

    for line in io::BufReader::new(file).lines() {
        if let Ok(val_str) = line {
            if let Ok(val) = val_str.trim().parse::<f64>() {
                data.push(val);
            }
        }
    }

    let (mean, std_dev) = compute_statistics(&data);
    println!("Mean: {:.4}, StdDev: {:.4}", mean, std_dev);
}
EOF

    cat << 'EOF' > /tmp/generate_data.py
import random

with open('/home/user/ticket_4092/sensor_data.csv', 'w') as f:
    for i in range(9900):
        # Normal data
        f.write(f"{random.uniform(10.0, 20.0)}\n")

    # Poison data that causes catastrophic cancellation
    # Very large numbers, very close to each other
    f.write("10000000000.0\n")
    f.write("10000000000.0000001\n")
    f.write("10000000000.0000002\n")

    for i in range(97):
        f.write(f"{random.uniform(10.0, 20.0)}\n")
EOF

    python3 /tmp/generate_data.py
    rm /tmp/generate_data.py

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user