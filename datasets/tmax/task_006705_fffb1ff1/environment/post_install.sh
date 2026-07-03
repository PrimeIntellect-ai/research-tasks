apt-get update && apt-get install -y python3 python3-pip git cargo rustc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/chrono_shift
    cd /home/user/chrono_shift

    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"

    # Cargo.toml
    cat << 'EOF' > Cargo.toml
[package]
name = "chrono_shift"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    # src/lib.rs
    mkdir -p src tests
    cat << 'EOF' > src/lib.rs
pub mod parser;
EOF

    # src/parser.rs (Good version)
    cat << 'EOF' > src/parser.rs
pub fn parse_timezone(input: &str) -> Result<&str, &'static str> {
    if input.len() < 19 {
        return Err("Invalid Timezone");
    }
    match input.get(19..) {
        Some(tz) => Ok(tz),
        None => Err("Invalid Timezone")
    }
}
EOF

    # tests/test_parser.rs
    cat << 'EOF' > tests/test_parser.rs
use chrono_shift::parser::parse_timezone;

#[test]
fn test_valid_timezone() {
    assert_eq!(parse_timezone("2023-10-12T05:00:00-05:00"), Ok("-05:00"));
}

#[test]
fn test_corrupted_timezone() {
    // Too short
    assert_eq!(parse_timezone("2023-10-12"), Err("Invalid Timezone"));

    // Invalid character boundary at index 19
    let bad_str = "2023-10-12T05:00:0\u{2800}Z"; 
    assert_eq!(parse_timezone(bad_str), Err("Invalid Timezone"));
}
EOF

    git add .
    git commit -m "Commit 1: Initial implementation"

    # Commit 2: Dummy commit
    echo "// doc update" >> src/lib.rs
    git add src/lib.rs
    git commit -m "Commit 2: Update documentation"

    # Commit 3: Bad commit (Introduces panic)
    cat << 'EOF' > src/parser.rs
pub fn parse_timezone(input: &str) -> Result<&str, &'static str> {
    // Optimized timezone extraction (BUG: Panics on out-of-bounds or char boundary)
    let tz_offset = &input[19..];
    Ok(tz_offset)
}
EOF
    git add src/parser.rs
    git commit -m "Commit 3: Optimize timezone extraction"
    git rev-parse HEAD > /tmp/expected_bad_commit.txt

    # Commit 4: Dummy commit
    echo "// another doc update" >> src/lib.rs
    git add src/lib.rs
    git commit -m "Commit 4: Minor formatting"

    # Ensure permissions
    chown -R user:user /home/user/chrono_shift
    chmod -R 777 /home/user