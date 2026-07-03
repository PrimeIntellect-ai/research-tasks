# test_final_state.py

import os
import pytest

def test_cjson_shared_library_built():
    """Verify that the cJSON shared library was successfully built."""
    so_path = "/app/cJSON/libcjson.so"
    assert os.path.isfile(so_path), f"Shared library not found at {so_path}. Did you fix the Makefile and run make?"

def test_results_csv_accuracy():
    """Verify the accuracy of the computed subtree sums in results.csv."""
    results_path = "/home/user/results.csv"
    assert os.path.isfile(results_path), f"Results file not found at {results_path}."

    expected = {
        "node3": 150.0,
        "node2": 155.0,
        "root": 215.5
    }

    actual = {}
    with open(results_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            assert len(parts) == 2, f"Invalid line format in {results_path}: '{line}'. Expected 'id,subtree_sum'."
            try:
                actual[parts[0]] = float(parts[1])
            except ValueError:
                pytest.fail(f"Invalid numeric value in {results_path}: '{parts[1]}'.")

    correct = 0
    for k, v in expected.items():
        if k in actual and abs(actual[k] - v) < 0.01:
            correct += 1

    # Penalize false positives
    accuracy = correct / max(len(expected), len(actual))

    assert accuracy >= 1.0, f"Accuracy metric failed. Expected 1.0, got {accuracy}. Expected dict: {expected}, Actual dict: {actual}"