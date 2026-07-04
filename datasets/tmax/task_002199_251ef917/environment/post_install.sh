apt-get update && apt-get install -y python3 python3-pip git redis-server golang-go
    pip3 install pytest

    mkdir -p /app/repo/worker

    # Create the Go oracle processor
    cat << 'EOF' > /tmp/oracle.go
package main
import (
    "crypto/sha256"
    "fmt"
    "os"
)
func main() {
    if len(os.Args) < 2 { return }
    data := []byte(os.Args[1])
    h := sha256.Sum256(data)
    fmt.Printf("LOG_ENTRY_%x_%x\n", h, data)
}
EOF
    go build -o /tmp/oracle_processor /tmp/oracle.go

    # Also put a copy in /opt/verifier/ as requested
    mkdir -p /opt/verifier
    cp /tmp/oracle_processor /opt/verifier/oracle_processor

    # Setup git repo
    cd /app/repo
    git init
    git config user.email "eng@example.com"
    git config user.name "Eng"

    echo "init" > README.md
    git add README.md
    git commit -m "Initial commit"

    cp /tmp/oracle_processor ./worker/format_name
    git add worker/format_name
    git commit -m "Add compiled Go helper binary"

    echo "update" >> README.md
    git add README.md
    git commit -m "Update README"

    rm ./worker/format_name
    cat << 'EOF' > ./worker/format_name.sh
#!/bin/bash
echo "LOG_ENTRY_$(echo -n $1 | sha256sum | awk '{print $1}')_$(echo -n $1 | xxd -p)"
EOF
    chmod +x ./worker/format_name.sh
    git rm worker/format_name
    git add worker/format_name.sh
    git commit -m "Replace binary with bash script"

    # Setup receiver.py
    cat << 'EOF' > /app/receiver.py
from http.server import BaseHTTPRequestHandler, HTTPServer
class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
HTTPServer(('127.0.0.1', 8080), Handler).serve_forever()
EOF

    # Start services on shell startup
    echo "redis-server --daemonize yes > /dev/null 2>&1 || true" >> /etc/bash.bashrc
    echo "pgrep -f receiver.py > /dev/null || nohup python3 /app/receiver.py > /dev/null 2>&1 &" >> /etc/bash.bashrc

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user
    chmod -R 777 /app