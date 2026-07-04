apt-get update && apt-get install -y python3 python3-pip git gawk
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    cd /home/user

    # 1. Create the environment requirement
    echo 'THRESHOLD=100' > /home/user/config.ini

    # 2. Create the dataset
    cat << 'EOF' > /home/user/data.csv
id,amount,status
1,50,active
2,150,active
3,200,inactive
4,120,active
EOF

    # 3. Initialize Git repository
    mkdir -p /home/user/reporting_tool
    cd /home/user/reporting_tool
    git init
    git config user.email 'tech@example.com'
    git config user.name 'IT Tech'

    # Create the analyze script
    cat << 'EOF' > analyze.sh
#!/bin/bash
if [ -z "$REPORT_CONFIG" ]; then
    echo "ERROR: REPORT_CONFIG environment variable is not set."
    exit 255
fi
if [ ! -f "$REPORT_CONFIG" ]; then
    echo "ERROR: Config file not found at $REPORT_CONFIG"
    exit 255
fi

# Calculate sum of active amounts
# GOOD LOGIC:
awk -F',' '$3=="active" {sum+=$2} END {print "Total Active: " sum}' /home/user/data.csv
EOF
    chmod +x analyze.sh

    git add analyze.sh
    git commit -m 'Initial commit: Add analyze script'
    git tag v1.0

    # Commit 2 (Good)
    echo '# comment 1' >> analyze.sh
    git commit -am 'Refactor: Add comments'

    # Commit 3 (Good)
    echo '# comment 2' >> analyze.sh
    git commit -am 'Update documentation'

    # Commit 4 (BAD COMMIT - introduces regression)
    cat << 'EOF' > analyze.sh
#!/bin/bash
if [ -z "$REPORT_CONFIG" ]; then
    echo "ERROR: REPORT_CONFIG environment variable is not set."
    exit 255
fi
if [ ! -f "$REPORT_CONFIG" ]; then
    echo "ERROR: Config file not found at $REPORT_CONFIG"
    exit 255
fi

# Calculate sum of active amounts
# BAD LOGIC: sums all amounts regardless of status
awk -F',' 'NR>1 {sum+=$2} END {print "Total Active: " sum}' /home/user/data.csv
EOF
    chmod +x analyze.sh
    git commit -am 'Feature: Optimize awk processing'
    git rev-parse HEAD > /home/user/.secret_bad_commit

    # Commit 5 (Bad)
    echo '# comment 3' >> analyze.sh
    git commit -am 'Minor tweak to logs'

    # Commit 6 (Bad)
    echo '# comment 4' >> analyze.sh
    git commit -am 'Formatting adjustments'

    chown -R user:user /home/user
    chmod -R 777 /home/user