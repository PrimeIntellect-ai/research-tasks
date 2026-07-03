# test_final_state.py

import os
import pytest

def test_source_files_exist():
    """Verify that the required source files and Makefile exist."""
    required_files = [
        "/home/user/extractor.c",
        "/home/user/detector.c",
        "/home/user/Makefile"
    ]
    for file_path in required_files:
        assert os.path.isfile(file_path), f"Required file is missing: {file_path}"

def test_parsed_csv_content():
    """Verify that parsed.csv exists and contains the correct extracted records."""
    file_path = "/home/user/parsed.csv"
    assert os.path.isfile(file_path), f"The output file {file_path} does not exist."

    expected_lines = [
        "timestamp,sensor_id,value",
        "2023-10-01T12:00:02Z,S1,10.5",
        "2023-10-01T12:00:03Z,S2,100.0",
        "2023-10-01T12:00:04Z,S1,11.0",
        "2023-10-01T12:00:05Z,S1,45.0",
        "2023-10-01T12:00:06Z,S1,46.0",
        "2023-10-01T12:00:07Z,S2,101.0",
        "2023-10-01T12:00:08Z,S1,20.0"
    ]

    with open(file_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"The content of {file_path} does not match the expected extracted data."

def test_anomalies_csv_content():
    """Verify that anomalies.csv exists and contains the correct anomaly records."""
    file_path = "/home/user/anomalies.csv"
    assert os.path.isfile(file_path), f"The output file {file_path} does not exist."

    expected_lines = [
        "timestamp,sensor_id,value,diff",
        "2023-10-01T12:00:05Z,S1,45.0,34.0",
        "2023-10-01T12:00:08Z,S1,20.0,26.0"
    ]

    with open(file_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"The content of {file_path} does not match the expected anomaly data."