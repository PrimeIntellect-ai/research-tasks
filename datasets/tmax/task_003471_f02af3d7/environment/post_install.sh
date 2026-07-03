apt-get update && apt-get install -y python3 python3-pip gcc make zlib1g-dev
    pip3 install pytest

    mkdir -p /app/log_extractor-1.0.2
    mkdir -p /home/user

    cat << 'EOF' > /app/log_extractor-1.0.2/extractor.c
#include <stdio.h>
#include <zlib.h>
#include <stdlib.h>

int main(int argc, char** argv) {
    if (argc != 3) {
        printf("Usage: %s <input.bin> <output.txt>\n", argv[0]);
        return 1;
    }
    gzFile in = gzopen(argv[1], "rb");
    if (!in) return 1;
    FILE* out = fopen(argv[2], "wb");
    if (!out) return 1;
    char buf[4096];
    int len;
    while ((len = gzread(in, buf, sizeof(buf))) > 0) {
        fwrite(buf, 1, len, out);
    }
    gzclose(in);
    fclose(out);
    return 0;
}
EOF

    cat << 'EOF' > /app/log_extractor-1.0.2/Makefile
extractor: extractor.c
	gcc -o extractor extractor.c
EOF

    cat << 'EOF' > /app/setup.py
import os
import gzip
import random

valid_ids = []
random.seed(42)

with open('/tmp/logs.txt', 'wb') as f:
    for i in range(1, 5001):
        corrupt = random.random() < 0.25
        lines = [f"RECORD_START {i}".encode()]
        lines.append(f"Value: {random.random()*100:.2f}".encode())
        lines.append(f"Status: OK".encode())
        if corrupt:
            bad_byte = bytes([random.choice([1, 2, 3, 4, 5, 27, 127, 200, 255])])
            lines.append(b"Junk: " + bad_byte)
        else:
            valid_ids.append(i)
        lines.append(b"RECORD_END\n")

        f.write(b'\n'.join(lines) + b'\n')

with open('/tmp/logs.txt', 'rb') as f_in:
    with gzip.open('/app/raw_data.bin', 'wb') as f_out:
        f_out.write(f_in.read())

with open('/app/valid_ids.txt', 'w') as f:
    for vid in valid_ids:
        f.write(f"{vid}\n")
EOF

    python3 /app/setup.py
    rm /app/setup.py /tmp/logs.txt

    cat << 'EOF' > /app/verify.py
import os
import sys

def verify():
    if not os.path.exists('/home/user/cleaned_data.csv'):
        print("CSV file not found.")
        sys.exit(1)

    with open('/app/valid_ids.txt', 'r') as f:
        ground_truth = set(line.strip() for line in f if line.strip())

    predicted = set()
    with open('/home/user/cleaned_data.csv', 'r') as f:
        header = f.readline().strip()
        if header != "ID,Value,Status":
            print(f"Incorrect header: {header}")
            sys.exit(1)
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 1:
                predicted.add(parts[0])

    tp = len(predicted & ground_truth)
    fp = len(predicted - ground_truth)
    fn = len(ground_truth - predicted)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print(f"F1 Score: {f1:.4f}")
    if f1 >= 0.99:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    verify()
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user