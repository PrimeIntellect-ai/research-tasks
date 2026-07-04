# test_final_state.py

import os
import pytest

def test_calc_engine_executable_exists():
    path = "/home/user/calc_engine"
    assert os.path.isfile(path), f"Executable {path} is missing. Did you compile the code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_output_txt_exists_and_correct():
    path = "/home/user/output.txt"
    assert os.path.isfile(path), f"Output file {path} is missing. Did you run the compiled program?"

    with open(path, "r") as f:
        lines = f.read().strip().split()

    assert len(lines) == 4, f"Expected 4 lines of output in {path}, but found {len(lines)}."

    try:
        values = [float(line) for line in lines]
    except ValueError:
        pytest.fail(f"Output file {path} contains non-numeric data.")

    expected_values = [0.5, 2.0, 0.0, 1.0]

    for i, (actual, expected) in enumerate(zip(values, expected_values)):
        assert abs(actual - expected) < 1e-6, f"Line {i+1} in {path} is {actual}, expected {expected}."