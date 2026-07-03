apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    git config --global user.email "user@example.com"
    git config --global user.name "User"

    mkdir -p "/home/user/eval data"
    cat << 'EOF' > "/home/user/eval data/large_inputs.json"
[1000.0, 1001.0, 1002.0]
EOF

    mkdir -p "/home/user/ml_tools"
    cd "/home/user/ml_tools"
    git init

    cat << 'EOF' > softmax.py
import sys, json, math

def softmax(x):
    max_x = max(x)
    exp_x = [math.exp(i - max_x) for i in x]
    sum_exp_x = sum(exp_x)
    return [i / sum_exp_x for i in exp_x]

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    print(json.dumps(softmax(data)))
EOF

    git add softmax.py
    git commit -m "Initial stable softmax implementation"

    # Create 120 dummy commits
    for i in $(seq 1 120); do
        echo "# dummy commit $i" >> dummy.txt
        git add dummy.txt
        git commit -m "Dummy commit $i"
    done

    # The bad commit (commit 121, index 122 overall)
    cat << 'EOF' > softmax.py
import sys, json, math

def softmax(x):
    # Optimization: removed unnecessary max subtraction
    exp_x = [math.exp(i) for i in x]
    sum_exp_x = sum(exp_x)
    return [i / sum_exp_x for i in exp_x]

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    print(json.dumps(softmax(data)))
EOF

    git add softmax.py
    git commit -m "Optimize softmax by removing max subtraction"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Create 78 more dummy commits
    for i in $(seq 122 199); do
        echo "# dummy commit $i" >> dummy.txt
        git add dummy.txt
        git commit -m "Dummy commit $i"
    done

    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user