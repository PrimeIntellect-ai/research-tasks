# test_final_state.py

import os
import math
import subprocess
import sys

def test_cpp_file_fixed():
    cpp_path = "/home/user/mc_sim.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} is missing."

    with open(cpp_path, 'r') as f:
        content = f.read()

    assert "#pragma omp parallel for" in content, "The C++ program must retain the parallel for loop."
    assert "compute_energy" in content, "The C++ program must retain the compute_energy function."

def test_python_script_exists():
    py_path = "/home/user/run_convergence.py"
    assert os.path.isfile(py_path), f"Python script {py_path} is missing."

def test_hdf5_contents():
    hdf5_path = "/home/user/convergence_results.h5"
    assert os.path.isfile(hdf5_path), f"HDF5 output file {hdf5_path} is missing."

    # Recompute expected deterministic sequential summation
    seed = 12345
    Ns = [1000, 10000, 50000, 100000]
    expected_energies = []

    for N in Ns:
        total = 0.0
        for i in range(N):
            x = (i * 137.0 + seed) * 0.01
            total += math.sin(x) * math.cos(x * 2.5)
        expected_energies.append(total)

    # Python script to run in subprocess to avoid importing third-party h5py in pytest directly
    checker_script = f"""
import sys
import math

try:
    import h5py
except ImportError:
    print("h5py is not installed")
    sys.exit(1)

try:
    with h5py.File('{hdf5_path}', 'r') as f:
        if 'N_values' not in f or 'energies' not in f:
            print("Missing required datasets in HDF5 file.")
            sys.exit(1)

        n_vals = list(f['N_values'][:])
        e_vals = list(f['energies'][:])

        expected_n = {Ns}
        expected_e = {expected_energies}

        if n_vals != expected_n:
            print(f"N_values mismatch: expected {{expected_n}}, got {{n_vals}}")
            sys.exit(1)

        if len(e_vals) != len(expected_e):
            print(f"energies length mismatch: expected {{len(expected_e)}}, got {{len(e_vals)}}")
            sys.exit(1)

        for i, (a, b) in enumerate(zip(e_vals, expected_e)):
            if not math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-12):
                print(f"Energy mismatch at index {{i}} (N={{expected_n[i]}}): expected {{b}}, got {{a}}")
                sys.exit(1)

        # Check dtypes
        if f['N_values'].dtype.name != 'int32':
            print(f"N_values dtype mismatch: expected int32, got {{f['N_values'].dtype.name}}")
            sys.exit(1)

        if f['energies'].dtype.name != 'float64':
            print(f"energies dtype mismatch: expected float64, got {{f['energies'].dtype.name}}")
            sys.exit(1)

except Exception as e:
    print(f"Error reading HDF5: {{e}}")
    sys.exit(1)
"""

    result = subprocess.run([sys.executable, "-c", checker_script], capture_output=True, text=True)
    assert result.returncode == 0, f"HDF5 verification failed:\n{result.stdout}\n{result.stderr}"