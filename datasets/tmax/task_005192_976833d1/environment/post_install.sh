apt-get update && apt-get install -y python3 python3-pip ffmpeg curl build-essential
    pip3 install pytest opencv-python-headless numpy

    # Install Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    export PATH="/root/.cargo/bin:${PATH}"

    mkdir -p /app

    # Generate video
    cat << 'EOF' > /tmp/gen_video.py
import cv2
import numpy as np
import random

frames = 300
red_frames = 47
red_indices = random.sample(range(frames), red_frames)

out = cv2.VideoWriter('/app/audit_visual_log.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (100, 100))

for i in range(frames):
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    if i in red_indices:
        img[0, 0] = [0, 0, 255] # BGR for cv2
    out.write(img)
out.release()
EOF
    python3 /tmp/gen_video.py

    # Build oracle
    cargo new /tmp/oracle_build
    cd /tmp/oracle_build
    cargo add md5
    cat << 'EOF' > src/main.rs
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("INVALID");
        return;
    }
    let input = &args[1];

    let parts: Vec<&str> = input.split(';').collect();
    if parts.len() != 3 {
        println!("INVALID");
        return;
    }

    let user_part = parts[0];
    let esc_part = parts[1];
    let tok_part = parts[2];

    if !user_part.starts_with("USER:") || !esc_part.starts_with("ESCALATION:") || !tok_part.starts_with("TOKEN:") {
        println!("INVALID");
        return;
    }

    let username = &user_part[5..];
    let level = &esc_part[11..];
    let token = &tok_part[6..];

    if !username.chars().all(|c| c.is_ascii_alphanumeric()) || username.is_empty() {
        println!("INVALID");
        return;
    }

    if !level.chars().all(|c| c.is_ascii_digit()) || level.is_empty() {
        println!("INVALID");
        return;
    }

    let secret = "47";
    let data_to_hash = format!("{}{}{}", username, level, secret);
    let digest = md5::compute(data_to_hash);
    let expected_token = format!("{:x}", digest);

    if token == expected_token {
        println!("VALID");
    } else {
        println!("INVALID");
    }
}
EOF
    cargo build --release
    cp target/release/oracle_build /app/oracle_audit_verifier
    chmod +x /app/oracle_audit_verifier

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user