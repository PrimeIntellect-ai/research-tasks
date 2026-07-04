# test_final_state.py

import os
import csv
import pytest

def test_csv_file_exists():
    """Verify that the output CSV file exists."""
    csv_file = "/home/user/failed_backups_report.csv"
    assert os.path.exists(csv_file), f"Expected output file {csv_file} does not exist. Did you create it?"
    assert os.path.isfile(csv_file), f"Path {csv_file} is not a file."

def test_csv_file_content():
    """Verify that the CSV file contains the correct aggregated and sorted data."""
    csv_file = "/home/user/failed_backups_report.csv"

    expected_rows = [
        ["cluster", "avg_failed_duration", "longest_job_1", "longest_job_2", "longest_job_3"],
        ["alpha-cluster", "125.0", "job_a2", "job_a3", "job_a1"],
        ["beta-cluster", "300.0", "job_b1", "job_b2", ""],
        ["delta-cluster", "45.0", "job_d1", "", ""]
    ]

    actual_rows = []
    with open(csv_file, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) > 0, f"The file {csv_file} is empty."

    # Check header
    assert actual_rows[0] == expected_rows[0], f"CSV header is incorrect. Expected {expected_rows[0]}, got {actual_rows[0]}."

    # Check number of rows
    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows (including header), but found {len(actual_rows)}."

    # Check data rows exactly
    for i in range(1, len(expected_rows)):
        assert actual_rows[i] == expected_rows[i], f"Row {i+1} is incorrect. Expected {expected_rows[i]}, got {actual_rows[i]}."