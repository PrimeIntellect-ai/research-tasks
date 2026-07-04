# test_final_state.py

import os
import pytest

def test_binary_exists_and_executable():
    binary_path = "/home/user/telemetry_svc/parser_svc"
    assert os.path.isfile(binary_path), f"Binary {binary_path} was not built."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."

def test_postmortem_exists():
    pm_path = "/home/user/postmortem.txt"
    assert os.path.isfile(pm_path), f"Post-mortem file {pm_path} does not exist."
    assert os.path.getsize(pm_path) > 0, f"Post-mortem file {pm_path} is empty."

def test_clean_data_correctness():
    output_path = "/home/user/clean_data.csv"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did you run the binary?"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 5, "Output file does not contain all expected rows (header + 4 data rows). The program might have crashed."

    # Check header
    assert "TIMESTAMP" in lines[0], "Header row is missing or incorrect."

    # Check precision loss and correct parsing
    expected_timestamps = [
        "1700000000123456",
        "1700000000223456",
        "1700000000323456",
        "1700000000423456"
    ]

    extracted_timestamps = []
    for line in lines[1:]:
        parts = line.split(",")
        if len(parts) >= 2:
            extracted_timestamps.append(parts[1])

    for expected in expected_timestamps:
        assert expected in extracted_timestamps, f"Expected timestamp {expected} not found in output. Precision loss bug is likely not fixed."