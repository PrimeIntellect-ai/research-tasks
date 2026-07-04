apt-get update && apt-get install -y python3 python3-pip git gcc make gdb
    pip3 install pytest

    mkdir -p /home/user/pipeline_repo
    mkdir -p /home/user/data

    cd /home/user/pipeline_repo
    git config --global init.defaultBranch main
    git config --global user.email "dev@example.com"
    git config --global user.name "DevOps Engineer"
    git init

    cat << 'EOF' > mathops.c
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

// Computes a normalized variance, but has a fixed buffer size
double compute_metric(double* values, int count) {
    double cache[50];
    double sum = 0.0;

    // Buffer overflow if count > 50
    for(int i = 0; i < count; i++) {
        cache[i] = sqrt(values[i]); 
        sum += cache[i];
    }

    return sum / count;
}
EOF

    cat << 'EOF' > Makefile
all:
	gcc -shared -o libmathops.so -fPIC mathops.c
EOF

    cat << 'EOF' > process.py
import sys
import ctypes
import base64

if len(sys.argv) != 3:
    print("Usage: python3 process.py <logfile> <secret_key>")
    sys.exit(1)

log_file = sys.argv[1]
secret_key = sys.argv[2]

if secret_key != "MATH_SEC_88291":
    print("Invalid secret key!")
    sys.exit(1)

# Load library
try:
    lib = ctypes.CDLL('./libmathops.so')
    lib.compute_metric.restype = ctypes.c_double
    lib.compute_metric.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
except OSError:
    print("Failed to load libmathops.so. Did you build it?")
    sys.exit(1)

# Read and "decrypt" logs (base64 decode for simplicity in this task)
with open(log_file, 'r') as f:
    for line in f:
        decoded = base64.b64decode(line.strip()).decode('utf-8')
        parts = decoded.split('|')
        log_id = parts[0]
        values = [float(x) for x in parts[1].split(',')]

        arr_type = ctypes.c_double * len(values)
        arr = arr_type(*values)

        # This will crash on LOG_409 due to len(values) > 50
        result = lib.compute_metric(arr, len(values))
        print(f"Processed {log_id}: {result}")
EOF

    git add mathops.c Makefile process.py
    git commit -m "Initial commit of math pipeline"

    echo 'SECRET_KEY="MATH_SEC_88291"' > config.py
    git add config.py
    git commit -m "Add config with keys"

    git rm config.py
    git commit -m "Remove hardcoded keys from repo"

    cd /home/user/data
    echo -n "LOG_101|1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0" | base64 > logs.enc
    echo "" >> logs.enc
    echo -n "LOG_205|1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0" | base64 >> logs.enc
    echo "" >> logs.enc
    echo -n "LOG_409|1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10,1,2,3,4,5,6,7,8,9,10" | base64 >> logs.enc
    echo "" >> logs.enc

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user