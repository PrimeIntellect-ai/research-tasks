apt-get update && apt-get install -y python3 python3-pip cargo nginx curl netcat-openbsd
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/app
mkdir -p /home/user/proxy/src

cat << 'EOF' > /home/user/app/nginx.conf
worker_processes 1;
events { worker_connections 1024; }
http {
    server {
        listen 8080;
        location /process {
            proxy_pass http://127.0.0.1:8081;
        }
    }
}
EOF

cat << 'EOF' > /home/user/app/reload_nginx.sh
#!/bin/bash
nginx -s reload -c /home/user/app/nginx.conf
EOF
chmod +x /home/user/app/reload_nginx.sh

cat << 'EOF' > /home/user/proxy/Cargo.toml
[package]
name = "proxy"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = "0.6"
tokio = { version = "1", features = ["full"] }
reqwest = "0.11"
EOF

cat << 'EOF' > /home/user/proxy/src/main.rs
#[tokio::main]
async fn main() {
    println!("Hello, world!");
}
EOF

chmod -R 777 /home/user