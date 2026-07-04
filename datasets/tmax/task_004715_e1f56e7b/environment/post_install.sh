apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/report-builder
    cd /home/user/report-builder
    git init
    git config user.name "Auto Bot"
    git config user.email "bot@example.com"

    cat << 'EOF' > build_report.sh
#!/bin/bash
log_file=$1
if [ ! -f "$log_file" ]; then
    echo "File not found"
    exit 1
fi
info_count=$(grep -c "INFO" "$log_file" || true)
error_count=$(grep -c "ERROR" "$log_file" || true)

echo "Report generated: INFO=$info_count, ERROR=$error_count"
exit 0
EOF
    chmod +x build_report.sh

    git add build_report.sh
    git commit -m "Initial commit"
    git tag v1.0

    # Generate commits
    for i in $(seq 1 200); do
        if [ "$i" -eq 137 ]; then
            # Introduce the bug
            cat << 'EOF' > build_report.sh
#!/bin/bash
log_file=$1
if [ ! -f "$log_file" ]; then
    echo "File not found"
    exit 1
fi
info_count=$(grep -c "INFO" "$log_file" || true)
error_count=$(grep -c "ERROR" "$log_file" || true)

# Bug: Fails if ERROR count is more than 3 times the INFO count
if [ "$error_count" -gt $((info_count * 3)) ]; then
    echo "Statistical anomaly detected: Possible build corruption." >&2
    exit 1
fi

echo "Report generated: INFO=$info_count, ERROR=$error_count"
exit 0
EOF
            git commit -am "Update reporting logic with anomaly detection"
            BAD_COMMIT=$(git rev-parse HEAD)
        else
            echo "# Comment line $i" >> build_report.sh
            git commit -am "Add comment $i"
        fi
    done

    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    chown -R user:user /home/user/report-builder
    chmod -R 777 /home/user