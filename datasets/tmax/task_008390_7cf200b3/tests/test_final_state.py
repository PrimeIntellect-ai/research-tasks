# test_final_state.py

import os
import pytest

def test_cross_dependencies_csv_exists():
    """Test that the output CSV file exists."""
    file_path = "/home/user/cross_dependencies.csv"
    assert os.path.exists(file_path), f"The output file {file_path} does not exist. Did your script run and generate it?"
    assert os.path.isfile(file_path), f"The path {file_path} is not a valid file."

def test_cross_dependencies_csv_content():
    """Test that the output CSV file contains the correct cross-dependent employee pairs."""
    file_path = "/home/user/cross_dependencies.csv"
    assert os.path.exists(file_path), f"Cannot test content because {file_path} is missing."

    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "http://example.org/Alice,http://example.org/Bob",
        "http://example.org/Charlie,http://example.org/Diana"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in CSV, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."

def test_script_exists():
    """Test that the python script was created."""
    script_path = "/home/user/find_cycles.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a valid file."