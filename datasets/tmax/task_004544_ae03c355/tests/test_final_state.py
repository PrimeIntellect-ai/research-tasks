# test_final_state.py

import os
import json
import pytest

def test_files_exist():
    expected_files = [
        "/home/user/baseline.txt",
        "/home/user/py_float64.txt",
        "/home/user/py_float32.txt",
        "/home/user/metrics.json"
    ]
    for path in expected_files:
        assert os.path.isfile(path), f"Expected output file {path} is missing."

def test_output_lengths():
    txt_files = [
        "/home/user/baseline.txt",
        "/home/user/py_float64.txt",
        "/home/user/py_float32.txt"
    ]
    for path in txt_files:
        if os.path.exists(path):
            with open(path, "r") as f:
                lines = f.read().splitlines()
            assert len(lines) == 10000, f"File {path} does not have exactly 10,000 lines (found {len(lines)})."

def test_metrics_json():
    path = "/home/user/metrics.json"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} is not valid JSON.")

    expected_keys = {
        "ks_stat_float32",
        "ks_stat_float64",
        "wd_float32",
        "wd_float64"
    }

    for key in expected_keys:
        assert key in metrics, f"Key '{key}' is missing from metrics.json"
        assert isinstance(metrics[key], (int, float)), f"Value for '{key}' must be a float."

    # Float64 should be effectively 0
    assert metrics["ks_stat_float64"] < 1e-10, f"ks_stat_float64 is too large: {metrics['ks_stat_float64']}. Expected near 0."
    assert metrics["wd_float64"] < 1e-10, f"wd_float64 is too large: {metrics['wd_float64']}. Expected near 0."

    # Float32 should be strictly greater than 0 due to precision loss
    assert metrics["ks_stat_float32"] > 1e-5, f"ks_stat_float32 is too small: {metrics['ks_stat_float32']}. Expected > 0 due to precision loss."
    assert metrics["wd_float32"] > 1e-5, f"wd_float32 is too small: {metrics['wd_float32']}. Expected > 0 due to precision loss."