apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Create directories
    mkdir -p /app/malware_score_clone-1.2.0

    # Create the oracle binary
    cat << 'EOF' > /app/malware_oracle
#!/usr/bin/env python3
import sys
import re

def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    data = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            m = re.search(r'finished in (\d+\.\d+) ms', line)
            if m:
                data.append(float(m.group(1)))

    if not data:
        print("0.000000")
        return

    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    print(f"{variance:.6f}")

if __name__ == '__main__':
    main()
EOF
    chmod +x /app/malware_oracle

    # Create the buggy Python script
    cat << 'EOF' > /app/malware_score_clone-1.2.0/scorer.py
import sys
import re

def main():
    if len(sys.argv) != 2:
        sys.exit(1)

    data = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            m = re.search(r'finished in (\d+\.\d{1,2}) ms', line)
            if m:
                data.append(float(m.group(1)))

    if not data:
        print("0.000000")
        return

    n = len(data)
    sum_x = sum(data)
    sum_x2 = sum(x*x for x in data)
    variance = (sum_x2 - (sum_x * sum_x) / n) / n
    print(f"{variance:.6f}")

if __name__ == '__main__':
    main()
EOF

    # Create the user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user