apt-get update && apt-get install -y python3 python3-pip git strace coreutils
pip3 install pytest

# Create data dir and input file (> 64KB to cause pipe deadlock)
mkdir -p /home/user/data
head -c 100000 /dev/urandom | base64 > /home/user/data/input.txt

# Setup git repo
mkdir -p /home/user/repo
cd /home/user/repo
git init
git config user.email "dev@example.com"
git config user.name "Dev"

# Good commit version (uses subprocess.run, handles pipes correctly)
cat << 'EOF' > process.py
import sys
import subprocess

def process_data(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    # Process
    result = subprocess.run(['tr', 'a', 'A'], input=data, capture_output=True)
    sys.stdout.buffer.write(result.stdout)

if __name__ == '__main__':
    process_data(sys.argv[1])
EOF

git add process.py
git commit -m "Initial commit"
git tag v1.0

# 24 good commits
for i in {1..24}; do
    echo "# comment $i" >> process.py
    git commit -am "Commit $i"
done

# Bad commit 25: Introduces pipe deadlock
cat << 'EOF' > process.py
import sys
import subprocess

def process_data(file_path):
    with open(file_path, 'rb') as f:
        data = f.read()

    # Process
    p = subprocess.Popen(['tr', 'a', 'A'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    p.wait()
    sys.stdout.buffer.write(p.stdout.read())

if __name__ == '__main__':
    process_data(sys.argv[1])
EOF
echo "# comment 25" >> process.py
git commit -am "Commit 25"
BAD_COMMIT=$(git rev-parse HEAD)
echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

# 25 more commits
for i in {26..50}; do
    echo "# comment $i" >> process.py
    git commit -am "Commit $i"
done
git tag v2.0

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user