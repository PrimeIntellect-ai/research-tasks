# test_final_state.py

import os
import pytest

def expected_distance():
    c = 0.1
    for _ in range(100):
        c += 0.05 * c * (1.0 - c) * 0.45

    total = c * 100000
    expected = 50000.0
    return abs(total - expected)

def test_simulate_fixed_executable():
    path = "/home/user/simulate_fixed"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_stability_log():
    path = "/home/user/stability.log"
    assert os.path.exists(path), f"File {path} is missing."
    assert os.path.isfile(path), f"Path {path} is not a file."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines in {path}, found {len(lines)}."

    # Check that all lines are identical (deterministic)
    first_line = lines[0]
    for i, line in enumerate(lines):
        assert line == first_line, f"Line {i+1} ('{line}') differs from the first line ('{first_line}'). Non-determinism is still present."

    # Check that the calculated distance matches the expected true sequential result
    expected_val = expected_distance()
    expected_str = f"{expected_val:.10f}"

    assert first_line == expected_str, f"The logged distance '{first_line}' does not match the expected deterministic value '{expected_str}'."