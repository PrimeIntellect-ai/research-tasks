apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    git config --global user.email "test@example.com"
    git config --global user.name "Test User"

    mkdir -p /home/user/app
    cd /home/user/app
    git init

    cat << 'EOF' > daemon.sh
#!/bin/bash
ITEMS=()
process_data() {
    for i in $(seq 1 100); do
        ITEMS+=("data_$i")
        if [ "${#ITEMS[@]}" -ge 10 ]; then
            ITEMS=()
        fi
    done
}
EOF
    chmod +x daemon.sh
    git add daemon.sh
    git commit -m "Initial commit with working daemon"

    # Create some good commits
    for i in $(seq 1 5); do
        echo "# comment $i" >> daemon.sh
        git commit -am "Safe change $i"
    done

    # Introduce the bug
    sed -i 's/-ge 10/-eq -1/g' daemon.sh
    git commit -am "Refactor cleanup logic"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Create some more commits after the bug
    for i in $(seq 6 10); do
        echo "# comment $i" >> daemon.sh
        git commit -am "Safe change $i"
    done

    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user