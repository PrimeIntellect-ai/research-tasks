apt-get update && apt-get install -y python3 python3-pip git gcc gawk
    pip3 install pytest

    mkdir -p /home/user/sensor_pipeline
    cd /home/user/sensor_pipeline
    git init

    cat << 'EOF' > encode.py
import struct
import random

random.seed(42)
# Generate 1000 sensor readings
data = [random.uniform(-10.0, 10.0) for _ in range(1000)]

with open("data.bin", "wb") as f:
    f.write(struct.pack(f'{len(data)}d', *data))
EOF

    cat << 'EOF' > compute.c
#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *f = fopen("data.bin", "rb");
    if (!f) return 1;

    double sum_of_squares = 0.0;
    double val;
    int count = 0;

    while (fread(&val, sizeof(double), 1, f) == 1) {
        sum_of_squares += val * val;
        count++;
    }
    fclose(f);

    printf("%f\n", sum_of_squares);
    return 0;
}
EOF

    cat << 'EOF' > test.sh
#!/bin/bash
gcc -o compute compute.c
python3 encode.py
result=$(./compute)
expected=33842.0

# Check if result is within 100.0 of expected (simple float comparison in bash using awk)
is_valid=$(awk -v res="$result" -v exp="$expected" 'BEGIN { diff = res - exp; if (diff < 0) diff = -diff; if (diff < 100.0) print 1; else print 0; }')

if [ "$is_valid" -eq 1 ]; then
    echo "Pass"
    exit 0
else
    echo "Fail: got $result"
    exit 1
fi
EOF
    chmod +x test.sh

    git add .
    git config user.email "engineer@company.com"
    git config user.name "Ops Engineer"
    git commit -m "Initial commit: working pipeline"

    # Commit 2 (Good)
    echo "# Added a comment" >> encode.py
    git commit -am "Add comment to encode.py"

    # Commit 3 (Good)
    echo "// Added a comment" >> compute.c
    git commit -am "Add comment to compute.c"

    # Commit 4 (BAD COMMIT - introduces the bug)
    sed -i "s/f'{len(data)}d'/f'{len(data)}f'/" encode.py
    git commit -am "Optimize storage: use float32 for binary export"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Commit 5 (Bad)
    echo "# Extra comment" >> test.sh
    git commit -am "Update test script"

    # Commit 6 (Bad)
    echo "# Final comment" >> encode.py
    git commit -am "Finalize encoder"

    # Save truth
    echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt
    chmod 777 /tmp/expected_bad_commit.txt

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user