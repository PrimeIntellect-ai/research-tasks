apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    mkdir -p /home/user/log_aggregator/logs
    mkdir -p /home/user/actual_logs

    cd /home/user/log_aggregator
    git init

    # Commit 1 (v1.0 - Good)
    cat << 'EOF' > aggregate_logs.sh
#!/bin/bash
INPUT_DIR=$1
OUTPUT_FILE=$2

total_errors=0
for f in "$INPUT_DIR"/*.log; do
    errors=$(grep -c "ERROR" "$f" || true)
    total_errors=$((total_errors + errors))
done

echo "Total Errors: $total_errors" > "$OUTPUT_FILE"
EOF
    chmod +x aggregate_logs.sh

    cat << 'EOF' > test.sh
#!/bin/bash
./aggregate_logs.sh test_logs output.txt
result=$(cat output.txt)
if [[ "$result" == "Total Errors: 7" ]]; then
    exit 0
else
    exit 1
fi
EOF
    chmod +x test.sh

    mkdir test_logs
    echo "ERROR 1" > test_logs/1.log
    echo "INFO 1" >> test_logs/1.log
    echo "ERROR 2" > test_logs/2.log
    echo "ERROR 3" >> test_logs/2.log
    echo -e "ERROR 4\nERROR 5\nERROR 6\nERROR 7" > test_logs/3.log

    git add .
    git config user.email "support@example.com"
    git config user.name "Support Engineer"
    git commit -m "Initial commit"
    git tag v1.0

    # Commit 2
    echo "# Refactoring to improve performance" >> aggregate_logs.sh
    git commit -am "Refactoring"

    # Commit 3
    echo "# Added support for parallel processing (WIP)" >> aggregate_logs.sh
    git commit -am "Another change"

    # Commit 4 (The Bad Commit)
    cat << 'EOF' > aggregate_logs.sh
#!/bin/bash
INPUT_DIR=$1
OUTPUT_FILE=$2

total_errors=0
for f in "$INPUT_DIR"/*.log; do
    errors=$(grep -c "ERROR" "$f" || true)
    total_errors="$total_errors + $errors"
done

# Added support for parallel processing (WIP)
echo "Total Errors: $total_errors" > "$OUTPUT_FILE"
EOF
    git commit -am "Update aggregation logic to support string concatenation"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Commit 5 (v2.0 - Bad)
    echo "# Documentation updated" >> aggregate_logs.sh
    git commit -am "Docs"
    git tag v2.0

    # Set up actual logs to be processed
    for i in $(seq 1 10); do
        for j in $(seq 1 5); do
            echo "ERROR processing job $j in region $i" >> /home/user/actual_logs/log_$i.log
        done
    done

    # Save expected bad commit hash for verification
    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user