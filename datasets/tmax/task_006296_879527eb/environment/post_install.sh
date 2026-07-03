apt-get update && apt-get install -y python3 python3-pip git cargo
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/wal_project
    cd /home/user/wal_project

    git config --global user.email "dev@example.com"
    git config --global user.name "Dev"

    cargo init --bin
    echo "bad corrupted data" > corrupted.wal

    cat << 'EOF' > src/main.rs
fn main() { 
    // good state
    std::process::exit(0); 
}
EOF

    git add .
    git commit -m "Commit 1 (Initial)"

    for i in $(seq 2 149); do
        echo "// commit $i" >> src/main.rs
        git commit -am "Commit $i"
    done

    # Commit 150: The Regression (Panic on corrupted WAL)
    cat << 'EOF' > src/main.rs
fn main() {
    let wal = std::fs::read("corrupted.wal").unwrap_or_default();
    if wal.len() > 0 { 
        panic!("Core dumped during WAL recovery!"); 
    }
}
EOF
    git commit -am "Commit 150 (Regression)"
    BAD_COMMIT_HASH=$(git rev-parse HEAD)

    # Commits 151-159: Bad but compiling
    for i in $(seq 151 159); do
        echo "// commit $i" >> src/main.rs
        git commit -am "Commit $i"
    done

    # Commits 160-165: Compiler Error
    for i in $(seq 160 165); do
        echo "this is not valid rust code {" >> src/main.rs
        git commit -am "Commit $i"
    done

    # Commits 166-200: Bad but compiling again
    for i in $(seq 166 200); do
        cat << EOF > src/main.rs
fn main() {
    let wal = std::fs::read("corrupted.wal").unwrap_or_default();
    if wal.len() > 0 { 
        panic!("Core dumped during WAL recovery!"); 
    }
    // commit $i
}
EOF
        git commit -am "Commit $i"
    done

    mkdir -p /tmp/truth
    echo "$BAD_COMMIT_HASH" > /tmp/truth/expected_commit.txt

    chown -R user:user /home/user/wal_project
    chmod -R 777 /home/user