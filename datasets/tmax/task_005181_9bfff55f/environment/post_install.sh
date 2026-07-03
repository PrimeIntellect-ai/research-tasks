apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

useradd -m -s /bin/bash user || true

git config --global user.email "test@example.com"
git config --global user.name "Test User"
git config --global init.defaultBranch main

mkdir -p /home/user/perf-repo
cd /home/user/perf-repo
git init

# Commit 1 (Good)
cat << 'EOF' > runner.sh
#!/bin/bash
process_jobs() {
    if [ $# -eq 0 ]; then return 0; fi
    echo "Processing $1"
    shift
    process_jobs "$@"
}
process_jobs "task1" "task2" "task3"
EOF
chmod +x runner.sh
git add runner.sh && git commit -m "Initial commit"

# Commit 2
echo "# dummy 1" >> dummy.txt && git add dummy.txt && git commit -m "Add dummy 1"

# Commit 3
echo "# dummy 2" >> dummy.txt && git add dummy.txt && git commit -m "Add dummy 2"

# Commit 4
echo "# dummy 3" >> dummy.txt && git add dummy.txt && git commit -m "Add dummy 3"

# Commit 5 (Bad)
cat << 'EOF' > runner.sh
#!/bin/bash
process_jobs() {
    if [ $# -eq 0 ]; then return 0; fi
    echo "Processing $1"
    process_jobs "$@"
}
process_jobs "task1" "task2" "task3"
EOF
git add runner.sh && git commit -m "Refactor processing logic"
BAD_COMMIT=$(git rev-parse HEAD)
echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

# Commit 6
echo "# dummy 4" >> dummy.txt && git add dummy.txt && git commit -m "Add dummy 4"

# Commit 7
echo "# dummy 5" >> dummy.txt && git add dummy.txt && git commit -m "Add dummy 5"

chown -R user:user /home/user/perf-repo
chmod 777 /tmp/expected_bad_commit.txt
chmod -R 777 /home/user