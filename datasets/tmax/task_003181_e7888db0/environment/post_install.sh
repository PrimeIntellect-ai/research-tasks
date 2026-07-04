apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    # Create the oracle binary (implemented as a Python script for simplicity, simulating the C binary)
    mkdir -p /app
    cat << 'EOF' > /app/legacy_loc_etl
#!/usr/bin/env python3
import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    current_bucket = None
    queue = []

    for row in reader:
        if len(row) < 3:
            continue
        col1, col2, col3 = row[0], row[1], row[2]

        # Simulate the "Embedded Newline" Bug
        if '\n' in col2 or '\n' in col3:
            continue

        try:
            timestamp = int(col1)
        except ValueError:
            continue

        bucket = timestamp - (timestamp % 300)
        dist = abs(len(col2) - len(col3))

        if bucket != current_bucket:
            current_bucket = bucket
            queue = []

        queue.append(dist)
        if len(queue) > 3:
            queue.pop(0)

        mean = sum(queue) / len(queue)
        print(f"{bucket},{mean:.2f}")

if __name__ == '__main__':
    main()
EOF
    chmod +x /app/legacy_loc_etl

    # Create user
    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user