# test_final_state.py

import os
import pytest

def test_libmetrics_so_exists():
    """Test that the shared library was built."""
    path = "/home/user/libmetrics.so"
    assert os.path.isfile(path), f"Shared library {path} does not exist."

def test_eval_results():
    """Test that eval_results.txt contains the correct evaluated results."""
    path = "/home/user/eval_results.txt"
    assert os.path.isfile(path), f"Results file {path} does not exist."

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    expected_values = ["20.0", "25.0", "16.0", "21.0"]
    for val in expected_values:
        assert val in content, f"Expected value {val} not found in {path}."

def test_metrics_out():
    """Test that metrics.out contains the correct final sum."""
    path = "/home/user/metrics.out"
    assert os.path.isfile(path), f"Metrics output file {path} does not exist."

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    assert "82.00" in content, f"Expected sum 82.00 not found in {path}."

def test_valgrind_log():
    """Test that valgrind.log exists and contains leak check output."""
    path = "/home/user/valgrind.log"
    assert os.path.isfile(path), f"Valgrind log file {path} does not exist."

    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().lower()

    assert "definitely lost:" in content, f"Valgrind log {path} does not contain expected leak check output."