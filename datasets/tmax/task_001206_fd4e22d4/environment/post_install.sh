apt-get update && apt-get install -y python3 python3-pip git gcc make
pip3 install pytest

useradd -m -s /bin/bash user || true

mkdir -p /home/user/nightly_processor
cd /home/user/nightly_processor
git init
git config user.name "OnCall Eng"
git config user.email "oncall@example.com"

# Create initial good state
cat << 'EOF' > Makefile
CC=gcc
CFLAGS=-O2

all: processor

processor: processor.c
	$(CC) $(CFLAGS) -o processor processor.c -lm
EOF

cat << 'EOF' > processor.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int process_data(int val) {
    if (val < 0) {
        return 0; // Handled correctly in good commit
    }
    int result = 0;
    while (val > 0) {
        result += val % 10;
        val /= 10;
    }
    return result;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    int val;
    int total = 0;
    while (fscanf(f, "%d", &val) == 1) {
        total += process_data(val);
    }
    fclose(f);

    // Simulate some math dependency
    double final_val = sqrt((double)total);
    printf("%d\n", (int)final_val);
    return 0;
}
EOF

cat << 'EOF' > aggregator.py
import sys
import subprocess

def run(dataset, output):
    res = subprocess.run(['./processor', dataset], capture_output=True, text=True)
    if res.returncode == 0:
        with open(output, 'w') as f:
            f.write(f"PROCESSED_TOTAL:{res.stdout.strip()}\n")
    else:
        sys.exit(1)

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2])
EOF

git add Makefile processor.c aggregator.py
git commit -m "Initial commit: working data pipeline"
GOOD_COMMIT=$(git rev-parse HEAD)

# Commit 2: Unrelated change
echo "// Added comment for better readability" >> processor.c
git commit -am "Docs: update processor.c"

# Commit 3: Introduce the infinite loop regression (Bad Commit)
cat << 'EOF' > processor.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int process_data(int val) {
    int result = 0;
    // BUG: If val is negative, val % 10 is negative or 0, val / 10 is 0.
    // Wait, let's make it an explicit infinite loop for negative numbers
    while (val != 0) {
        result += val % 10;
        if (val > 0) {
            val /= 10;
        }
        // if val is negative, it never changes, infinite loop
    }
    return result;
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    FILE *f = fopen(argv[1], "r");
    if (!f) return 1;

    int val;
    int total = 0;
    while (fscanf(f, "%d", &val) == 1) {
        total += process_data(val);
    }
    fclose(f);

    double final_val = sqrt((double)total);
    printf("%d\n", (int)final_val);
    return 0;
}
EOF
git commit -am "Feature: refactor data processing loop"
BAD_COMMIT=$(git rev-parse HEAD)

# Commit 4: Another unrelated change
echo "# End of Makefile" >> Makefile
git commit -am "Build: update Makefile comments"

# Commit 5: Introduce the Linker error
cat << 'EOF' > Makefile
CC=gcc
CFLAGS=-O2

all: processor

processor: processor.c
	$(CC) $(CFLAGS) -o processor processor.c
EOF
git commit -am "Build: remove unnecessary flags"

# Create the dataset
cat << 'EOF' > /home/user/dataset.csv
452
103
-15
88
EOF

# Save the bad commit hash somewhere to verify later in the test system
echo "$BAD_COMMIT" > /tmp/expected_bad_commit.txt

chmod -R 777 /home/user