apt-get update && apt-get install -y python3 python3-pip git cargo python3-scapy
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    mkdir -p /home/user/packet-parser
    cd /home/user/packet-parser

    cat << 'EOF' > Cargo.toml
[package]
name = "packet-parser"
version = "0.1.0"
edition = "2021"

[dependencies]
pcap-parser = "0.14"
EOF

    mkdir src
    cat << 'EOF' > src/parser.rs
#[derive(Debug)]
pub struct TlvNode {
    pub typ: u8,
    pub val: Vec<u8>,
}

pub fn parse_tlv(data: &[u8]) -> Result<Vec<TlvNode>, &'static str> {
    let mut offset = 0;
    let mut nodes = Vec::new();

    while offset < data.len() {
        if offset + 2 > data.len() {
            break;
        }
        let typ = data[offset];
        let len = data[offset + 1] as usize;

        if len == 0 {
            return Err("Zero length not allowed");
        }

        if offset + 2 + len > data.len() {
            break;
        }

        nodes.push(TlvNode {
            typ,
            val: data[offset + 2 .. offset + 2 + len].to_vec(),
        });

        offset += 2 + len;
    }

    Ok(nodes)
}
EOF

    cat << 'EOF' > src/main.rs
mod parser;
use pcap_parser::*;
use pcap_parser::traits::PcapReaderIterator;
use std::fs::File;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <pcap>", args[0]);
        return;
    }
    let file = File::open(&args[1]).unwrap();
    let mut num_blocks = 0;
    let mut reader = LegacyPcapReader::new(65536, file).unwrap();
    loop {
        match reader.next() {
            Ok((offset, block)) => {
                num_blocks += 1;
                match block {
                    PcapBlockOwned::Legacy(b) => {
                        // Skip mock ethernet/IP/UDP headers (assume fixed 42 bytes for this test)
                        if b.data.len() > 42 {
                            let payload = &b.data[42..];
                            let _ = parser::parse_tlv(payload);
                        }
                    },
                    _ => ()
                }
                reader.consume(offset);
            },
            Err(PcapError::Eof) => break,
            Err(PcapError::Incomplete) => {
                reader.refill().unwrap();
            },
            Err(e) => panic!("error while reading: {:?}", e),
        }
    }
    println!("Processed {} blocks", num_blocks);
}
EOF

    git init
    git add .
    git commit -m "Initial commit: basic TLV parsing"

    echo "// minor change" >> src/parser.rs
    git commit -am "Minor formatting"

    cat << 'EOF' > src/parser.rs
#[derive(Debug)]
pub struct TlvNode {
    pub typ: u8,
    pub val: Vec<u8>,
}

pub fn parse_tlv(data: &[u8]) -> Result<Vec<TlvNode>, &'static str> {
    let mut offset = 0;
    let mut nodes = Vec::new();

    while offset < data.len() {
        if offset + 2 > data.len() {
            break;
        }
        let typ = data[offset];
        let len = data[offset + 1] as usize;

        // BUG INTRODUCED HERE: allow 0 length but forget to advance offset
        // This causes an infinite loop allocating empty nodes, leading to memory leak / hang
        if len == 0 {
            nodes.push(TlvNode { typ, val: vec![] });
            // Missing: offset += 2;
            continue; 
        }

        if offset + 2 + len > data.len() {
            break;
        }

        nodes.push(TlvNode {
            typ,
            val: data[offset + 2 .. offset + 2 + len].to_vec(),
        });

        offset += 2 + len;
    }

    Ok(nodes)
}
EOF
    git commit -am "Feature: support zero-length TLV nodes"
    BAD_COMMIT=$(git rev-parse HEAD)
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    echo "// another minor change" >> src/parser.rs
    git commit -am "Add comments"

    cat << 'EOF' > /tmp/gen_pcap.py
from scapy.all import *
# Payload: TLV type 1, len 2, val A, B. Then type 2, len 0.
payload = bytes([0x01, 0x02, 0x41, 0x42, 0x02, 0x00])
pkt = Ether()/IP(dst="127.0.0.1")/UDP(sport=1234, dport=5678)/Raw(load=payload)
wrpcap('/home/user/capture.pcap', [pkt])
EOF
    python3 /tmp/gen_pcap.py

    chown -R user:user /home/user/packet-parser /home/user/capture.pcap
    chmod -R 777 /home/user