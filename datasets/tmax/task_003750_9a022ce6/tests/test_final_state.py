# test_final_state.py

import os
import pytest

def test_anomalies_csv_exists():
    """Test that the anomalies.csv file has been created."""
    file_path = "/home/user/anomalies.csv"
    assert os.path.exists(file_path), f"File {file_path} does not exist."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_anomalies_csv_content():
    """Test that the anomalies.csv file contains the correct results."""
    file_path = "/home/user/anomalies.csv"
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "string_id,language,current_width,rolling_avg",
        "5,FR,150,56",
        "5,JA,110,43",
        "10,DE,105,55"
    ]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in CSV, got {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual.strip()}'."