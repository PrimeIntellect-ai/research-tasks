apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    mkdir -p /home/user/financial_parser
    cd /home/user/financial_parser
    git init

    # Create the data file with edge cases (spaces before numbers, etc.)
    cat << 'EOF' > records.txt
TXN001, 450.25
TXN002,120.00
TXN003, 99.99
TXN004,   3.50
EOF

    # Create the initial good parser.py
    cat << 'EOF' > parser.py
import sys

def parse(file_path):
    total = 0.0
    with open(file_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(',')
            # Correctly handle spaces and keep precision
            val_str = parts[1].strip()
            val = float(val_str)
            total += val
    print(f"Total: {total:.2f}")

if __name__ == "__main__":
    parse(sys.argv[1])
EOF

    git config user.email "test@example.com"
    git config user.name "Test User"
    git add records.txt parser.py
    git commit -m "Initial working commit"
    git tag v1.0

    # Generate commits 2 to 136
    for i in $(seq 2 136); do
        echo "# Non-breaking change $i" >> parser.py
        git commit -am "Refactoring step $i"
    done

    # Commit 137: Introduce the regression (bad format parsing fix that crashes on spaces/decimals)
    cat << 'EOF' > parser.py
import sys

def parse(file_path):
    total = 0.0
    with open(file_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            parts = line.strip().split(',')
            val_str = parts[1]

            # BUG INTRODUCED HERE: 
            # Developer tried to handle commas as decimals but broke standard decimal parsing
            # and forced integer conversion causing precision loss if it didn't crash.
            if ' ' in val_str:
                val_str = val_str.replace('.', ',') # This causes float() to raise ValueError

            try:
                val = float(val_str)
            except ValueError:
                # Fallback that loses precision and still might crash
                val = float(int(val_str.split(',')[0]))

            total += val
    print(f"Total: {total:.2f}")

if __name__ == "__main__":
    parse(sys.argv[1])
EOF
    git commit -am "Update parsing logic for European locales"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Generate commits 138 to 200
    for i in $(seq 138 200); do
        echo "# Further development $i" >> parser.py
        git commit -am "Feature advancement $i"
    done

    # Save the expected ground truth for verification internally
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user