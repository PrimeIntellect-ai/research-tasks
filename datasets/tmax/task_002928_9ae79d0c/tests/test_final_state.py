# test_final_state.py

import os
import pytest

def test_simulate_go_exists():
    file_path = "/home/user/simulate.go"
    assert os.path.exists(file_path), f"The file {file_path} is missing."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_output_txt_content():
    output_path = "/home/user/output.txt"
    assert os.path.exists(output_path), f"The file {output_path} is missing. Did you run the Go program?"
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    expected_lines = [
        "Mean Initial: 10.6400",
        "Std Initial: 0.8030",
        "Lower CI: 4.9967",
        "Upper CI: 5.0001"
    ]

    with open(output_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output.txt, but got {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch in output.txt: expected '{expected}', got '{actual}'."