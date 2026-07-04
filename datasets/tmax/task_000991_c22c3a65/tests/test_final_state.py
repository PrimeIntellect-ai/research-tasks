# test_final_state.py

import os
import json
import pytest

def test_metrics_json_exists_and_meets_thresholds():
    metrics_file = "/home/user/workspace/metrics.json"
    assert os.path.isfile(metrics_file), f"Metrics file missing at {metrics_file}"

    try:
        with open(metrics_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read or parse metrics JSON: {e}")

    assert 'mse' in data, "Key 'mse' missing in metrics.json"
    assert 'speedup_ratio' in data, "Key 'speedup_ratio' missing in metrics.json"

    try:
        mse = float(data['mse'])
        speedup = float(data['speedup_ratio'])
    except ValueError as e:
        pytest.fail(f"Failed to convert metrics to float: {e}")

    assert mse <= 1e-4, f"FAIL: MSE {mse} is above threshold 1e-4"
    assert speedup >= 1.2, f"FAIL: Speedup {speedup} is below threshold 1.2"

def test_binaries_and_libraries_exist():
    go_binary = "/home/user/workspace/bin/fftapp"
    assert os.path.isfile(go_binary), f"Go binary missing at {go_binary}"
    assert os.access(go_binary, os.X_OK), f"Go binary {go_binary} is not executable"

    lib_dir = "/home/user/workspace/lib"
    assert os.path.isdir(lib_dir), f"Library directory missing at {lib_dir}"

    # The prompt specifies the shared library name should be libkissfft.so
    lib_path = os.path.join(lib_dir, "libkissfft.so")
    assert os.path.isfile(lib_path), f"Shared library missing at {lib_path}"