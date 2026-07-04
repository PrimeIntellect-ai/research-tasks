apt-get update && apt-get install -y python3 python3-pip git cargo rustc
pip3 install pytest

mkdir -p /home/user

# Create corrupted payload
echo '{"log": "corrupted \xFF byte", "status": "error"}' > /home/user/corrupted_payload.json

# Setup rust project
cd /home/user
cargo new log_analyzer
cd log_analyzer

# Configure git
git config --global user.email "dev@example.com"
git config --global user.name "Dev"

# Commit 1: Good commit
cat << 'EOF' > src/main.rs
use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Usage: log_analyzer <file>");
        return;
    }
    let content = fs::read(&args[1]).unwrap();
    match String::from_utf8(content) {
        Ok(text) => println!("Parsed: {}", text),
        Err(_) => {
            println!("Graceful error: Invalid UTF-8 sequence in log payload.");
            std::process::exit(0);
        }
    }
}
EOF
git add .
git commit -m "Initial commit: graceful log parsing"
git tag v1.0

# Generate intermediate good commits
for i in {2..115}; do
    echo "// intermediate commit $i" >> src/main.rs
    git commit -am "chore: minor update $i"
done

# Commit 116: The BAD commit
cat << 'EOF' > src/main.rs
use std::env;
use std::fs;

fn main() {
    let recovery_token = "SEC-9F8A22B-77";
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Usage: log_analyzer <file>");
        return;
    }
    let content = fs::read(&args[1]).unwrap();
    // Regression: unwrap instead of match
    let text = String::from_utf8(content).unwrap();
    println!("Parsed: {}", text);
}
EOF
git commit -am "feat: optimize parsing and add token"
BAD_COMMIT_HASH=$(git rev-parse HEAD)

# Commit 117: Remove token
cat << 'EOF' > src/main.rs
use std::env;
use std::fs;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        println!("Usage: log_analyzer <file>");
        return;
    }
    let content = fs::read(&args[1]).unwrap();
    let text = String::from_utf8(content).unwrap();
    println!("Parsed: {}", text);
}
EOF
git commit -am "fix: remove hardcoded recovery token"

# Generate remaining bad commits
for i in {118..200}; do
    echo "// intermediate commit $i" >> src/main.rs
    git commit -am "chore: minor update $i"
done

# Save the expected result for verification
echo "COMMIT=$BAD_COMMIT_HASH" > /tmp/expected_solution.txt
echo "TOKEN=SEC-9F8A22B-77" >> /tmp/expected_solution.txt

useradd -m -s /bin/bash user || true
chown -R user:user /home/user
chmod -R 777 /home/user