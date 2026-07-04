apt-get update && apt-get install -y python3 python3-pip sqlite3 gcc make git
    pip3 install pytest

    # Setup script
    mkdir -p /home/user/app_repo
    cd /home/user/app_repo

    cat << 'EOF' > processor.c
#include <stdio.h>

int process_data(int *arr, int size) {
    int sum = 0;
    for (int i = 0; i < size; i++) {
        sum += arr[i];
    }
    return sum;
}
EOF

    cat << 'EOF' > Makefile
all: libprocessor.so

libprocessor.so: processor.c
	gcc -shared -o libprocessor.so -fPIC processor.c

test: all
	python3 test_app.py
EOF

    cat << 'EOF' > test_app.py
import ctypes
import os
import random

lib = ctypes.CDLL(os.path.abspath('./libprocessor.so'))
lib.process_data.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int]
lib.process_data.restype = ctypes.c_int

def run_test():
    size = 10
    arr = (ctypes.c_int * size)(*[1]*size)
    # create some garbage in memory just after
    garbage = (ctypes.c_int * 10)(*[random.randint(100, 1000) for _ in range(10)])

    result = lib.process_data(arr, size)
    assert result == 10, f"Expected 10, got {result}"

if __name__ == "__main__":
    for _ in range(100):
        run_test()
    print("Tests passed.")
EOF

    git init
    git config user.name "Dev"
    git config user.email "dev@example.com"
    git add .
    git commit -m "Initial working commit"

    # Commit 2
    echo "# minor change" >> Makefile
    git add Makefile
    git commit -m "Update Makefile"

    # Commit 3 (Bad commit)
    cat << 'EOF' > processor.c
#include <stdio.h>

int process_data(int *arr, int size) {
    int sum = 0;
    for (int i = 0; i <= size; i++) { // BUG: <= instead of <
        sum += arr[i];
    }
    return sum;
}
EOF
    git add processor.c
    git commit -m "Optimize processing loop"
    BAD_COMMIT=$(git rev-parse HEAD)

    # Commit 4
    echo "# another minor change" >> Makefile
    git add Makefile
    git commit -m "Another Makefile update"

    # Commit 5
    echo "# test update" >> test_app.py
    git add test_app.py
    git commit -m "Update test script"

    # Store bad commit for validation
    echo $BAD_COMMIT > /tmp/expected_bad_commit.txt

    # DB Crash Setup
    mkdir -p /home/user/db_crash
    cd /home/user/db_crash
    sqlite3 app.db "CREATE TABLE users (id INTEGER, name TEXT); INSERT INTO users VALUES (1, 'Alice');"

    # Use python to insert and SIGKILL to ensure WAL file is left behind uncheckpointed
    python3 -c "import sqlite3, os, signal; \
conn = sqlite3.connect('app.db'); \
conn.execute('PRAGMA journal_mode=WAL'); \
conn.execute('INSERT INTO users VALUES (2, \"Bob\")'); \
conn.commit(); \
os.kill(os.getpid(), signal.SIGKILL)" || true

    # Corrupt the main db file header
    dd if=/dev/urandom of=app.db bs=100 count=1 conv=notrunc

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user