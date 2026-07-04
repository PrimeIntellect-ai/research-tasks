# test_final_state.py

import os
import numpy as np
import pytest

def test_output_files_exist():
    """Check that the required output files exist."""
    assert os.path.exists('/home/user/output_spectra.npy'), "Output file /home/user/output_spectra.npy is missing."
    assert os.path.exists('/home/user/timing.log'), "Timing log file /home/user/timing.log is missing."

def test_mse_metric():
    """Verify that the Mean Squared Error (MSE) is within the acceptable threshold."""
    ref_path = '/app/reference_spectra.npy'
    out_path = '/home/user/output_spectra.npy'

    assert os.path.exists(ref_path), f"Reference file {ref_path} is missing."
    assert os.path.exists(out_path), f"Output file {out_path} is missing."

    try:
        ref = np.load(ref_path)
    except Exception as e:
        pytest.fail(f"Failed to load reference spectra: {e}")

    try:
        out = np.load(out_path)
    except Exception as e:
        pytest.fail(f"Failed to load output spectra: {e}")

    assert ref.shape == out.shape, f"Shape mismatch: reference {ref.shape} vs output {out.shape}"

    mse = np.mean((ref - out)**2)
    threshold = 1e-8

    assert mse <= threshold, f"MSE {mse} exceeds threshold {threshold}"

def test_timing_metric():
    """Verify that the execution time logged is within the acceptable threshold."""
    log_path = '/home/user/timing.log'

    assert os.path.exists(log_path), f"Timing log {log_path} is missing."

    try:
        with open(log_path, 'r') as f:
            time_str = f.read().strip()
            time_val = float(time_str)
    except ValueError:
        pytest.fail(f"Timing log does not contain a valid float: '{time_str}'")
    except Exception as e:
        pytest.fail(f"Failed to read timing log: {e}")

    threshold = 5.0
    assert time_val <= threshold, f"Execution time {time_val}s exceeds threshold {threshold}s"