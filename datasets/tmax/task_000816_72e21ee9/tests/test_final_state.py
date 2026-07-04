# test_final_state.py

import os
import subprocess
import sys
import tempfile

def test_results_file_exists():
    assert os.path.exists('/home/user/results.h5'), "Output file /home/user/results.h5 does not exist."

def test_results_correctness():
    """
    Verifies the correctness of the generated HDF5 file using numpy, h5py, and scipy.
    Runs in a subprocess to strictly adhere to the standard-library-only rule for the pytest file itself.
    """
    script = """
import sys
try:
    import numpy as np
    import h5py
    from scipy.special import logsumexp
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)

try:
    with h5py.File('/home/user/seq_data.h5', 'r') as f:
        X = f['embeddings'][:]
except Exception as e:
    print(f"Failed to read input file: {e}")
    sys.exit(1)

try:
    with h5py.File('/home/user/results.h5', 'r') as f:
        if 'log_scores' not in f:
            print("Dataset 'log_scores' not found in results.h5")
            sys.exit(5)
        S_agent = f['log_scores'][:]
except Exception as e:
    print(f"Failed to read output file: {e}")
    sys.exit(1)

D = np.dot(X, X.T)
S_true = D - logsumexp(D, axis=1, keepdims=True)

if np.isnan(S_agent).any():
    print("Output contains NaNs. Numerical stability requirement failed.")
    sys.exit(2)

if S_agent.shape != S_true.shape:
    print(f"Expected shape {S_true.shape}, got {S_agent.shape}")
    sys.exit(3)

max_diff = np.max(np.abs(S_agent - S_true))
if max_diff > 1e-10:
    print(f"Values differ from ground truth by {max_diff}")
    sys.exit(4)

print("PASS")
sys.exit(0)
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
        tmp.write(script)
        tmp_path = tmp.name

    try:
        result = subprocess.run([sys.executable, tmp_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Verification failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    finally:
        os.remove(tmp_path)