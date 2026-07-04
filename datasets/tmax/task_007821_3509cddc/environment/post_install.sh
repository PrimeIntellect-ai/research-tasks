apt-get update && apt-get install -y python3 python3-pip git cargo rustc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Use bash to ensure brace expansion works
    bash -c '
    mkdir -p /home/user/physics_engine
    cd /home/user/physics_engine

    git config --global init.defaultBranch main
    git config --global user.email "developer@example.com"
    git config --global user.name "Developer"

    git init

    cat << "EOF" > Cargo.toml
[package]
name = "physics_engine"
version = "0.1.0"
edition = "2021"
EOF

    mkdir -p src
    cat << "EOF" > src/main.rs
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <time>", args[0]);
        std::process::exit(1);
    }
    let t: f64 = args[1].parse().unwrap();
    let v0 = 100.0;
    let theta: f64 = 0.7853981633974483; // 45 degrees

    // Calculate horizontal distance
    let distance = v0 * theta.cos() * t;
    println!("{:.10}", distance);
}
EOF

    git add .
    git commit -m "Initial commit"
    git tag v1.0

    # Create 143 good commits
    for i in {1..143}; do
        echo "// comment $i" >> src/main.rs
        git commit -am "Routine update $i"
    done

    # Introduce bug at 144
    cat << "EOF" > src/main.rs
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <time>", args[0]);
        std::process::exit(1);
    }
    let t: f64 = args[1].parse().unwrap();
    let v0 = 100.0;
    let theta: f64 = 0.7853981633974483; 

    // Bug: precision loss introduced by casting to f32
    let distance = v0 * (theta as f32).cos() as f64 * t;
    println!("{:.10}", distance);
}
EOF
    git commit -am "Refactor calculation for performance"
    BAD_COMMIT=$(git rev-parse HEAD)
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    # Create remaining bad commits
    for i in {145..200}; do
        echo "// comment $i" >> src/main.rs
        git commit -am "Routine update $i"
    done
    '

    chown -R user:user /home/user/physics_engine
    chmod -R 777 /home/user