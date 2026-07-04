apt-get update && apt-get install -y python3 python3-pip git curl build-essential
    pip3 install pytest

    # Install Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    export PATH="/root/.cargo/bin:${PATH}"

    # Create audio fixture
    mkdir -p /app
    echo "dummy audio data" > /app/telemetry_signal.wav

    # Create git repository
    mkdir -p /home/user/acoustic-node
    cd /home/user/acoustic-node
    git init
    git config --global user.email "dev@example.com"
    git config --global user.name "Dev"

    # Initialize Cargo project
    cargo init .
    git add .
    git commit -m "Initial commit"
    git tag v1.0.0

    # Create commits
    for i in $(seq 1 50); do
        echo "// commit $i" >> src/main.rs
        git commit -am "chore: minor update $i"
    done

    # Introduce the bad commit
    echo "// unsafe concurrent modification here" >> src/main.rs
    git commit -am "refactor: optimize concurrent chunk aggregation"

    # Create more commits
    for i in $(seq 51 100); do
        echo "// commit $i" >> src/main.rs
        git commit -am "chore: minor update $i"
    done

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user
    chmod -R 777 /app