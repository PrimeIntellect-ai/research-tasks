apt-get update && apt-get install -y python3 python3-pip rustc cargo tcpdump tshark
    pip3 install pytest scapy

    mkdir -p /home/user/c2_agent/src

    cat << 'EOF' > /home/user/c2_agent/Cargo.toml
[package]
name = "c2_agent"
version = "0.1.0"
edition = "2021"
EOF

    cat << 'EOF' > /home/user/c2_agent/src/main.rs
use std::env;
use std::fs::File;
// use std::io::Read;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Usage: c2_agent <payload_file>");
        return;
    }
    let mut file = File::open(&args[1]).expect("Failed to open file");
    let mut contents = Vec::new();

    // Compilation will fail here because Read trait is not in scope
    file.read_to_end(&mut contents).expect("Failed to read file");

    let trigger = [0xde, 0xad, 0xbe, 0xef, 0x42];

    if contents.windows(trigger.len()).any(|w| w == trigger) {
        println!("[!] C2 INSTRUCTION RECEIVED");
    } else {
        println!("IDLE");
    }
}
EOF

    cat << 'EOF' > /tmp/gen_pcap.py
from scapy.all import *

# Generate a packet with junk, the trigger, and more junk
payload = b'\x00\x11\x22\x33' * 10 + b'\xde\xad\xbe\xef\x42' + b'\xaa\xbb\xcc' * 10
pkt = IP(dst="192.168.1.100", src="192.168.1.200")/TCP(dport=1337, sport=54321)/Raw(load=payload)

wrpcap('/home/user/capture.pcap', [pkt])
EOF

    python3 /tmp/gen_pcap.py
    rm /tmp/gen_pcap.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/c2_agent /home/user/capture.pcap
    chmod -R 777 /home/user