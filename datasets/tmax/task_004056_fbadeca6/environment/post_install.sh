apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest numpy==1.26.4

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user/seq_repo
    cd /home/user/seq_repo
    git init
    git config user.email "dev@example.com"
    git config user.name "Dev"

    # Create requirements
    echo "numpy==1.26.4" > requirements.txt
    # Deliberately missing pytest which is needed by test_seq.py

    # Create working seq.py
    cat << 'EOF' > seq.py
def calculate_sequence(target, current=1, step=1):
    if current >= target:
        return current
    return calculate_sequence(target, current + step, step + 1)

if __name__ == "__main__":
    print(calculate_sequence(1000))
EOF

    cat << 'EOF' > test_seq.py
import pytest
from seq import calculate_sequence

def test_sequence():
    assert calculate_sequence(100) > 0
EOF

    git add seq.py test_seq.py requirements.txt
    git commit -m "Initial commit"

    # Create 5 dummy commits
    for i in {1..5}; do
        echo "# dummy $i" >> seq.py
        git commit -am "Dummy commit $i"
    done

    # INTRODUCE BUG
    cat << 'EOF' > seq.py
import numpy as np

def calculate_sequence(target, current=np.int8(1), step=np.int8(1)):
    # Optimization: use int8 to save memory
    if current >= target:
        return current
    return calculate_sequence(target, current + step, step + 1)

if __name__ == "__main__":
    print(calculate_sequence(1000))
EOF

    git commit -am "Optimize memory usage by using numpy int8"
    BAD_COMMIT=$(git rev-parse --short HEAD)
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    # Create 5 more dummy commits
    for i in {6..10}; do
        echo "# dummy $i" >> seq.py
        git commit -am "Dummy commit $i"
    done

    chown -R user:user /home/user/seq_repo
    chmod -R 777 /home/user