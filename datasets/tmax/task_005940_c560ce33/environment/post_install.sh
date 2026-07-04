apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

mkdir -p /home/user/log_processor/data
cd /home/user/log_processor

git init
git config user.email "engineer@example.com"
git config user.name "Engineer"

# Commit A: Initial good code
cat << 'EOF' > process.py
import sys
import json
import argparse

def parse_log(data_string):
    tokens = []
    i = 0
    while i < len(data_string):
        if data_string[i].isspace():
            i += 1
            continue
        if data_string[i] == '<':
            token = ""
            i += 1
            while i < len(data_string) and data_string[i] != '>':
                if data_string[i] == '*':
                    if i + 1 < len(data_string):
                        token += data_string[i+1] * 2
                        i += 2
                    else:
                        i += 1
                else:
                    token += data_string[i]
                    i += 1
            tokens.append(token)
            if i < len(data_string) and data_string[i] == '>':
                i += 1
        else:
            i += 1
    return tokens

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        data = f.read()

    result = parse_log(data)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f)
    else:
        print(json.dumps(result))
EOF

git add process.py
git commit -m "Initial commit: add log processor"

# Commit B: Add normal test file
cat << 'EOF' > data/normal.txt
<apple> <banana>
EOF
git add data/normal.txt
git commit -m "Add normal test data"

# Commit C: Add edge case test file
cat << 'EOF' > data/edge_case_hang.log
<start *x end> <hello>
EOF
git add data/edge_case_hang.log
git commit -m "Add edge case test data"

# Commit D: Introduce the bug (BAD COMMIT)
cat << 'EOF' > process.py
import sys
import json
import argparse

def parse_log(data_string):
    tokens = []
    i = 0
    while i < len(data_string):
        if data_string[i].isspace():
            i += 1
            continue
        if data_string[i] == '<':
            token = ""
            i += 1
            while i < len(data_string) and data_string[i] != '>':
                if data_string[i] == '*':
                    if i + 1 < len(data_string):
                        token += data_string[i+1] * 2
                        # BUG: Forgot to increment i by 2 here. Causes infinite loop and memory leak on token append
                    else:
                        i += 1
                else:
                    token += data_string[i]
                    i += 1
            tokens.append(token)
            if i < len(data_string) and data_string[i] == '>':
                i += 1
        else:
            i += 1
    return tokens

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("-o", "--output")
    args = parser.parse_args()

    with open(args.input, 'r') as f:
        data = f.read()

    result = parse_log(data)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f)
    else:
        print(json.dumps(result))
EOF
git add process.py
git commit -m "Optimize token extraction"
BAD_COMMIT=$(git rev-parse HEAD)

# Commit E: Delete the edge case file
git rm data/edge_case_hang.log
git commit -m "Remove problematic data causing CI hang"

# Commit F: Unrelated change
echo "# End of file" >> process.py
git add process.py
git commit -m "Add EOF comment"

# Save the expected ground truth to a privileged location
mkdir -p /tmp/truth
echo "$BAD_COMMIT" > /tmp/truth/bad_commit.txt

useradd -m -s /bin/bash user || true
chown -R user:user /home/user/log_processor
chmod -R 777 /home/user