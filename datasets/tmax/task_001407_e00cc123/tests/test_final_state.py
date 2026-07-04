# test_final_state.py

import os
import sys
import subprocess
import pytest

def test_output_h5_exists():
    """Verify that the output.h5 file was created."""
    assert os.path.isfile("/home/user/data/output.h5"), "The file /home/user/data/output.h5 does not exist."

def test_trace_ci_txt_exists():
    """Verify that the trace_ci.txt file was created."""
    assert os.path.isfile("/home/user/data/trace_ci.txt"), "The file /home/user/data/trace_ci.txt does not exist."

def test_hdf5_contents_and_logic():
    """Verify the contents of the output.h5 file match the expected logic."""
    # We use a subprocess to run a script that imports h5py and numpy, 
    # ensuring the test file itself only imports standard library modules.
    script = """
import sys
try:
    import h5py
    import numpy as np
except ImportError:
    sys.exit(0) # Skip if not available, though they should be per environment setup

try:
    with h5py.File('/home/user/data/input.h5', 'r') as f:
        orig = f['cov_matrix'][:]
except Exception as e:
    print(f"Failed to read input.h5: {e}", file=sys.stderr)
    sys.exit(1)

try:
    with h5py.File('/home/user/data/output.h5', 'r') as f:
        assert 'reg_matrix' in f, "Dataset 'reg_matrix' not found in output.h5"
        reg = f['reg_matrix'][:]
except Exception as e:
    print(f"Failed to read output.h5: {e}", file=sys.stderr)
    sys.exit(1)

assert reg.shape == orig.shape, f"Expected shape {orig.shape}, got {reg.shape}"

diff = reg - orig
off_diag = diff - np.diag(np.diag(diff))

if not np.allclose(off_diag, 0, atol=1e-10):
    print("Off-diagonal elements of the regularized matrix were modified. Only the diagonal should be modified.", file=sys.stderr)
    sys.exit(1)

diags = np.diag(diff)
if not (np.all(diags > 0.004) and np.all(diags < 0.006)):
    print(f"Diagonal additions are out of expected range (mean of U(0, 0.01) is 0.005). Got min {diags.min()} and max {diags.max()}", file=sys.stderr)
    sys.exit(1)
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, f"HDF5 matrix validation failed:\n{result.stderr}"

def test_trace_ci_contents():
    """Verify the confidence intervals in trace_ci.txt."""
    script = """
import sys
try:
    import h5py
    import numpy as np
except ImportError:
    sys.exit(0)

with h5py.File('/home/user/data/input.h5', 'r') as f:
    orig = f['cov_matrix'][:]
orig_trace = np.trace(orig)

try:
    with open('/home/user/data/trace_ci.txt', 'r') as f:
        content = f.read().strip()
        bounds = content.split(',')
        if len(bounds) != 2:
            print(f"Expected 2 comma-separated values, got {len(bounds)}", file=sys.stderr)
            sys.exit(1)
        lower, upper = float(bounds[0]), float(bounds[1])
except Exception as e:
    print(f"Failed to parse trace_ci.txt: {e}", file=sys.stderr)
    sys.exit(1)

if not (orig_trace + 0.02 < lower < orig_trace + 0.045):
    print(f"Lower bound {lower} is out of the expected range.", file=sys.stderr)
    sys.exit(1)

if not (orig_trace + 0.055 < upper < orig_trace + 0.08):
    print(f"Upper bound {upper} is out of the expected range.", file=sys.stderr)
    sys.exit(1)
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, f"Trace CI validation failed:\n{result.stderr}"