# test_final_state.py

import os

def test_weights_file_exists():
    file_path = "/home/user/weights.txt"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. The task requires generating this file."

def test_weights_file_content():
    expected_file = "/tmp/expected_weights.txt"
    actual_file = "/home/user/weights.txt"

    assert os.path.isfile(expected_file), f"Expected truth file {expected_file} is missing."
    assert os.path.isfile(actual_file), f"Output file {actual_file} is missing."

    with open(expected_file, "r") as f:
        expected_content = f.read().strip()

    with open(actual_file, "r") as f:
        actual_content = f.read().strip()

    assert expected_content, "Expected content is empty."
    assert actual_content, "Actual content is empty."

    expected_weights = expected_content.split(",")
    actual_weights = actual_content.split(",")

    assert len(actual_weights) == 3, f"Expected 3 weights separated by commas, found {len(actual_weights)}."

    for i, (expected, actual) in enumerate(zip(expected_weights, actual_weights)):
        assert actual == expected, f"Weight at index {i} does not match. Expected '{expected}', got '{actual}'."