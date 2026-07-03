apt-get update && apt-get install -y python3 python3-pip curl build-essential cargo rustc
    pip3 install pytest flask requests

    mkdir -p /home/user/app/retrieval_system/src/bin

    cat << 'EOF' > /home/user/app/retrieval_system/Cargo.toml
[package]
name = "retrieval_system"
version = "0.1.0"
edition = "2021"

[dependencies]
reqwest = { version = "0.11", features = ["json", "blocking"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
warp = "0.3"
tokio = { version = "1", features = ["full"] }
EOF

    cat << 'EOF' > /home/user/app/retrieval_system/src/bin/etl.rs
fn main() {
    // Bugged ETL pipeline with data leakage
    println!("Running ETL pipeline...");
    // Mock output
    println!("Tuned threshold: 0.85");
}
EOF

    cat << 'EOF' > /home/user/app/retrieval_system/src/bin/server.rs
#[tokio::main]
async fn main() {
    // Incomplete server implementation
    println!("Starting server...");
}
EOF

    cat << 'EOF' > /home/user/app/embedding_service.py
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/embed', methods=['POST'])
def embed():
    return jsonify({"embedding": [0.1, 0.2, 0.3]})

if __name__ == '__main__':
    app.run(port=9000)
EOF

    cat << 'EOF' > /home/user/app/data_service.py
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/data', methods=['GET'])
def data():
    return jsonify([{"id": "doc_042", "embedding": [0.1, 0.2, 0.3]}])

if __name__ == '__main__':
    app.run(port=9001)
EOF

    cat << 'EOF' > /home/user/app/start_services.sh
#!/bin/bash
python3 /home/user/app/embedding_service.py > /dev/null 2>&1 &
python3 /home/user/app/data_service.py > /dev/null 2>&1 &
echo "Services started."
EOF
    chmod +x /home/user/app/start_services.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user