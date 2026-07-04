apt-get update && apt-get install -y python3 python3-pip git rustc cargo
pip3 install pytest

mkdir -p /home/user/tlv_parser/src
mkdir -p /home/user/samples
cd /home/user/tlv_parser

git config --global user.email "test@example.com"
git config --global user.name "Test User"

git init
cat << 'EOF' > Cargo.toml
[package]
name = "tlv_parser"
version = "0.1.0"
edition = "2021"
EOF

cat << 'EOF' > src/main.rs
use std::env;
use std::fs::File;
use std::io::Read;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <file>", args[0]);
        std::process::exit(1);
    }

    let mut file = File::open(&args[1]).unwrap();
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer).unwrap();

    let mut cursor = 0;
    while cursor < buffer.len() {
        if cursor + 5 > buffer.len() { break; }
        let record_type = buffer[cursor];
        let length = u32::from_be_bytes([
            buffer[cursor+1], buffer[cursor+2], buffer[cursor+3], buffer[cursor+4]
        ]) as usize;

        // GOOD LOGIC: always advances cursor
        cursor += 5 + length;
    }
    println!("Successfully parsed file.");
}
EOF

git add Cargo.toml src/main.rs
git commit -m "Initial commit"

for i in $(seq 1 100); do
    echo "// Comment $i" >> src/main.rs
    git commit -am "Update $i"
done

cat << 'EOF' > src/main.rs
use std::env;
use std::fs::File;
use std::io::Read;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <file>", args[0]);
        std::process::exit(1);
    }

    let mut file = File::open(&args[1]).unwrap();
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer).unwrap();

    let mut cursor = 0;
    while cursor < buffer.len() {
        if cursor + 5 > buffer.len() { break; }
        let record_type = buffer[cursor];
        let length = u32::from_be_bytes([
            buffer[cursor+1], buffer[cursor+2], buffer[cursor+3], buffer[cursor+4]
        ]) as usize;

        // BUG INTRODUCED HERE: type 0x99 causes infinite loop without advancing cursor
        if record_type == 0x99 {
            continue;
        }

        cursor += 5 + length;
    }
    println!("Successfully parsed file.");
}
EOF
git commit -am "Refactor parsing logic to handle deprecated types"
BAD_COMMIT=$(git rev-parse HEAD)

for i in $(seq 101 199); do
    echo "// Post bug comment $i" >> src/main.rs
    git commit -am "Update $i"
done

echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

for i in $(seq 1 49); do
    printf "\x01\x00\x00\x00\x04\xAA\xBB\xCC\xDD" > /home/user/samples/sample_$i.bin
done

printf "\x01\x00\x00\x00\x04\xAA\xBB\xCC\xDD\x99\x00\x00\x00\x02\xFF\xFF\x02\x00\x00\x00\x01\x00" > /home/user/samples/sample_50.bin

printf "\x99\x00\x00\x00\x02\xFF\xFF" > /tmp/expected_minimal.bin

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user