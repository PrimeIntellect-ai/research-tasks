# test_final_state.py

import os
import pytest

def test_files_exist():
    """Verify that all required files have been created."""
    expected_files = [
        "/home/user/anomaly_detector.cpp",
        "/home/user/run_pipeline.sh",
        "/home/user/detector",
        "/home/user/anomalies.csv",
        "/home/user/anomaly_count.txt"
    ]
    for f in expected_files:
        assert os.path.exists(f), f"Required file is missing: {f}"
        assert os.path.isfile(f), f"Expected {f} to be a file."

def test_anomalies_csv_contents():
    """Verify the contents of anomalies.csv match the expected output."""
    csv_path = "/home/user/anomalies.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist."

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "2023-10-01 10:16:40,55.5,22.0",
        "2023-10-01 11:23:20,88.8,22.0",
        "2023-10-01 12:30:00,99.9,22.0"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {csv_path}, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1} in {csv_path}. Expected: '{expected}', Got: '{actual}'"

def test_anomaly_count_contents():
    """Verify the contents of anomaly_count.txt match the expected output."""
    count_path = "/home/user/anomaly_count.txt"
    assert os.path.exists(count_path), f"File {count_path} does not exist."

    with open(count_path, "r") as f:
        content = f.read().strip()

    assert content == "3", f"Expected '3' in {count_path}, but got '{content}'."