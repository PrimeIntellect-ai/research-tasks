apt-get update && apt-get install -y python3 python3-pip git strace
    pip3 install pytest

    mkdir -p /home/user/repo
    cd /home/user/repo
    git init
    git config user.email "test@example.com"
    git config user.name "Test User"

    cat << 'EOF' > log.txt
INFO: Everything is fine
ERROR: "Bug1"
WARN: Low disk space
ERROR: "Bug2"
EOF

    cat << 'EOF' > build.sh
#!/bin/bash
echo "Building..."
grep "ERROR" log.txt | cut -d: -f2 > temp.txt
sed -i 's/"//g' temp.txt
cat temp.txt > output.txt
EOF
    chmod +x build.sh

    git add log.txt build.sh
    git commit -m "Initial commit"

    # 4 good commits
    for i in 1 2 3 4; do
        echo "# Comment $i" >> build.sh
        git commit -am "Add comment $i"
    done

    # The bad commit
    cat << 'EOF' > build.sh
#!/bin/bash
echo "Building..."
grep "ERROR" log.txt | cut -d: -f2 > temp.txt
# Clean up quotes for format parsing
sed 's/"//g' > temp.txt
cat temp.txt > output.txt
# Comment 1
# Comment 2
# Comment 3
# Comment 4
EOF
    chmod +x build.sh
    git commit -am "Optimize format parsing"
    BAD_COMMIT=$(git rev-parse HEAD)

    # 3 more commits
    for i in 5 6 7; do
        echo "# Comment $i" >> build.sh
        git commit -am "Add comment $i"
    done

    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user