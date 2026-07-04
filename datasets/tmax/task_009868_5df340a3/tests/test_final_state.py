# test_final_state.py
import os
import pytest

def test_anomalies_file_exists():
    """Test if the output CSV file was created."""
    path = "/home/user/anomalies.csv"
    assert os.path.isfile(path), f"Expected output file {path} is missing."

def test_anomalies_file_content():
    """Test if the output CSV file has the correct computed content."""
    path = "/home/user/anomalies.csv"
    if not os.path.isfile(path):
        pytest.fail(f"File {path} does not exist.")

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "bucket_start,total_impact,moving_avg,is_anomaly",
        "1700002800,30,0.00,0",
        "1700006400,40,30.00,0",
        "1700010000,20,35.00,0",
        "1700013600,70,30.00,1",
        "1700017200,10,43.33,0",
        "1700020800,0,33.33,0",
        "1700024400,60,26.67,1"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in anomalies.csv, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Mismatch at line {i+1}: expected '{expected}', got '{actual}'."