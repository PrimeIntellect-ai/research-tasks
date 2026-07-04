apt-get update && apt-get install -y python3 python3-pip gcc python3-dev
    pip3 install pytest cython numpy

    mkdir -p /home/user

    cat << 'EOF' > /home/user/calc_chunk.pyx
import numpy as np
cimport numpy as cnp

def compute_subdomain(int start, int end, int num_points):
    cdef double dx = (end - start) / float(num_points)
    cdef double total = 0.0
    cdef double x
    cdef int i
    for i in range(num_points):
        x = start + i * dx
        # Oscillating function with varying magnitudes
        total += np.sin(x**2) * np.exp(-x/1000.0) * dx
    return total
EOF

    cat << 'EOF' > /home/user/setup.py
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules = cythonize("calc_chunk.pyx"),
    include_dirs=[numpy.get_include()]
)
EOF

    cat << 'EOF' > /home/user/sim.py
import multiprocessing
import calc_chunk

def worker(args):
    idx, start, end, num_points = args
    val = calc_chunk.compute_subdomain(start, end, num_points)
    return idx, val

def main():
    num_chunks = 100
    mesh_start = 0
    mesh_end = 1000
    points_per_chunk = 100000

    chunk_size = int((mesh_end - mesh_start) / num_chunks)

    tasks = []
    for i in range(num_chunks):
        start = mesh_start + i * chunk_size
        end = start + chunk_size
        tasks.append((i, start, end, points_per_chunk))

    total_val = 0.0
    with multiprocessing.Pool(processes=4) as pool:
        # BUG: non-deterministic addition order
        for idx, val in pool.imap_unordered(worker, tasks):
            total_val += val

    print(f"{total_val:.15f}")

if __name__ == '__main__':
    main()
EOF

    cd /home/user
    python3 setup.py build_ext --inplace

    cat << 'EOF' > /home/user/gen_ref.py
import multiprocessing
import calc_chunk

def worker(args):
    idx, start, end, num_points = args
    val = calc_chunk.compute_subdomain(start, end, num_points)
    return idx, val

def main():
    num_chunks = 100
    mesh_start = 0
    mesh_end = 1000
    points_per_chunk = 100000

    chunk_size = int((mesh_end - mesh_start) / num_chunks)

    tasks = []
    for i in range(num_chunks):
        start = mesh_start + i * chunk_size
        end = start + chunk_size
        tasks.append((i, start, end, points_per_chunk))

    results = []
    with multiprocessing.Pool(processes=4) as pool:
        for idx, val in pool.imap_unordered(worker, tasks):
            results.append((idx, val))

    results.sort(key=lambda x: x[0])
    total_val = 0.0
    for idx, val in results:
        total_val += val

    with open('/home/user/reference.txt', 'w') as f:
        f.write(f"{total_val:.15f}\n")

if __name__ == '__main__':
    main()
EOF

    python3 /home/user/gen_ref.py
    rm /home/user/gen_ref.py

    # Clean up the compiled extension so the agent has to do task 1
    rm -rf /home/user/build /home/user/calc_chunk.*.so /home/user/calc_chunk.c

    useradd -m -s /bin/bash user || true
    chmod -R 777 /home/user