apt-get update && apt-get install -y python3 python3-pip curl build-essential
    pip3 install pytest

    # Install Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    export PATH="/root/.cargo/bin:${PATH}"

    # Create /app directory
    mkdir -p /app

    # Create vendored crate seq_utils
    mkdir -p /app/seq_utils/src
    cat << 'EOF' > /app/seq_utils/Cargo.toml
[package]
name = "seq_utils"
version = "0.1.0"
edition = "2021"
EOF

    cat << 'EOF' > /app/seq_utils/src/lib.rs
pub fn melting_temp(seq: &str) -> u32 {
    let mut count_a = 0;
    let mut count_c = 0;
    let mut count_g = 0;
    let mut count_t = 0;

    for c in seq.chars() {
        match c {
            'A' => count_a += 1,
            'C' => count_c += 1,
            'G' => count_g += 1,
            'T' => count_t += 1,
            _ => {}
        }
    }

    // Bug: 2 * (A + G) + 4 * (T + C) instead of 2*(A+T) + 4*(G+C)
    2 * (count_a + count_g) + 4 * (count_t + count_c)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wallace_rule() {
        assert_eq!(melting_temp("ATGC"), 12); // 2*(2) + 4*(2) = 12. Bug gives: 2*(2) + 4*(2) = 12
        assert_eq!(melting_temp("AAAA"), 8);  // 2*(4) + 4*(0) = 8. Bug gives: 2*(4) + 4*(0) = 8
        assert_eq!(melting_temp("GGGG"), 16); // 2*(0) + 4*(4) = 16. Bug gives: 2*(4) + 4*(0) = 8 (Fails)
    }
}
EOF

    # Create oracle_analyzer
    mkdir -p /tmp/oracle
    cat << 'EOF' > /tmp/oracle/main.rs
use std::io::{self, Read};

fn main() {
    let mut input = String::new();
    io::stdin().read_to_string(&mut input).unwrap();
    let mut seq = String::new();
    for line in input.lines() {
        if line.starts_with('>') { continue; }
        seq.push_str(line.trim());
    }

    if seq.len() < 20 {
        println!("TOO_SHORT");
        return;
    }

    let mut bins = vec![0; 10];
    let bytes = seq.as_bytes();
    for i in 0..=(bytes.len() - 20) {
        let window = &bytes[i..i+20];
        let mut at = 0;
        let mut gc = 0;
        for &b in window {
            if b == b'A' || b == b'T' { at += 1; }
            if b == b'G' || b == b'C' { gc += 1; }
        }
        let tm = 2 * at + 4 * gc;
        let mut idx = (tm - 40) / 4;
        if idx > 9 { idx = 9; }
        bins[idx as usize] += 1;
    }

    let strs: Vec<String> = bins.into_iter().map(|b| b.to_string()).collect();
    println!("{}", strs.join(","));
}
EOF
    rustc /tmp/oracle/main.rs -o /app/oracle_analyzer
    rm -rf /tmp/oracle

    # Make Rust available to all users
    chmod -R 777 /root/.cargo || true
    chmod -R 777 /root/.rustup || true

    # Create user
    useradd -m -s /bin/bash user || true

    # Add Rust to user's path
    echo 'export PATH="/root/.cargo/bin:${PATH}"' >> /home/user/.bashrc

    chmod -R 777 /app
    chmod -R 777 /home/user