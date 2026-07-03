# test_final_state.py
import os
import pytest

def test_predictions_file_exists():
    """Check if the output file /home/user/predictions.csv was created."""
    file_path = "/home/user/predictions.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} is missing. Did you run the C++ program?"

def test_predictions_file_content():
    """Verify the exact contents of the predictions.csv file."""
    file_path = "/home/user/predictions.csv"

    expected_content = [
        "id,score,prediction",
        "1,0.2642,1",
        "2,0.2636,1",
        "3,0.0000,0",
        "4,-0.9000,0",
        "5,0.0462,0",
        "6,0.0457,0"
    ]

    with open(file_path, "r") as f:
        actual_content = [line.strip() for line in f if line.strip()]

    assert len(actual_content) == len(expected_content), f"Expected {len(expected_content)} lines, but got {len(actual_content)}."

    for i, (actual, expected) in enumerate(zip(actual_content, expected_content)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."