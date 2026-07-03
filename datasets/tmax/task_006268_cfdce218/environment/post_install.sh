apt-get update && apt-get install -y python3 python3-pip procps
    pip3 install pytest

    mkdir -p /home/user/data
    mkdir -p /home/user/fraud_analyzer

    cat << 'EOF' > /home/user/data/transactions.csv
id,amount
1,1000000000.1
2,1000000000.2
3,1000000000.3
corrupt1,1000000000.4
4,1000000000.5
corrupt2,1000000000.6
5,1000000000.7
EOF

    sed -i 's/corrupt1/\x00\x00corrupt1/g' /home/user/data/transactions.csv
    sed -i 's/corrupt2/\x00\x00corrupt2/g' /home/user/data/transactions.csv

    cat << 'EOF' > /home/user/data_streamer.py
import time
import sys
f = open('/home/user/data/transactions.csv', 'r')
while True:
    time.sleep(10)
EOF

    cat << 'EOF' > /home/user/fraud_analyzer/setup.py
from setuptools import setup, find_packages
setup(
    name='fraud_analyzer',
    version='0.1.0',
    packages=find_packages(),
)
EOF

    cat << 'EOF' > /home/user/fraud_analyzer/__init__.py
# empty
EOF

    cat << 'EOF' > /home/user/fraud_analyzer/metrics.py
def calculate_variance(data):
    if not data:
        return 0.0
    n = len(data)
    sum_sq = sum(x**2 for x in data)
    sq_sum = sum(data)**2
    return (sum_sq - sq_sum / n) / n

# SYNTAX ERROR INTENTIONALLY INJECTED BELOW
def calculate_mean(data)
    return sum(data) / len(data)
EOF

    cat << 'EOF' > /home/user/fraud_analyzer/run.py
import argparse
import json
from fraud_analyzer.metrics import calculate_variance

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    amounts = []
    with open(args.input, 'r') as f:
        next(f) # skip header
        for line in f:
            if line.strip():
                parts = line.strip().split(',')
                amounts.append(float(parts[1]))

    variance = calculate_variance(amounts)

    with open(args.output, 'w') as f:
        json.dump({"variance": variance, "count": len(amounts)}, f)

if __name__ == '__main__':
    main()
EOF

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user