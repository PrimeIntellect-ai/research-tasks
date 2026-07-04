# test_final_state.py

import os
import pytest

def test_simulate_go_fixed():
    path = "/home/user/simulate.go"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "dt := 0.001" in content, f"Expected fixed dt value 'dt := 0.001' not found in {path}"
    assert "dt := 2.5" not in content, f"Buggy dt value 'dt := 2.5' still found in {path}"

def test_final_states_txt_exists_and_valid():
    path = "/home/user/final_states.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 7, f"Expected 7 lines in {path}, found {len(lines)}"

    # Ensure they are valid floats
    for line in lines:
        try:
            float(line)
        except ValueError:
            pytest.fail(f"Could not parse '{line}' as a float in {path}")

def test_mean_attenuation_txt():
    path = "/home/user/mean_attenuation.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "0.0821", f"Expected mean attenuation to be '0.0821', but got '{content}'"