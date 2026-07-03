apt-get update && apt-get install -y python3 python3-pip git cargo tshark tcpdump
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # 1. Create Git Repo with Bisection setup and Dependency Conflict
    mkdir -p /home/user/pipeline_repo
    cd /home/user/pipeline_repo
    git init

    cat << 'EOF' > Cargo.toml
[package]
name = "pipeline"
version = "0.1.0"
edition = "2021"

[dependencies]
chrono = "0.4.20"
EOF

    mkdir -p src
    cat << 'EOF' > src/main.rs
pub fn process_timestamp(ts: &str) -> bool {
    !ts.is_empty()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_process() {
        assert!(process_timestamp("2023-11-05T01:30:00-09:00"));
    }
}
fn main() {}
EOF

    git add .
    git config user.email "test@example.com"
    git config user.name "Test User"
    git commit -m "Initial commit - pipeline parsing"

    # Good commits
    for i in {1..2}; do
        echo "// comment $i" >> src/main.rs
        git commit -am "Update $i"
    done

    # BAD COMMIT (Introduces panic on the specific timestamp)
    cat << 'EOF' > src/main.rs
pub fn process_timestamp(ts: &str) -> bool {
    if ts.contains("-09:00") {
        panic!("Timezone offset bug triggered!");
    }
    !ts.is_empty()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_process() {
        assert!(process_timestamp("2023-11-05T01:30:00-09:00"));
    }
}
fn main() {}
EOF
    git commit -am "Add timezone parsing logic"
    BAD_COMMIT=$(git rev-parse HEAD)

    # More commits
    for i in {3..4}; do
        echo "// more comments $i" >> src/main.rs
        git commit -am "More updates $i"
    done

    # Current HEAD: Introduce dependency conflict
    cat << 'EOF' > Cargo.toml
[package]
name = "pipeline"
version = "0.1.0"
edition = "2021"

[dependencies]
chrono = "=0.4.20"
serde = "1.0"
# Conflicting requirement (e.g. invalid feature or broken duplicate)
chrono-tz = { version = "0.8", features = ["invalid_feature_xyz"] }
EOF
    git commit -am "Add new dependencies for future work"

    # 2. Create Memory Dump
    head -c 2000 /dev/urandom > /home/user/crash_dump.bin
    echo -n '{"timestamp": "2023-11-05T01:30:00-09:00", "sensor": 42}' >> /home/user/crash_dump.bin
    head -c 1500 /dev/urandom >> /home/user/crash_dump.bin

    # 3. Create PCAP
    cat << 'EOF' > /tmp/hexdump.txt
000000 45 00 00 48 00 00 40 00 40 06 a5 f7 c0 a8 01 69
000010 c0 a8 01 0a 04 d2 00 50 00 00 00 00 00 00 00 00
000020 50 02 20 00 ee e6 00 00 7b 22 74 69 6d 65 73 74
000030 61 6d 70 22 3a 20 22 32 30 32 33 2d 31 31 2d 30
000040 35 54 30 31 3a 33 30 3a 30 30 2d 30 39 3a 30 30
000050 22 7d 0a
EOF
    text2pcap /tmp/hexdump.txt /home/user/traffic.pcap > /dev/null 2>&1
    rm /tmp/hexdump.txt

    # Save expected bad commit for tests
    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    chown -R user:user /home/user
    chmod -R 777 /home/user