apt-get update && apt-get install -y python3 python3-pip git cargo
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cd /home/user
    cat << 'EOF' > gen_pcap.py
import struct
with open('trace.pcap', 'wb') as f:
    # Global header (magic, major, minor, thiszone, sigfigs, snaplen, network)
    f.write(struct.pack('<IHHIIII', 0xa1b2c3d4, 2, 4, 0, 0, 65535, 1))
    # Packets: ts_sec, ts_usec, incl_len, orig_len
    sizes = [50, 100, 150, 200, 250]
    for i, size in enumerate(sizes):
        f.write(struct.pack('<IIII', i, 0, size, size))
        f.write(b'\x00' * size)
EOF
    python3 gen_pcap.py
    rm gen_pcap.py

    cargo new flow-analyzer --vcs none
    cd flow-analyzer

    cat << 'EOF' > src/main.rs
use std::env;
use std::fs::File;
use std::io::Read;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <file.pcap>", args[0]);
        std::process::exit(1);
    }

    let mut file = File::open(&args[1]).expect("Failed to open file");
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer).expect("Failed to read");

    // Skip 24 byte global header
    if buffer.len() < 24 { return; }
    let mut offset = 24;
    let mut packet_sizes = Vec::new();

    while offset + 16 <= buffer.len() {
        let incl_len = u32::from_le_bytes(buffer[offset+8..offset+12].try_into().unwrap()) as usize;
        packet_sizes.push(incl_len);
        offset += 16 + incl_len;
    }

    let window_size = 3;
    for i in 0..packet_sizes.len() {
        // Calculate moving average
        let start = if i < window_size { 0 } else { i - window_size };
        let end = i;

        let window = &packet_sizes[start..end];
        if window.is_empty() {
            continue;
        }
        let sum: usize = window.iter().sum();
        let avg = sum / window.len();
        println!("Window avg ending at index {}: {}", i, avg);
    }
}
EOF

    git config --global user.email "dev@example.com"
    git config --global user.name "Dev"
    git config --global init.defaultBranch main

    git init
    git add .
    git commit -m "Initial commit"
    git tag v1.0

    for i in {1..50}; do
        echo "// Dummy comment $i" >> src/main.rs
        git commit -am "Minor update $i"
    done

    sed -i 's/let end = i;/let end = i + 1;/g' src/main.rs
    git commit -am "Refactor windowing logic"
    BAD_COMMIT=$(git rev-parse HEAD)

    for i in {51..100}; do
        echo "// Another dummy comment $i" >> src/main.rs
        git commit -am "More updates $i"
    done

    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    chmod -R 777 /home/user