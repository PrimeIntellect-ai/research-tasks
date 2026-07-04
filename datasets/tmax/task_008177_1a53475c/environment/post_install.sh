apt-get update && apt-get install -y python3 python3-pip git make curl lsof
    pip3 install pytest

    mkdir -p /home/user/regression_repo
    cd /home/user/regression_repo
    git init
    git config user.email "dev@example.com"
    git config user.name "Dev"

    # Good state
    cat << 'EOF' > server.sh
#!/bin/bash
python3 -m http.server 8080 &
echo $! > server.pid
EOF
    chmod +x server.sh

    cat << 'EOF' > Makefile
test:
	./server.sh
	sleep 1
	curl -s http://localhost:8080 > /dev/null
	kill `cat server.pid`
	rm server.pid
EOF

    git add server.sh Makefile
    git commit -m "Initial commit"
    git tag v1.0

    # Add 20 good commits
    for i in {1..20}; do
        echo "# Good update $i" >> server.sh
        git commit -am "Update server $i"
    done

    # Introduce the bug at commit 21
    cat << 'EOF' > Makefile
test:
	./server.sh
	sleep 1
	curl -s http://localhost:8080 > /dev/null
	# BUG: referencing wrong pid file name, process leaks
	kill `cat wrong_server.pid 2>/dev/null` || true
	rm -f server.pid wrong_server.pid
EOF
    git commit -am "Refactor Makefile cleanup"
    BAD_COMMIT=$(git rev-parse HEAD)
    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    # Add 20 more bad commits
    for i in {21..40}; do
        echo "# Bad update $i" >> server.sh
        git commit -am "Update server $i"
    done

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user/regression_repo
    chmod -R 777 /home/user