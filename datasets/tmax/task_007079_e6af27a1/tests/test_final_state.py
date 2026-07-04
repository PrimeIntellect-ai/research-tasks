# test_final_state.py
import os
import subprocess

def test_results_file_exists():
    """Check that the results.h5 file was created."""
    assert os.path.isfile('/home/user/results.h5'), "/home/user/results.h5 does not exist"

def test_results_content_and_logic():
    """
    Verify the contents of results.h5 by running a subprocess.
    This avoids importing third-party libraries directly in the pytest environment,
    but utilizes the libraries the user was required to install.
    """
    script = """
import sys
try:
    import h5py
    import numpy as np
except ImportError as e:
    print(f"Missing required library: {e}")
    sys.exit(1)

try:
    with h5py.File('/home/user/results.h5', 'r') as f:
        assert 'optimized_v' in f, "Dataset 'optimized_v' missing"
        assert 'final_positions' in f, "Dataset 'final_positions' missing"
        assert 'target_count' in f, "Dataset 'target_count' missing"

        v = f['optimized_v'][:]
        pos = f['final_positions'][:]
        count = f['target_count'][()]

        assert v.shape == (2,), f"optimized_v shape is {v.shape}, expected (2,)"
        assert pos.shape == (10000, 2), f"final_positions shape is {pos.shape}, expected (10000, 2)"

        # Check that NaN tracking works
        nans = np.isnan(pos[:,0])
        assert np.sum(nans) > 0, "No trapped particles (NaNs) found!"

        # Check the success count matches what we compute from positions
        active_pos = pos[~nans]
        dist_target = np.sqrt(np.sum((active_pos - np.array([10.0, 10.0]))**2, axis=1))
        computed_count = np.sum(dist_target <= 2.0)

        assert int(count) == int(computed_count), f"target_count ({count}) does not match computed count ({computed_count})"
        assert computed_count > 1000, f"Optimization failed: only {computed_count} particles reached the target (expected > 1000)."

except Exception as e:
    print(f"Assertion/Verification Error: {e}")
    sys.exit(1)
"""

    result = subprocess.run(
        ['python3', '-c', script],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Verification failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"