apt-get update && apt-get install -y python3 python3-pip cargo rustc binutils
pip3 install pytest

mkdir -p /app/oracle_src
cd /app/oracle_src
cargo init --bin
cat << 'EOF' > Cargo.toml
[package]
name = "conf_oracle"
version = "0.1.0"
edition = "2021"

[dependencies]
unicode-normalization = "0.1"
sha2 = "0.10"
EOF

cat << 'EOF' > src/main.rs
use std::io::{self, BufRead};
use std::collections::{HashMap, HashSet};
use unicode_normalization::UnicodeNormalization;
use sha2::{Sha256, Digest};

fn main() {
    let stdin = io::stdin();
    let mut state: HashMap<String, (HashSet<String>, Vec<usize>)> = HashMap::new();

    for line_res in stdin.lock().lines() {
        let line = match line_res {
            Ok(l) => l,
            Err(_) => break,
        };

        let parts: Vec<&str> = line.splitn(2, ' ').collect();
        if parts.len() != 2 { continue; }
        let key = parts[0].to_string();
        let payload = parts[1];

        let nfc_payload: String = payload.nfc().collect();

        let mut hasher = Sha256::new();
        hasher.update(nfc_payload.as_bytes());
        let hash_hex = format!("{:x}", hasher.finalize());

        let entry = state.entry(key.clone()).or_insert_with(|| (HashSet::new(), Vec::new()));

        if entry.0.contains(&hash_hex) {
            continue;
        }

        entry.0.insert(hash_hex);

        let char_len = nfc_payload.chars().count();
        entry.1.push(char_len);
        if entry.1.len() > 3 {
            entry.1.remove(0);
        }

        let sum: usize = entry.1.iter().sum();
        let avg = sum / entry.1.len();

        println!("{}:{}", key, avg);
    }
}
EOF

cargo build --release
cp target/release/conf_oracle /app/conf_oracle
strip /app/conf_oracle
cd /
rm -rf /app/oracle_src

useradd -m -s /bin/bash user || true
mkdir -p /home/user/tracker
chmod -R 777 /home/user