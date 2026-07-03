apt-get update && apt-get install -y python3 python3-pip gcc procps coreutils
    pip3 install pytest

    mkdir -p /home/user
    cd /home/user

    cat << 'EOF' > parser.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int parse_payload(const unsigned char *data, int len) {
    int i = 0;
    int buffer_size = 10;
    unsigned char *buffer = malloc(buffer_size);
    int k = 0;

    while (i < len) {
        if (data[i] == 0xFF) {
            // BUG: Fails to increment 'i', causing infinite loop and memory leak
            if (k >= buffer_size) {
                buffer_size *= 2;
                buffer = realloc(buffer, buffer_size);
            }
            buffer[k++] = data[i];
            // Fix requires: i++;
        } else {
            if (k >= buffer_size) {
                buffer_size *= 2;
                buffer = realloc(buffer, buffer_size);
            }
            buffer[k++] = data[i];
            i++;
        }
    }
    free(buffer);
    return k;
}
EOF

    gcc -shared -o libparser.so -fPIC parser.c

    cat << 'EOF' > service.py
import sys
import ctypes
import os

if len(sys.argv) < 2:
    print("Usage: service.py <payload_file>")
    sys.exit(1)

parser = ctypes.CDLL('/home/user/libparser.so')
parser.parse_payload.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int]
parser.parse_payload.restype = ctypes.c_int

with open(sys.argv[1], 'rb') as f:
    data = f.read()

arr = (ctypes.c_ubyte * len(data))(*data)
result = parser.parse_payload(arr, len(data))

print(f"Parse complete: {len(data)} bytes")
EOF

    cat << 'EOF' > fuzzer.py
import os
import subprocess
import random
import sys

for i in range(50):
    payload = bytes([random.randint(0, 255) for _ in range(100)])
    with open('/tmp/fuzz.dat', 'wb') as f:
        f.write(payload)
    # 2 second timeout to detect hang
    try:
        subprocess.run(['python3', '/home/user/service.py', '/tmp/fuzz.dat'], timeout=2, stdout=subprocess.DEVNULL)
    except subprocess.TimeoutExpired:
        print("Fuzzer detected hang!")
        sys.exit(1)
print("Fuzzing complete. No hangs detected.")
EOF

    head -c 200 /dev/urandom > last_input.dat
    printf '\xFF\xFF\xFF' >> last_input.dat
    head -c 53 /dev/urandom >> last_input.dat

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user