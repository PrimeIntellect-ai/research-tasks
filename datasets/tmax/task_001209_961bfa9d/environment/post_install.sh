apt-get update && apt-get install -y python3 python3-pip gcc make
pip3 install pytest

mkdir -p /home/user/project/src
mkdir -p /home/user/project/tests

cat << 'EOF' > /home/user/project/src/processor.c
#include <stdlib.h>

static int* buffer;

void init_processor() {
    if (!buffer) {
        buffer = (int*)malloc(100 * sizeof(int));
        buffer[0] = 0;
    }
}

void process_data(int val) {
    if (buffer) {
        buffer[0] += val;
    }
}

int get_result() {
    if (buffer) {
        return buffer[0];
    }
    return -1;
}

void cleanup_processor() {
    if (buffer) {
        free(buffer);
        // BUG: buffer is not set to NULL after freeing.
        // When the next test calls init_processor(), it bypasses malloc,
        // and process_data attempts to write to freed memory, causing a segfault.
    }
}
EOF

cat << 'EOF' > /home/user/project/Makefile
all:
	gcc -shared -fPIC -O2 src/processor.c -o libprocessor.so
EOF

cat << 'EOF' > /home/user/project/tests/test_one.py
import ctypes
import os
import sys

def run():
    lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'libprocessor.so'))
    lib = ctypes.CDLL(lib_path)

    lib.init_processor()
    lib.process_data(5)
    res = lib.get_result()
    if res != 5:
        sys.exit(1)
    lib.cleanup_processor()

if __name__ == '__main__':
    run()
EOF

cat << 'EOF' > /home/user/project/tests/test_two.py
import ctypes
import os
import sys

def run():
    lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'libprocessor.so'))
    lib = ctypes.CDLL(lib_path)

    lib.init_processor()
    lib.process_data(10)
    res = lib.get_result()
    if res != 10:
        sys.exit(1)
    lib.cleanup_processor()

if __name__ == '__main__':
    run()
EOF

cat << 'EOF' > /home/user/project/tests/run_all.py
import test_one
import test_two
import sys

if __name__ == '__main__':
    try:
        test_one.run()
        test_two.run()
        print("All tests passed.")
    except Exception as e:
        print(f"Test failed: {e}")
        sys.exit(1)
EOF

cat << 'EOF' > /home/user/project/ci.sh
#!/bin/bash
cd /home/user/project
make clean >/dev/null 2>&1 || true
make
if python3 tests/run_all.py; then
    echo "CI PASS"
    echo "SUCCESS" > ci_success.log
    exit 0
else
    echo "CI FAILED"
    exit 1
fi
EOF

chmod +x /home/user/project/ci.sh

useradd -m -s /bin/bash user || true
chown -R user:user /home/user/project
chmod -R 777 /home/user