apt-get update && apt-get install -y python3 python3-pip git
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    python3 << 'EOF'
import os
import subprocess

# Create memory dump
os.makedirs('/home/user', exist_ok=True)
with open('/home/user/memory.dump', 'wb') as f:
    f.write(os.urandom(2048) + b'EXPECTED_METRIC_VALUE=3.142857142857142857142857142857' + os.urandom(2048))

# Setup git repo
repo_dir = '/home/user/repo'
os.makedirs(repo_dir, exist_ok=True)
os.chdir(repo_dir)

subprocess.run(['git', 'init'], check=True)
subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True)
subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True)

good_code = """
from decimal import Decimal, getcontext
getcontext().prec = 30
def calculate_metrics():
    return Decimal('22') / Decimal('7')
"""

bad_code = """
def calculate_metrics():
    return 22 / 7
"""

with open('math_ops.py', 'w') as f:
    f.write(good_code)

subprocess.run(['git', 'add', 'math_ops.py'], check=True)
subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)

bad_commit_hash = ""

for i in range(1, 201):
    if i == 115:
        with open('math_ops.py', 'w') as f:
            f.write(bad_code)
        subprocess.run(['git', 'add', 'math_ops.py'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Refactor math_ops.py for speed - commit {i}'], check=True)
        bad_commit_hash = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    else:
        with open('dummy.txt', 'w') as f:
            f.write(f'dummy content {i}')
        subprocess.run(['git', 'add', 'dummy.txt'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Dummy commit {i}'], check=True)

# Save the expected ground truth locally for test suites (out of agent's reach)
with open('/tmp/ground_truth_bad_commit.txt', 'w') as f:
    f.write(bad_commit_hash)
EOF

    chmod -R 777 /home/user