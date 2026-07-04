apt-get update && apt-get install -y python3 python3-pip cargo
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/service_app/src

    cat << 'EOF' > /home/user/service_app/Cargo.toml
[package]
name = "service_app"
version = "0.1.0"
edition = "2021"

[dependencies]
EOF

    cat << 'EOF' > /home/user/service_app/config.json
{
  "host": "300.0.0.1",
  "port": 9090,
  "log_dir": "/home/user/logs"
}
EOF

    cat << 'EOF' > /home/user/service_app/src/main.rs
use std::fs::OpenOptions;
use std::io::Write;
use std::net::TcpListener;

fn main() {
    let config_content = std::fs::read_to_string("config.json").expect("Failed to read config.json");

    let host = config_content.split("\"host\": \"").nth(1).expect("Parse error").split("\"").next().expect("Parse error");
    let port = config_content.split("\"port\": ").nth(1).expect("Parse error").split(",").next().expect("Parse error").trim().replace("\n", "").replace("\r", "");
    let log_dir = config_content.split("\"log_dir\": \"").nth(1).expect("Parse error").split("\"").next().expect("Parse error");

    let addr = format!("{}:{}", host, port);
    let _listener = TcpListener::bind(&addr).expect("Failed to bind to network interface");

    let log_path = format!("{}/service.log", log_dir);
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(log_path)
        .expect("Failed to open log file (does the directory exist?)");

    writeln!(file, "[INFO] Server started successfully. Token: X9A4B2Z1V").unwrap();
}
EOF

    chmod -R 777 /home/user