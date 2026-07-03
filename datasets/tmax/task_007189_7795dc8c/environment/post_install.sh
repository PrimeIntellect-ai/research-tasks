apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    mkdir -p /home/user/data_parser
    cd /home/user/data_parser

    git init
    git config user.email "dev@example.com"
    git config user.name "Dev"

    # Create robust version
    cat << 'EOF' > parser.py
import sys, json

def parse(data):
    res = {}
    for token in data.split('|'):
        if not token: continue
        parts = token.split('=', 1)
        if len(parts) == 2:
            res[parts[0]] = parts[1]
    return res

if __name__=='__main__':
    with open(sys.argv[1], 'r') as f:
        print(json.dumps(parse(f.read().strip())))
EOF

    cat << 'EOF' > input.txt
name=Bob|age=|city=London||extra=true|malformed_token
EOF

    git add parser.py input.txt
    git commit -m "Initial working parser"
    git tag v1.0

    # Create 80 dummy commits
    for i in $(seq 1 80); do
        echo "Dummy change $i" > dummy.txt
        git add dummy.txt
        git commit -m "Dummy commit $i"
    done

    # Introduce the bad commit
    cat << 'EOF' > parser.py
import sys, json

def parse(data):
    res = {}
    for token in data.split('|'):
        # Removed safety checks, causes IndexError or ValueError on edge cases
        parts = token.split('=')
        res[parts[0]] = parts[1]
    return res

if __name__=='__main__':
    with open(sys.argv[1], 'r') as f:
        print(json.dumps(parse(f.read().strip())))
EOF

    git add parser.py
    git commit -m "Refactor parser to be simpler"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Create 120 more dummy commits
    for i in $(seq 81 200); do
        echo "Dummy change $i" > dummy.txt
        git add dummy.txt
        git commit -m "Dummy commit $i"
    done

    # Save the bad commit hash somewhere the verification script can check
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user