apt-get update && apt-get install -y python3 python3-pip gcc libsqlite3-dev
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    # Create /home/user/graph_analyzer.c
    cat << 'EOF' > /home/user/graph_analyzer.c
#include <stdio.h>
#include <sqlite3.h>

int main(int argc, char **argv) {
    // Buggy implementation
    return 0;
}
EOF

    # Create /app/query_pattern.png
    mkdir -p /app
    touch /app/query_pattern.png

    # Create /opt/verifier/reference_graph_analyzer
    mkdir -p /opt/verifier
    cat << 'EOF' > /opt/verifier/reference.c
#include <stdio.h>
int main() {
    return 0;
}
EOF
    gcc /opt/verifier/reference.c -o /opt/verifier/reference_graph_analyzer
    chmod +x /opt/verifier/reference_graph_analyzer

    chmod -R 777 /home/user