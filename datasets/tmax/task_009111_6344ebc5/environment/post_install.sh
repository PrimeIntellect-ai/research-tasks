apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

# Setup Data
mkdir -p /home/user/data_dir
echo 10 > "/home/user/data_dir/file1.txt"
echo 20 > "/home/user/data_dir/file 2.txt"
echo 30 > "/home/user/data_dir/file_3.txt"
echo 40 > "/home/user/data_dir/file 4.txt"
echo 50 > "/home/user/data_dir/file5.txt"

# Setup Git Repo
mkdir -p /home/user/math_processor
cd /home/user/math_processor
git init
git config user.name "Dev"
git config user.email "dev@example.com"

# Commit 1 (v1.0) - Working version
cat << 'EOF' > aggregate.sh
#!/bin/bash
total=0
for f in /home/user/data_dir/*; do
    val=$(cat "$f")
    total=$((total + val))
done
echo $total
EOF
chmod +x aggregate.sh
git add aggregate.sh
GIT_COMMITTER_DATE="2023-01-01T12:00:00" git commit --date="2023-01-01T12:00:00" -m "Initial commit"
git tag v1.0

# Commit 2 - Introduces race condition (First bad commit)
cat << 'EOF' > aggregate.sh
#!/bin/bash
echo 0 > total.txt
for f in /home/user/data_dir/*; do
    (
        val=$(cat "$f")
        cur=$(cat total.txt)
        echo $((cur + val)) > total.txt
    ) &
done
wait
cat total.txt
EOF
git add aggregate.sh
GIT_COMMITTER_DATE="2023-01-02T12:00:00" git commit --date="2023-01-02T12:00:00" -m "Optimize with background jobs"
FIRST_BAD_COMMIT=$(git rev-parse HEAD)

# Commit 3 - Introduces spaces-in-filenames bug
cat << 'EOF' > aggregate.sh
#!/bin/bash
echo 0 > total.txt
for f in $(ls /home/user/data_dir/); do
    (
        val=$(cat "/home/user/data_dir/$f")
        cur=$(cat total.txt)
        echo $((cur + val)) > total.txt
    ) &
done
wait
cat total.txt
EOF
git add aggregate.sh
GIT_COMMITTER_DATE="2023-01-03T12:00:00" git commit --date="2023-01-03T12:00:00" -m "Refactor file loop"

# Save expected outputs for validation securely
echo $FIRST_BAD_COMMIT > /tmp/expected_bad_commit.txt

# Create user and set permissions
useradd -m -s /bin/bash user || true
chmod -R 777 /home/user