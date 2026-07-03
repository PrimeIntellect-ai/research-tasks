apt-get update && apt-get install -y python3 python3-pip git strace
    pip3 install pytest

    mkdir -p /home/user/suspicious_repo
    cd /home/user/suspicious_repo

    git init
    git config user.email "researcher@example.com"
    git config user.name "Security Researcher"

    # Commit 1: Clean version
    cat << 'EOF' > check_prime.py
import sys

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    n = int(sys.argv[1])
    if is_prime(n):
        print("Prime")
    else:
        print("Not Prime")
EOF
    git add check_prime.py
    git commit -m "Initial commit: basic prime checker"

    # Commit 2: Benign update
    echo "# Utility for checking primes" | cat - check_prime.py > temp && mv temp check_prime.py
    git add check_prime.py
    git commit -m "Add file header comment"

    # Commit 3: Benign update
    sed -i 's/return False/return False # not prime/g' check_prime.py
    git add check_prime.py
    git commit -m "Add inline comments"

    # Commit 4: The backdoor
    cat << 'EOF' > check_prime.py
# Utility for checking primes
import sys
import os

def is_prime(n):
    if n < 2: return False # not prime
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False # not prime
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    n = int(sys.argv[1])
    if n == 773:
        try:
            os.open('/tmp/.backdoor_x82', os.O_RDONLY)
        except OSError:
            pass
        sys.exit(139)
    if is_prime(n):
        print("Prime")
    else:
        print("Not Prime")
EOF
    git add check_prime.py
    git commit -m "Optimize prime loop conditions"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Commit 5: Benign update
    sed -i 's/print("Prime")/print(f"{n} is Prime")/g' check_prime.py
    git add check_prime.py
    git commit -m "Format output strings"

    # Commit 6: Benign update
    sed -i 's/print("Not Prime")/print(f"{n} is Not Prime")/g' check_prime.py
    git add check_prime.py
    git commit -m "Format negative output strings"

    # Save the bad commit hash to a verification file accessible to the test runner
    echo "$BAD_COMMIT" > /tmp/expected_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user