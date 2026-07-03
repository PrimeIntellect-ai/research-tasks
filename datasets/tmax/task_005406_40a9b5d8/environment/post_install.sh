apt-get update && apt-get install -y python3 python3-pip
    pip3 install pytest

    useradd -m -s /bin/bash user || true

    mkdir -p /home/user

    cat << 'EOF' > /home/user/processor.py
#!/usr/bin/env python3
import sys
import csv

def process_data(file_path):
    total = 0.0
    count = 0
    degraded_mode = False

    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                val = float(row['amount'])

                # The crash trigger
                if abs(val - 8888.88) < 0.001:
                    raise ValueError("Internal state corruption")

                # The precision loss trigger
                if abs(val - 1337.42) < 0.001:
                    degraded_mode = True

                if degraded_mode:
                    # Precision loss: truncates to integer
                    total += float(int(val))
                else:
                    total += val

                count += 1

        if count > 0:
            print(f"Total: {total:.2f}")
            print(f"Mean: {total/count:.2f}")
        else:
            print("No data")
    except Exception as e:
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: processor.py <csv_file>")
        sys.exit(1)
    process_data(sys.argv[1])
EOF
    chmod +x /home/user/processor.py

    cat << 'EOF' > /home/user/sample_data.csv
amount
100.50
250.75
300.20
1337.42
45.99
120.80
500.55
EOF

    chmod -R 777 /home/user