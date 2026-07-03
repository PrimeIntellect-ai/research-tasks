# test_final_state.py

import os
import pytest

def test_result_txt_content():
    result_path = "/home/user/result.txt"
    assert os.path.exists(result_path), f"Missing result file at {result_path}"
    assert os.path.isfile(result_path), f"{result_path} is not a file"

    # Compute expected value using Python's float (IEEE 754 double precision)
    x = 0.54321
    r = 3.95
    for _ in range(10000):
        x = r * x * (1.0 - x)
    expected_val = f"{x:.6f}"

    with open(result_path, 'r') as f:
        actual_val = f.read().strip()

    assert actual_val == expected_val, f"Incorrect output in {result_path}. Expected {expected_val}, got {actual_val}"

def test_simulator_go_fixed():
    source_path = "/home/user/simulator.go"
    assert os.path.exists(source_path), f"Missing source code at {source_path}"

    with open(source_path, 'r') as f:
        content = f.read()

    assert "float32" not in content, "simulator.go still contains 'float32', numerical instability not fully fixed."
    assert "float64" in content, "simulator.go does not use 'float64' for the simulation."
    assert "0.54321" in content or ".54321" in content, "simulator.go does not seem to contain the extracted seed value."