apt-get update && apt-get install -y python3 python3-pip git build-essential redis-server libhiredis-dev
    pip3 install pytest redis

    useradd -m -s /bin/bash user || true

    # Create timeline_analyzer repo
    mkdir -p /home/user/timeline_analyzer
    cd /home/user/timeline_analyzer
    git init
    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    cat << 'EOF' > analyzer.c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    printf("Analyzer\n");
    return 0;
}
EOF

    cat << 'EOF' > Makefile
analyzer: analyzer.c
	gcc -o analyzer analyzer.c -lhiredis
EOF

    git add analyzer.c Makefile
    git commit -m "Initial commit"

    # Create 200 commits to simulate history
    for i in {1..200}; do
        echo "// comment $i" >> analyzer.c
        git commit -am "Commit $i"
    done

    # Create env dir
    mkdir -p /home/user/env

    cat << 'EOF' > /home/user/env/startup.sh
#!/bin/bash
redis-server --daemonize yes
python3 /home/user/env/ingestor.py &
EOF
    chmod +x /home/user/env/startup.sh

    cat << 'EOF' > /home/user/env/ingestor.py
import redis
import time

r = redis.Redis(host='127.0.0.1', port=6379)
while True:
    time.sleep(1)
EOF

    chmod -R 777 /home/user