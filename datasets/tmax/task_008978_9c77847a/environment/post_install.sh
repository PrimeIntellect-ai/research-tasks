apt-get update && apt-get install -y python3 python3-pip git
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/data_processor
cd /home/user/data_processor

cat << 'EOF' > run.py
import sys
import json
from processor import run_pipeline

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python run.py <input.json> <output.json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        data = json.load(f)

    results = run_pipeline(data)

    with open(sys.argv[2], 'w') as f:
        json.dump(results, f)
EOF

cat << 'EOF' > processor.py
def extract_code(payload):
    tokens = payload.get('tokens', [])
    if len(tokens) > 2:
        return tokens[2]
    return None

def run_pipeline(data):
    results = []
    for d in data:
        results.append(extract_code(d))
    return results
EOF

git init
git add run.py processor.py
git config user.email "test@example.com"
git config user.name "Test User"
git commit -m "Initial commit: working pipeline"
GOOD_COMMIT=$(git rev-parse HEAD)

# Commit 2
cat << 'EOF' > processor.py
import logging

def extract_code(payload):
    tokens = payload.get('tokens', [])
    if len(tokens) > 2:
        return tokens[2]
    return None

def run_pipeline(data):
    logging.info(f"Processing {len(data)} records")
    results = []
    for d in data:
        results.append(extract_code(d))
    return results
EOF
git add processor.py
git commit -m "Add logging to pipeline"

# Commit 3 (BAD COMMIT)
cat << 'EOF' > processor.py
import logging

def extract_code(payload):
    tokens = payload.get('tokens', [])
    # Optimized extraction, assumes tokens has at least 3 elements if not empty
    return tokens[2] if tokens else None

def run_pipeline(data):
    logging.info(f"Processing {len(data)} records")
    results = []
    for d in data:
        results.append(extract_code(d))
    return results
EOF
git add processor.py
git commit -m "Optimize token extraction"
BAD_COMMIT=$(git rev-parse HEAD)

# Commit 4
cat << 'EOF' > processor.py
import logging

logging.basicConfig(level=logging.INFO)

def extract_code(payload):
    tokens = payload.get('tokens', [])
    return tokens[2] if tokens else None

def run_pipeline(data):
    logging.info(f"Processing {len(data)} records")
    results = []
    for d in data:
        results.append(extract_code(d))
    logging.info("Done processing")
    return results
EOF
git add processor.py
git commit -m "Configure logging basics"

# Commit 5
echo "# End of file" >> processor.py
git add processor.py
git commit -m "Add comment"

# Create input data
cat << 'EOF' > /home/user/input.json
[
    {"id": 1, "tokens": ["A", "B", "C", "D"]},
    {"id": 2, "tokens": ["X", "Y"]},
    {"id": 3, "tokens": ["1", "2", "3"]}
]
EOF

# Save the expected bad commit for verification
echo $BAD_COMMIT > /home/user/.expected_bad_commit

chmod -R 777 /home/user