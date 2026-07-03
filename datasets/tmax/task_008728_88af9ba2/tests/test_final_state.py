# test_final_state.py
import os
import csv
import math
import subprocess
import json
import pytest

def get_matrices_from_h5(file_path):
    """Reads the matrices from the HDF5 file using a subprocess since h5py is installed in the env."""
    script = f"""
import h5py
import json

try:
    with h5py.File('{file_path}', 'r') as f:
        matrices = f['cov_matrices'][:].tolist()
    print(json.dumps(matrices))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
"""
    try:
        out = subprocess.check_output(['python3', '-c', script], text=True)
        data = json.loads(out)
        if "error" in data:
            pytest.fail(f"Failed to read HDF5 file: {data['error']}")
        return data
    except subprocess.CalledProcessError:
        pytest.fail("Failed to execute python script to read HDF5 file.")

def cholesky_trace(A, lam):
    """Computes the trace of the Cholesky factor L of (A + lam * I) in pure Python."""
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    trace = 0.0
    for i in range(n):
        for j in range(i + 1):
            s = sum(L[i][k] * L[j][k] for k in range(j))
            if i == j:
                val = A[i][i] + lam - s
                if val <= 0:
                    return None
                L[i][j] = math.sqrt(val)
                trace += L[i][j]
            else:
                if L[j][j] == 0:
                    return None
                L[i][j] = (A[i][j] - s) / L[j][j]
    return trace

def test_results_csv_exists_and_format():
    """Check that results.csv exists and has the correct format."""
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"The results file does not exist at {results_path}"

    with open(results_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The results.csv file is empty."
    assert rows[0] == ['index', 'lambda', 'trace_L'], f"Incorrect header in results.csv: {rows[0]}"
    assert len(rows) == 6, f"Expected 5 data rows, got {len(rows) - 1}"

def test_results_values():
    """Verify the lambda values and the computed traces."""
    results_path = "/home/user/results.csv"
    h5_path = "/home/user/covariances.h5"

    assert os.path.isfile(results_path), "results.csv is missing."
    assert os.path.isfile(h5_path), "covariances.h5 is missing."

    matrices = get_matrices_from_h5(h5_path)
    assert len(matrices) == 5, "Expected 5 matrices in the HDF5 file."

    with open(results_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for i, row in enumerate(rows):
        idx = int(row['index'])
        assert idx == i, f"Expected index {i}, got {idx}"

        lam = float(row['lambda'])
        trace_l = float(row['trace_L'])

        if i == 0:
            assert math.isclose(lam, 0.0, abs_tol=1e-5), f"Matrix 0 is strongly SPD. Expected lambda=0.0, got {lam}"
        elif i == 1:
            assert lam >= 0.0, f"Matrix 1 is singular. Expected lambda >= 0.0, got {lam}"
        elif i == 2:
            assert lam >= 0.01, f"Matrix 2 is negative definite. Expected lambda >= 0.01, got {lam}"
        elif i == 3:
            assert math.isclose(lam, 0.0, abs_tol=1e-5), f"Matrix 3 is strongly SPD. Expected lambda=0.0, got {lam}"
        elif i == 4:
            assert lam >= 0.0001, f"Matrix 4 is near singular. Expected lambda >= 0.0001, got {lam}"

        expected_trace = cholesky_trace(matrices[i], lam)
        assert expected_trace is not None, f"Matrix {i} with lambda {lam} is still not positive definite."

        assert math.isclose(trace_l, expected_trace, rel_tol=1e-3, abs_tol=1e-3), \
            f"Trace mismatch for matrix {i}: expected ~{expected_trace:.4f}, got {trace_l:.4f}"