apt-get update && apt-get install -y python3 python3-pip python3-dev gcc
    pip3 install pytest

    mkdir -p /home/user/pde_solver
    cd /home/user/pde_solver

    cat << 'EOF' > requirements.txt
numpy==1.24.3
cython==0.29.36
EOF

    cat << 'EOF' > setup.py
from setuptools import setup
from Cython.Build import cythonize

# BUG: Missing include_dirs
setup(
    ext_modules=cythonize("solver.pyx", language_level=3)
)
EOF

    cat << 'EOF' > solver.pyx
# cython: boundscheck=False, wraparound=False
import numpy as np
cimport numpy as np

def solve_1d_heat(np.ndarray[np.float64_t, ndim=1] u, int steps):
    cdef int N = u.shape[0]
    cdef int t, i
    cdef np.ndarray[np.float64_t, ndim=1] u_next = np.empty_like(u)

    for t in range(steps):
        u_next[0] = 0.0
        # BUG: The loop goes up to N, causing an out-of-bounds access on u[i+1] when i=N-1
        for i in range(1, N): 
            u_next[i] = u[i] + 0.1 * (u[i-1] - 2*u[i] + u[i+1])
        u_next[N-1] = 0.0

        for i in range(N):
            u[i] = u_next[i]

    return u
EOF

    cat << 'EOF' > run_large_sim.py
import numpy as np
from solver import solve_1d_heat

print("Starting large simulation...")
arr = np.zeros(10000000, dtype=np.float64)
arr[5000000] = 100.0
solve_1d_heat(arr, 100)
print("Done.")
EOF

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user