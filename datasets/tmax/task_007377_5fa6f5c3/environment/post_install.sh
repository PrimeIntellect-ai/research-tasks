apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

useradd -m -s /bin/bash user || true

cat << 'EOF_SETUP' > /tmp/setup.sh
#!/bin/bash
mkdir -p /home/user/sysmon
mkdir -p /home/user/logs

# Create log files
cat << 'EOF' > /home/user/logs/good.log
INFO Starting system
WARN High disk usage
INFO System healthy
EOF

# Create yesterday.log with 1000 lines. Line 742 will be the poison line.
> /home/user/logs/yesterday.log
for i in $(seq 1 741); do echo "INFO Normal operation log $i" >> /home/user/logs/yesterday.log; done
echo "CRITICAL OOM_KILLED: nginx - Worker process exhausted memory" >> /home/user/logs/yesterday.log
for i in $(seq 743 1000); do echo "INFO Normal operation log $i" >> /home/user/logs/yesterday.log; done

cd /home/user/sysmon
git config --global user.email "test@example.com"
git config --global user.name "Test User"
git init

# Base commit
cat << 'EOF' > monitor.sh
#!/bin/bash
declare -a alerts
while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" == *"CRITICAL"* ]]; then
        alerts+=("CRITICAL_EVENT")
    fi
done < "$1"
echo "Processed logs. Alerts found: ${#alerts[@]}"
EOF
chmod +x monitor.sh
git add monitor.sh
git commit -m "Initial commit"
git tag v1.0

# Add a few good commits
for i in $(seq 1 3); do
    echo "# comment $i" >> monitor.sh
    git commit -am "Minor update $i"
done

# BAD COMMIT: Introduces infinite loop logic on "OOM_KILLED"
cat << 'EOF' > monitor.sh
#!/bin/bash
declare -a alerts
while IFS= read -r line || [[ -n "$line" ]]; do
    if [[ "$line" == *"CRITICAL"* ]]; then
        if [[ "$line" == *"OOM_KILLED"* ]]; then
            temp="$line"
            while [[ "$temp" == *"OOM_KILLED"* ]]; do
                proc="${temp#*OOM_KILLED: }"
                proc="${proc%% -*}"
                alerts+=("$proc")
                # BUG: Missing state progression! Should be: temp="${temp#*OOM_KILLED: $proc}"
            done
        else
            alerts+=("CRITICAL_EVENT")
        fi
    fi
done < "$1"
echo "Processed logs. Alerts found: ${#alerts[@]}"
EOF
chmod +x monitor.sh
git commit -am "Add specific tracking for OOM_KILLED events"
BAD_COMMIT_HASH=$(git rev-parse HEAD)

# Add a few more commits
for i in $(seq 4 6); do
    echo "# further feature $i" >> monitor.sh
    git commit -am "Feature update $i"
done

# Save the bad commit hash to a hidden file for the testing framework
echo "$BAD_COMMIT_HASH" > /tmp/expected_bad_commit.txt
EOF_SETUP

bash /tmp/setup.sh

chmod -R 777 /home/user