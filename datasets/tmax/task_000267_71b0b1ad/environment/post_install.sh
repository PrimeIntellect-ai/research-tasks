apt-get update && apt-get install -y python3 python3-pip git netcat-openbsd
    pip3 install pytest

    mkdir -p /app/bash-httpd-repo
    cd /app/bash-httpd-repo
    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"

    # Create the base server script
    cat << 'EOF' > server.sh
#!/bin/bash
PORT=$1
if [ -z "$PORT" ]; then PORT=8080; fi

coproc SERVER_PROC { nc -l -p $PORT -k; }

while read -u ${SERVER_PROC[0]} -r line; do
    line=$(echo "$line" | tr -d '\r')
    if [ -z "$line" ]; then
        # End of headers, send response
        echo -ne "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK" >&${SERVER_PROC[1]}
        break
    fi
done
EOF
    chmod +x server.sh
    git add server.sh
    git commit -m "Initial commit"

    # Create 140 good commits
    for i in $(seq 1 140); do
        echo "# Commmit $i" >> README.md
        git add README.md
        git commit -m "Doc update $i"
    done

    # Commit 142 (Buggy commit)
    cat << 'EOF' > server.sh
#!/bin/bash
PORT=$1
if [ -z "$PORT" ]; then PORT=8080; fi

rm -f /tmp/http_pipe
mkfifo /tmp/http_pipe

while true; do
    nc -l -p $PORT < /tmp/http_pipe | while read -r line; do
        line=$(echo "$line" | tr -d '\r')
        if [ "$line" = "X-Debug-Trace: true" ]; then
            # Convergence failure: infinite loop introduced here
            debug_loops=5
            while [ $debug_loops -gt 0 ]; do
                # Bug: debug_loops is never decremented
                if [ 1 -eq 0 ]; then debug_loops=$((debug_loops - 1)); fi
            done
        fi

        if [ -z "$line" ]; then
            echo -ne "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK" > /tmp/http_pipe
            break
        fi
    done
done
EOF
    git add server.sh
    git commit -m "Add debug trace support"
    BUGGY_COMMIT=$(git rev-parse HEAD)

    # Create 58 more commits
    for i in $(seq 142 199); do
        echo "# Commmit $i" >> README.md
        git add README.md
        git commit -m "Doc update $i"
    done

    # Save the expected buggy commit hash for the verifier
    echo "$BUGGY_COMMIT" > /app/.expected_buggy_commit

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user /app