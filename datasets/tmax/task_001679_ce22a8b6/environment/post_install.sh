apt-get update && apt-get install -y python3 python3-pip rustc cargo
    pip3 install pytest

    # Create Rust boilerplate
    mkdir -p /home/user/audit_service/src

    cat << 'EOF' > /home/user/audit_service/Cargo.toml
[package]
name = "audit_service"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
sqlx = { version = "0.6", features = ["runtime-tokio-native-tls", "postgres"] }
neo4rs = "0.6"
serde_json = "1.0"
EOF

    cat << 'EOF' > /home/user/audit_service/src/main.rs
fn main() {
    println!("Hello, world!");
}
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user