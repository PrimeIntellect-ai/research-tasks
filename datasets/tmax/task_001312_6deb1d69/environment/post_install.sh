apt-get update && apt-get install -y python3 python3-pip cargo curl strace tcpdump
    pip3 install pytest

    mkdir -p /app/pipeline/config
    mkdir -p /app/pipeline/output
    mkdir -p /app/math-analyzer/src/bin
    mkdir -p /app/corpora/clean
    mkdir -p /app/corpora/evil

    # Pipeline Scripts
    cat << 'EOF' > /app/pipeline/start.sh
#!/bin/bash
echo "Starting pipeline..."
EOF
    chmod +x /app/pipeline/start.sh

    # Pipeline Configs
    touch /app/pipeline/config/streamer.env
    touch /app/pipeline/config/analyzer.toml
    touch /app/pipeline/config/sink.env

    # Math Analyzer Codebase
    cat << 'EOF' > /app/math-analyzer/Cargo.toml
[package]
name = "math-analyzer"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    touch /app/math-analyzer/src/main.rs
    touch /app/math-analyzer/src/bin/filter_cli.rs

    # Corpora
    for i in {1..50}; do
        touch /app/corpora/clean/clean_$i.log
        touch /app/corpora/evil/evil_$i.log
    done

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app