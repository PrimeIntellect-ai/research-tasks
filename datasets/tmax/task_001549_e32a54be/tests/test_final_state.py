# test_final_state.py

import os
import pytest

def test_run_analysis_script_exists_and_executable():
    path = "/home/user/run_analysis.sh"
    assert os.path.isfile(path), f"Missing script: {path}"
    assert os.access(path, os.X_OK), f"Script is not executable: {path}"

def test_clean_data_csv():
    path = "/home/user/clean_data.csv"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) > 0, f"File {path} is empty"
    assert lines[0] == "time,value", f"Incorrect header in {path}"
    assert len(lines) == 201, f"Expected 200 data points + header, found {len(lines)}"

    # Check first data row format
    parts = lines[1].split(",")
    assert len(parts) == 2, f"Incorrect format in data row: {lines[1]}"
    try:
        float(parts[0])
        float(parts[1])
    except ValueError:
        pytest.fail(f"Non-numeric data in {path}: {lines[1]}")

def test_noisy_data_csv():
    clean_path = "/home/user/clean_data.csv"
    noisy_path = "/home/user/noisy_data.csv"
    assert os.path.isfile(noisy_path), f"Missing file: {noisy_path}"

    with open(clean_path, "r") as f:
        clean_lines = [line.strip() for line in f.readlines() if line.strip()]

    with open(noisy_path, "r") as f:
        noisy_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(noisy_lines) == len(clean_lines), f"Line count mismatch between clean and noisy data"
    assert noisy_lines[0] == "time,value", f"Incorrect header in {noisy_path}"

    # Check that +0.05 was added
    clean_parts = clean_lines[1].split(",")
    noisy_parts = noisy_lines[1].split(",")

    assert clean_parts[0] == noisy_parts[0], "Time column should not be modified"

    clean_val = float(clean_parts[1])
    noisy_val = float(noisy_parts[1])

    # Use a small tolerance for floating point arithmetic
    assert abs(noisy_val - (clean_val + 0.05)) < 1e-5, f"Expected value to be increased by 0.05, got {noisy_val} vs {clean_val}"

def test_analysis_report():
    path = "/home/user/analysis_report.txt"
    assert os.path.isfile(path), f"Missing file: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "DATA_POINTS: 200",
        "CLEAN_FREQ: 5.00",
        "REF_COMPARISON: MATCH",
        "NOISY_FREQ: 5.00",
        "STABLE: YES"
    ]

    actual_lines = [line.strip() for line in content.split("\n") if line.strip()]

    for expected in expected_lines:
        assert expected in actual_lines, f"Missing or incorrect line in report: expected '{expected}'"

    assert len(actual_lines) == len(expected_lines), f"Report has extra or missing lines. Expected {len(expected_lines)}, got {len(actual_lines)}"