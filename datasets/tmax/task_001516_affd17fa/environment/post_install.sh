apt-get update && apt-get install -y python3 python3-pip strace
    pip3 install pytest

    mkdir -p /home/user/project

    cat << 'EOF' > /home/user/project/config.ini
DATA_FILE=/home/user/project/data.txt

EOF

    cat << 'EOF' > /home/user/project/data.txt
1000000.1, 1000000.2, 1000000.3,
1000000.4, 1000000.5
1000000.6, , 1000000.7
EOF

    cat << 'EOF' > /home/user/project/precompute.py
import sys

def read_config():
    with open('/home/user/project/config.ini', 'r') as f:
        return f.read().split('=')[1]

def parse_data(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            parts = line.split(',')
            for p in parts:
                p = p.strip()
                if p:
                    data.append(float(p))
    return data

def compute_variance(data):
    n = len(data)
    if n < 2: return 0.0
    sum_x = sum(data)
    sum_x2 = sum(x*x for x in data)
    return (sum_x2 - (sum_x * sum_x) / n) / (n - 1)

def main():
    filepath = read_config()
    try:
        data = parse_data(filepath)
    except Exception:
        sys.exit(1)

    var = compute_variance(data)
    with open('/home/user/project/output.txt', 'w') as f:
        f.write(f"{var:.6f}\n")

if __name__ == '__main__':
    main()
EOF

    cat << 'EOF' > /home/user/project/build.sh
#!/bin/bash
python3 /home/user/project/precompute.py
if [ $? -ne 0 ]; then
    echo "Build failed"
    exit 1
fi
if [ ! -f /home/user/project/output.txt ]; then
    echo "Output missing"
    exit 1
fi
ACTUAL=$(cat /home/user/project/output.txt)
EXPECTED="0.046667"
if [ "$ACTUAL" != "$EXPECTED" ]; then
    echo "Incorrect output: $ACTUAL"
    exit 1
fi
echo "Build succeeded"
exit 0
EOF

    chmod +x /home/user/project/build.sh

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user