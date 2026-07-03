apt-get update && apt-get install -y python3 python3-pip curl git build-essential
    pip3 install pytest

    export RUSTUP_HOME=/opt/rustup
    export CARGO_HOME=/opt/cargo
    export PATH=/opt/cargo/bin:$PATH

    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    rustup toolchain install nightly
    cargo install cargo-fuzz

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/tz_utils
    cd /home/user/tz_utils

    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"

    cat << 'EOF' > Cargo.toml
[package]
name = "tz_utils"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    mkdir src
    cat << 'EOF' > src/lib.rs
pub fn local_day_start(ts: i64, tz_offset_sec: i64) -> i64 {
    let local_ts = ts + tz_offset_sec;
    let local_midnight = if local_ts >= 0 {
        (local_ts / 86400) * 86400
    } else {
        ((local_ts - 86399) / 86400) * 86400
    };
    local_midnight - tz_offset_sec
}

pub fn dummy1() {}
EOF

    cargo +nightly fuzz init
    cat << 'EOF' > fuzz/fuzz_targets/fuzz_target_1.rs
#![no_main]
use libfuzzer_sys::fuzz_target;
use tz_utils::local_day_start;

fuzz_target!(|data: (i64, i64)| {
    let (ts, offset) = data;
    if offset > -86400 && offset < 86400 {
        let start = local_day_start(ts, offset);
        assert_eq!((start + offset) % 86400, 0);
        assert!(ts - start >= 0 && ts - start < 86400);
    }
});
EOF

    git add .
    git commit -m "Initial commit with working local_day_start"

    for i in {1..3}; do
        echo "pub fn dummy_$i() {}" >> src/lib.rs
        git add src/lib.rs
        git commit -m "Add dummy_$i"
    done

    cat << 'EOF' > src/lib.rs
pub fn local_day_start(ts: i64, tz_offset_sec: i64) -> i64 {
    let local_ts = ts + tz_offset_sec;
    let local_midnight = if local_ts >= 0 {
        (local_ts / 86400) * 86400
    } else {
        ((local_ts - 86399) / 86400) * 86400
    };
    local_midnight
}

pub fn dummy1() {}
pub fn dummy_1() {}
pub fn dummy_2() {}
pub fn dummy_3() {}
EOF
    git add src/lib.rs
    git commit -m "Refactor local_day_start to simplify return value"
    git rev-parse HEAD > /tmp/expected_bad_commit.txt

    for i in {4..6}; do
        echo "pub fn dummy_$i() {}" >> src/lib.rs
        git add src/lib.rs
        git commit -m "Add dummy_$i"
    done

    chown -R user:user /home/user/tz_utils
    chmod -R 777 /opt/rustup /opt/cargo
    chmod -R 777 /home/user