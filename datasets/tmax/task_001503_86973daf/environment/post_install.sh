apt-get update && apt-get install -y python3 python3-pip python3-opencv python3-numpy cargo rustc
    pip3 install pytest

    mkdir -p /app

    # Create video generation script
    cat << 'EOF' > /app/gen_video.py
import cv2
import numpy as np

secret = b"SUPER_SECRET_TRAFFIC_KEY_9921"
width, height = 1280, 720
fps = 10

out = cv2.VideoWriter('/app/traffic_monitor.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

for byte in secret:
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(8):
        bit = (byte >> (7 - i)) & 1
        if bit:
            # White square
            frame[0:160, i*160:(i+1)*160] = (255, 255, 255)
    out.write(frame)

out.release()
EOF
    python3 /app/gen_video.py

    # Create Oracle Rust implementation
    cat << 'EOF' > /app/oracle.rs
use std::io::{self, BufRead};

fn main() {
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        let line = line.unwrap();
        if line.is_empty() { continue; }

        if !line.contains("[TLS:OK]") {
            println!("DENY: Invalid TLS");
            continue;
        }

        if line.contains("<script>") || line.contains("javascript:") {
            println!("DENY: XSS detected");
            continue;
        }

        if line.contains("' OR ") || line.contains("UNION SELECT") {
            println!("DENY: SQLi detected");
            continue;
        }

        let username = line.split_whitespace().next().unwrap_or("");
        if username == "root" || username == "admin" {
            println!("DENY: Privilege escalation");
            continue;
        }

        println!("ALLOW");
    }
}
EOF
    rustc /app/oracle.rs -o /app/oracle_log_analyzer

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app