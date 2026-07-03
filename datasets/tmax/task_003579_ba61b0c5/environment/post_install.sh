apt-get update && apt-get install -y \
        python3 \
        python3-pip \
        postgresql \
        postgresql-contrib \
        redis-server \
        cargo \
        rustc \
        libpq-dev \
        build-essential

    pip3 install pytest pandas scikit-learn psycopg2-binary redis

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/app/src

    cat << 'EOF' > /home/user/app/Cargo.toml
[package]
name = "app"
version = "0.1.0"
edition = "2021"

[dependencies]
postgres = "0.19"
redis = "0.23"
dotenv = "0.15"
csv = "1.1"
EOF

    cat << 'EOF' > /home/user/app/src/main.rs
fn main() {
    // TODO: IMPLEMENT CORRELATION, COVARIANCE, AND REGRESSION LOGIC
    println!("Hello, world!");
}
EOF

    chmod -R 777 /home/user