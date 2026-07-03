apt-get update && apt-get install -y python3 python3-pip git rustc cargo
pip3 install pytest

useradd -m -s /bin/bash user || true

bash -c '
mkdir -p /home/user/log_parser_repo
cd /home/user/log_parser_repo
git init -b main
git config --global user.email "test@example.com"
git config --global user.name "Test User"

cat << "EOF" > Cargo.toml
[package]
name = "log_parser"
version = "0.1.0"
edition = "2021"
EOF

mkdir -p src

cat << "EOF" > test.log
INFO: system started
WARN: high memory usage
ERROR: disk full
INFO: user logged in
WARN: connection timeout
ERROR: permission denied
EOF
for i in $(seq 1 1000); do
  echo "INFO: line $i" >> test.log
done

git add Cargo.toml test.log
git commit -m "Initial commit with data"

# Generate 99 good commits
for i in $(seq 1 99); do
  cat << "EOF" > src/main.rs
use std::sync::{Arc, Mutex};
use std::thread;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("test.log").unwrap();
    let reader = BufReader::new(file);
    let lines: Vec<String> = reader.lines().map(|l| l.unwrap()).collect();
    let counts = Arc::new(Mutex::new(std::collections::HashMap::new()));
    let chunks: Vec<Vec<String>> = lines.chunks(255).map(|c| c.to_vec()).collect();
    let mut handles = vec![];
    for chunk in chunks {
        let counts_clone = Arc::clone(&counts);
        let handle = thread::spawn(move || {
            for line in chunk {
                let parts: Vec<&str> = line.splitn(2, '\'':'\'').collect();
                if parts.len() == 2 {
                    let level = parts[0].to_string();
                    let mut c = counts_clone.lock().unwrap();
                    *c.entry(level).or_insert(0) += 1;
                }
            }
        });
        handles.push(handle);
    }
    for handle in handles { handle.join().unwrap(); }
    let total: i32 = counts.lock().unwrap().values().sum();
    assert_eq!(total, 1006, "Total log entries parsed incorrectly! Race condition detected.");
}
EOF
  # Fix the single quote issue in the heredoc above by replacing it with a normal single quote
  sed -i "s/':'/':'/g" src/main.rs
  echo "// Commit $i" >> src/main.rs
  git add src/main.rs
  git commit -m "Update $i"
done

# Generate the bad commit (100) introducing the race condition
cat << "EOF" > src/main.rs
use std::sync::{Arc, Mutex};
use std::thread;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("test.log").unwrap();
    let reader = BufReader::new(file);
    let lines: Vec<String> = reader.lines().map(|l| l.unwrap()).collect();
    let counts = Arc::new(Mutex::new(std::collections::HashMap::new()));
    let chunks: Vec<Vec<String>> = lines.chunks(255).map(|c| c.to_vec()).collect();
    let mut handles = vec![];
    for chunk in chunks {
        let counts_clone = Arc::clone(&counts);
        let handle = thread::spawn(move || {
            for line in chunk {
                let parts: Vec<&str> = line.splitn(2, '\'':'\'').collect();
                if parts.len() == 2 {
                    let level = parts[0].to_string();
                    let count = *counts_clone.lock().unwrap().get(&level).unwrap_or(&0);
                    // Context switch vulnerability
                    counts_clone.lock().unwrap().insert(level, count + 1);
                }
            }
        });
        handles.push(handle);
    }
    for handle in handles { handle.join().unwrap(); }
    let total: i32 = counts.lock().unwrap().values().sum();
    assert_eq!(total, 1006, "Total log entries parsed incorrectly! Race condition detected.");
}
// Commit 100 (regression)
EOF
sed -i "s/':'/':'/g" src/main.rs
git add src/main.rs
git commit -m "Update 100"

# Save the hash for verification
git rev-parse HEAD > /tmp/expected_bad_commit.txt

# Generate the remaining commits
for i in $(seq 101 200); do
  echo "// Commit $i" >> src/main.rs
  git add src/main.rs
  git commit -m "Update $i"
done
'

chown -R user:user /home/user/log_parser_repo
chmod -R 777 /home/user