# test_final_state.py

import os
import csv
import pytest

def test_analyze_cpp_exists():
    """Test that the C++ source file was created."""
    file_path = '/home/user/analyze.cpp'
    assert os.path.exists(file_path), f"Source file {file_path} is missing. Did you create it?"
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_alerts_log_correctness():
    """Test that the alerts.log file exists and contains the correctly computed alerts."""
    alerts_path = '/home/user/alerts.log'
    metrics_path = '/home/user/metrics.csv'

    assert os.path.exists(alerts_path), f"Output file {alerts_path} is missing. Did you run the program?"
    assert os.path.exists(metrics_path), f"Input file {metrics_path} is missing."

    # Derive expected output from the input CSV
    web01_rows = []
    with open(metrics_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if row[0] == "web-01":
                web01_rows.append(row)

    # Systematic sampling: every 5th record (0, 5, 10, ...)
    sampled_rows = web01_rows[::5]

    expected_alerts = []
    for i in range(1, len(sampled_rows)):
        prev_val = int(sampled_rows[i-1][2])
        curr_val = int(sampled_rows[i][2])
        delta = curr_val - prev_val

        if delta > 100:
            timestamp = sampled_rows[i][1]
            expected_alerts.append(f"[ALERT] web-01 spike at {timestamp}: +{delta}ms\n")

    # Read actual output
    with open(alerts_path, 'r') as f:
        actual_alerts = f.readlines()

    # Strip trailing whitespace/newlines for robust comparison if the user missed a trailing newline,
    # but the prompt asks for exactly matching strings, one per line.
    actual_alerts_clean = [line.strip() for line in actual_alerts if line.strip()]
    expected_alerts_clean = [line.strip() for line in expected_alerts]

    assert actual_alerts_clean == expected_alerts_clean, (
        f"Contents of {alerts_path} do not match the expected alerts. "
        f"Expected: {expected_alerts_clean}, Got: {actual_alerts_clean}"
    )