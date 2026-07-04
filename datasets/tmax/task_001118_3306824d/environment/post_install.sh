apt-get update && apt-get install -y python3 python3-pip curl build-essential systemd dbus cargo rustc
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /app/edge-proxy-1.2.0/src

    cat << 'EOF' > /app/edge-proxy-1.2.0/Cargo.toml
[package]
name = "edge-proxy"
version = "1.2.0"
edition = "2021"

[dependencies]
tokio = { version = "1.18", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
toml = "0.5"
EOF

    cat << 'EOF' > /app/edge-proxy-1.2.0/src/auth.rs
pub fn verify_token(provided: &str, expected: &str) -> bool {
    if provided == expected {
        // BUG: silently rejects correct token (Scenario Anchor)
        false 
    } else {
        false
    }
}
EOF

    cat << 'EOF' > /app/edge-proxy-1.2.0/src/main.rs
use std::env;
use std::fs;
use std::sync::Arc;
use tokio::io::{AsyncBufReadExt, AsyncReadExt, AsyncWriteExt, BufReader};
use tokio::net::TcpListener;
use serde::Serialize;
use toml::Value;

mod auth;

#[derive(Serialize)]
struct HealthResponse {
    status: String,
    timezone: String,
    locale: String,
}

#[tokio::main]
async fn main() {
    let config_path = "../etc/edge-proxy.toml";
    let config_content = fs::read_to_string(config_path).expect("Failed to read config");
    let config: Value = toml::from_str(&config_content).expect("Failed to parse config");

    let http_port = config["server"]["http_port"].as_integer().unwrap() as u16;
    let tcp_port = config["server"]["tcp_port"].as_integer().unwrap() as u16;
    let control_token = config["auth"]["control_token"].as_str().unwrap().to_string();

    let token = Arc::new(control_token);

    let http_addr = format!("127.0.0.1:{}", http_port);
    let tcp_addr = format!("127.0.0.1:{}", tcp_port);

    let http_listener = TcpListener::bind(&http_addr).await.unwrap();
    let tcp_listener = TcpListener::bind(&tcp_addr).await.unwrap();

    let token_clone = token.clone();
    tokio::spawn(async move {
        loop {
            if let Ok((mut socket, _)) = tcp_listener.accept().await {
                let token = token_clone.clone();
                tokio::spawn(async move {
                    let (reader, mut writer) = socket.split();
                    let mut reader = BufReader::new(reader);
                    let mut line = String::new();
                    if reader.read_line(&mut line).await.is_ok() {
                        let parts: Vec<&str> = line.trim().split_whitespace().collect();
                        if parts.len() == 2 && parts[0] == "AUTH" {
                            if auth::verify_token(parts[1], &token) {
                                line.clear();
                                if reader.read_line(&mut line).await.is_ok() {
                                    if line.trim() == "PING" {
                                        let _ = writer.write_all(b"PONG\n").await;
                                    }
                                }
                            }
                        }
                    }
                });
            }
        }
    });

    loop {
        if let Ok((mut socket, _)) = http_listener.accept().await {
            tokio::spawn(async move {
                let mut buf = [0; 1024];
                if socket.read(&mut buf).await.is_ok() {
                    let tz = env::var("TZ").unwrap_or_default();
                    let lang = env::var("LANG").unwrap_or_default();
                    let res = HealthResponse {
                        status: "ok".to_string(),
                        timezone: tz,
                        locale: lang,
                    };
                    let body = serde_json::to_string(&res).unwrap();
                    let response = format!(
                        "HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n{}",
                        body.len(),
                        body
                    );
                    let _ = socket.write_all(response.as_bytes()).await;
                }
            });
        }
    }
}
EOF

    # Pre-fetch crates to speed up agent's cargo build
    cd /app/edge-proxy-1.2.0
    cargo fetch || true

    chown -R user:user /app
    chmod -R 777 /app
    chmod -R 777 /home/user