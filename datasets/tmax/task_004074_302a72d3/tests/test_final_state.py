# test_final_state.py

import os
import pytest

def test_target_vector_file():
    target_file = "/home/user/target_vector.txt"
    assert os.path.isfile(target_file), f"Expected file {target_file} does not exist."

    with open(target_file, "r") as f:
        content = f.read().strip()

    assert content, f"File {target_file} is empty."

    parts = content.split(",")
    assert len(parts) == 5, f"Expected 5 comma-separated values in {target_file}, found {len(parts)}."

    try:
        vector = [float(x) for x in parts]
    except ValueError:
        pytest.fail(f"Could not parse values in {target_file} as floats.")

    expected_vector = [0.26202468, 0.15868397, 0.27812652, 0.45931689, 0.32100054]

    for act, exp in zip(vector, expected_vector):
        assert abs(act - exp) < 1e-4, f"Vector value {act} does not match expected {exp} within tolerance."

def test_best_match_file():
    match_file = "/home/user/best_match.txt"
    assert os.path.isfile(match_file), f"Expected file {match_file} does not exist."

    with open(match_file, "r") as f:
        content = f.read().strip()

    assert content == "exp_beta", f"Expected 'exp_beta' in {match_file}, but found '{content}'."