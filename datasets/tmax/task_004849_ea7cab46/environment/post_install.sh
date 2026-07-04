apt-get update && apt-get install -y python3 python3-pip curl build-essential tesseract-ocr
    pip3 install pytest Pillow

    # Install Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    export PATH="/root/.cargo/bin:${PATH}"

    mkdir -p /app
    mkdir -p /home/user/signal_filter/src

    # Create oracle source
    mkdir -p /tmp/oracle_src
    cat << 'EOF' > /tmp/oracle_src/main.rs
use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let nums: Vec<f64> = input.split_whitespace().filter_map(|s| s.parse().ok()).collect();
    if nums.len() < 3 { return; }
    let out: Vec<f64> = nums.windows(3).map(|w| {
        w[0] * 0.125 + w[1] * 0.75 + w[2] * 0.125 + 0.05
    }).collect();

    for (i, v) in out.iter().enumerate() {
        if i > 0 { print!(" "); }
        print!("{:.6}", v);
    }
    println!();
}
EOF
    rustc -O /tmp/oracle_src/main.rs -o /app/oracle_filter
    strip /app/oracle_filter

    # Generate kernel image
    cat << 'EOF' > /tmp/gen_image.py
from PIL import Image, ImageDraw
img = Image.new('RGB', (400, 100), color=(255, 255, 255))
d = ImageDraw.Draw(img)
d.text((10, 10), "Kernel = [0.125, 0.75, 0.125]\nBias = 0.05", fill=(0, 0, 0))
img.save('/app/kernel.png')
EOF
    python3 /tmp/gen_image.py

    # Create buggy project
    cat << 'EOF' > /home/user/signal_filter/Cargo.toml
[package]
name = "signal_filter"
version = "0.1.0"
edition = "2021"

[dependencies]
rayon = "=1.5.0"
rayon-core = "=1.10.0"
EOF

    cat << 'EOF' > /home/user/signal_filter/src/main.rs
use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let nums: Vec<f32> = input.split_whitespace().filter_map(|s| s.parse().ok()).collect();

    // Buggy implementation
    if nums.len() < 3 { return; }
    for i in 0..nums.len()-2 {
        let val = nums[i] * 0.1 + nums[i+1] * 0.8 + nums[i+2] * 0.1;
        if i > 0 { print!(" "); }
        print!("{:.6}", val);
    }
    println!();
}
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user