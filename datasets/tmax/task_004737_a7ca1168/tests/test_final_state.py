# test_final_state.py

import os
import pytest

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_weights_file():
    weights_path = "/home/user/weights.txt"
    assert os.path.isfile(weights_path), f"Weights file {weights_path} does not exist."

    with open(weights_path, 'r') as f:
        lines = f.read().splitlines()

    # Remove empty lines
    lines = [line.strip() for line in lines if line.strip()]

    assert len(lines) == 3, f"Expected 3 weights, found {len(lines)} in {weights_path}."

    try:
        weights = [float(x) for x in lines]
    except ValueError:
        pytest.fail(f"Could not parse weights as floats in {weights_path}.")

    expected_weights = [10.0, 0.0, 20.0]

    for i, (w, ew) in enumerate(zip(weights, expected_weights)):
        assert abs(w - ew) < 1e-4, f"Weight {i+1} is {w}, expected approximately {ew}."

def test_norm_file():
    norm_path = "/home/user/norm.txt"
    assert os.path.isfile(norm_path), f"Norm file {norm_path} does not exist."

    with open(norm_path, 'r') as f:
        content = f.read().strip()

    assert content == "22.36", f"Expected norm to be '22.36', but got '{content}'."