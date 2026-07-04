apt-get update && apt-get install -y python3 python3-pip golang g++ ffmpeg curl
    pip3 install pytest websockets

    # Create directories
    mkdir -p /home/user/videoproc/analyzer/models
    mkdir -p /home/user/videoproc/analyzer/graph
    mkdir -p /home/user/videoproc/extractor
    mkdir -p /home/user/videoproc/assets
    mkdir -p /home/user/bin
    mkdir -p /app

    # Create Go files with circular dependency
    cd /home/user/videoproc/analyzer
    go mod init analyzer

    cat << 'EOF' > main.go
package main
import "analyzer/models"
import "analyzer/graph"
func main() {}
EOF

    cat << 'EOF' > models/models.go
package models
import "analyzer/graph"
type Model struct {
    Node graph.Node
}
EOF

    cat << 'EOF' > graph/graph.go
package graph
import "analyzer/models"
type Node struct {
    Model models.Model
}
EOF

    # Create C++ extractor
    cat << 'EOF' > /home/user/videoproc/extractor/main.cpp
#include <iostream>
#include <cstdlib>
int main() {
    std::system("ffmpeg -version");
    return 0;
}
EOF

    # Create assets
    cat << 'EOF' > /home/user/videoproc/assets/dependencies.json
{
    "root": ["child"],
    "child": ["grandchild"]
}
EOF
    touch /home/user/videoproc/assets/root.conf
    touch /home/user/videoproc/assets/child.conf
    touch /home/user/videoproc/assets/grandchild.conf

    # Create dummy video
    touch /app/input.mp4

    # Create ground truth metrics
    python3 -c "import json; json.dump([0.0]*100, open('/tmp/ground_truth_metrics.json', 'w'))"

    # Create user and set permissions
    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user
    chmod -R 777 /app
    chmod 777 /tmp/ground_truth_metrics.json