# test_final_state.py

import os
import pytest

def test_joined_features_exists_and_content():
    path = "/home/user/joined_features.txt"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "1 2.0 0.5",
        "2 3.5 1.0",
        "3 1.0 -1.0",
        "4 0.0 -1.5",
        "5 -2.0 3.0"
    ]

    # We allow variable whitespace between columns as long as the values match
    parsed_lines = [line.split() for line in lines]
    parsed_expected = [line.split() for line in expected]

    assert parsed_lines == parsed_expected, f"Content of {path} does not match the expected joined and sorted output."

def test_predictions_log_exists_and_content():
    path = "/home/user/predictions.log"
    assert os.path.exists(path), f"File {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "1,2.85",
        "2,4.85",
        "3,2.10",
        "4,0.85",
        "5,-4.40"
    ]

    assert lines == expected, f"Content of {path} does not match the expected predictions."

def test_inference_c_exists():
    path = "/home/user/inference.c"
    assert os.path.exists(path), f"Source file {path} is missing."

def test_inference_bin_exists_and_executable():
    path = "/home/user/inference_bin"
    assert os.path.exists(path), f"Binary file {path} is missing."
    assert os.access(path, os.X_OK), f"Binary file {path} is not executable."