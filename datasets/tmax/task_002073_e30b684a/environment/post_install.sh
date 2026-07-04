apt-get update && apt-get install -y python3 python3-pip curl gcc
    pip3 install pytest

    # Install Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal
    export PATH="/root/.cargo/bin:$PATH"

    mkdir -p /app/vendored/log-processor-1.0.0
    cd /app/vendored/log-processor-1.0.0

    cat << 'EOF' > Cargo.toml
[workspace]
members = ["cli", "semver_parser", "text_encoder"]
EOF

    mkdir -p cli/src semver_parser/src text_encoder/src

    cat << 'EOF' > cli/Cargo.toml
[package]
name = "cli"
version = "0.1.0"
edition = "2021"

[dependencies]
semver_parser = { path = "../semver_parser" }
text_encoder = { path = "../text_encoder" }
EOF

    cat << 'EOF' > cli/src/main.rs
fn main() {
    println!("Hello, world!");
}
EOF

    cat << 'EOF' > semver_parser/Cargo.toml
[package]
name = "semver_parser"
version = "0.1.0"
edition = "2021"

[dependencies]
text_encoder = { path = "../text_encoder" }
EOF

    cat << 'EOF' > semver_parser/src/lib.rs
pub use text_encoder::Error;
pub struct Semver;
EOF

    cat << 'EOF' > text_encoder/Cargo.toml
[package]
name = "text_encoder"
version = "0.1.0"
edition = "2021"

[dependencies]
semver_parser = { path = "../semver_parser" }
EOF

    cat << 'EOF' > text_encoder/src/lib.rs
pub use semver_parser::Semver;
pub struct Error;
EOF

    # Oracle
    cat << 'EOF' > /app/oracle.py
import sys
import re
from functools import cmp_to_key

def rle(s):
    if not s: return ""
    res = []
    count = 1
    prev = s[0]
    for c in s[1:]:
        if c == prev:
            count += 1
        else:
            res.append(f"{prev}{count}")
            prev = c
            count = 1
    res.append(f"{prev}{count}")
    return "".join(res)

def parse_semver(s):
    m = re.match(r'^(\d+)\.(\d+)\.(\d+)$', s)
    if m:
        return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None

def cmp(a, b):
    for i in range(3):
        if a[0][i] != b[0][i]:
            return b[0][i] - a[0][i]
    if a[1] != b[1]:
        return -1 if a[1] < b[1] else 1
    return 0

lines = []
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    parts = line.split(' ', 1)
    if len(parts) != 2: continue
    sv, text = parts
    parsed = parse_semver(sv)
    if parsed:
        encoded = rle(text)
        lines.append((parsed, encoded, sv))

lines.sort(key=cmp_to_key(cmp))

for item in lines:
    print(f"{item[1]}\t{item[2]}")
EOF

    cat << 'EOF' > /app/oracle.c
#include <stdlib.h>
int main() {
    return system("python3 /app/oracle.py");
}
EOF
    gcc -o /app/oracle /app/oracle.c
    rm /app/oracle.c

    useradd -m -s /bin/bash user || true
    mkdir -p /home/user/repo/.github/workflows
    mkdir -p /home/user/bin
    chown -R user:user /home/user
    chmod -R 777 /home/user