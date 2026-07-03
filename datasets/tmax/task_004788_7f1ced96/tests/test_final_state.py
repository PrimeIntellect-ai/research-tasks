# test_final_state.py

import os
import pytest

def test_go_file_exists():
    """Check if the Go program file exists."""
    file_path = "/home/user/clean_data.go"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

def test_cleaned_csv_content():
    """Verify that cleaned.csv contains only the valid rows and the header."""
    file_path = "/home/user/data/cleaned.csv"
    assert os.path.isfile(file_path), f"File {file_path} was not created."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "event_id,user_id,value",
        "evt_001,1001,45.5",
        "evt_004,1002,11.1",
        "evt_007,-99,0.0",
        "evt_008,0,1.1",
        "evt_010,1004,8.8"
    ]

    assert lines == expected_lines, (
        f"Content of {file_path} does not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {lines}"
    )

def test_anomalies_txt_content():
    """Verify that anomalies.txt contains the event_ids of anomalous rows."""
    file_path = "/home/user/anomalies.txt"
    assert os.path.isfile(file_path), f"File {file_path} was not created."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "evt_003",
        "evt_005",
        "evt_006",
        "evt_009"
    ]

    assert lines == expected_lines, (
        f"Content of {file_path} does not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {lines}"
    )