apt-get update && apt-get install -y python3 python3-pip git gcc make strace
pip3 install pytest

mkdir -p /home/user/data_service
cd /home/user/data_service
git init
git config --global user.email "test@example.com"
git config --global user.name "Test User"

cat << 'EOF' > Makefile
all:
	gcc -shared -o libprocessor.so -fPIC processor.c -pthread
EOF

cat << 'EOF' > worker.py
import ctypes
import threading
import time
import argparse

lib = ctypes.CDLL('./libprocessor.so')

def worker_task():
    for _ in range(500):
        lib.process_data()
        time.sleep(0.001)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-duration", type=int, default=3)
    args = parser.parse_args()

    threads = []
    start_time = time.time()

    while time.time() - start_time < args.run_duration:
        t = threading.Thread(target=worker_task)
        t.start()
        threads.append(t)
        if len(threads) >= 10:
            for t in threads:
                t.join()
            threads = []
EOF

# Initial Good Commit
cat << 'EOF' > processor.c
#include <stdlib.h>
#include <stdio.h>

void process_data() {
    char *buffer = malloc(1024 * 1024); // 1MB
    if (buffer) {
        buffer[0] = 'a';
        free(buffer);
    }
}
EOF

git add Makefile worker.py processor.c
git commit -m "Initial commit: basic working processing"

# Commit 2 (Good)
echo "// some comment" >> processor.c
git commit -am "Add comment to processor"

# Commit 3 (Bad - introduces leak)
cat << 'EOF' > processor.c
#include <stdlib.h>
#include <stdio.h>

void process_data() {
    char *buffer = malloc(1024 * 1024); // 1MB
    if (buffer) {
        buffer[0] = 'a';
        // Bug introduced: removed free(buffer)
    }
}
EOF
git commit -am "Optimize data processing"
BAD_COMMIT=$(git rev-parse HEAD)

# Commit 4 (Bad)
echo "// another comment" >> processor.c
git commit -am "Add another comment"

# Compile for the current HEAD so it's ready
make

# Save the expected JSON to a secret location for verification
cat << EOF > /tmp/expected_report.json
{
  "bad_commit": "${BAD_COMMIT}",
  "leaking_c_function": "process_data",
  "system_call_leaking": "mmap"
}
EOF

useradd -m -s /bin/bash user || true
chmod -R 777 /home/user