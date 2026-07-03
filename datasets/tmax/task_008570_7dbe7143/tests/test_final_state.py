# test_final_state.py

import os
import csv
import pytest

def test_summary_csv_exists_and_content():
    summary_path = "/home/user/output/summary.csv"
    assert os.path.isfile(summary_path), f"Output file {summary_path} does not exist."

    expected_rows = [
        ["hour", "tier", "resource_type", "count"],
        ["2024-03-15 08:00", "basic", "IP", "1"],
        ["2024-03-15 08:00", "enterprise", "IP", "0"],
        ["2024-03-15 08:00", "premium", "DB", "1"],
        ["2024-03-15 08:00", "premium", "IP", "1"],
        ["2024-03-15 09:00", "basic", "IP", "0"],
        ["2024-03-15 09:00", "enterprise", "IP", "0"],
        ["2024-03-15 09:00", "premium", "IP", "0"],
        ["2024-03-15 10:00", "basic", "IP", "0"],
        ["2024-03-15 10:00", "enterprise", "IP", "0"],
        ["2024-03-15 10:00", "premium", "IP", "1"],
        ["2024-03-15 10:00", "premium", "TIMEOUT", "1"],
    ]

    with open(summary_path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_rows = [row for row in reader if any(field.strip() for field in row)]

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in summary.csv, got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."

def test_pipeline_log_content():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    expected_log_line = "ETL SUCCESS: Processed 5 valid log entries"

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    found = any(expected_log_line in line for line in lines)
    assert found, f"Expected log line '{expected_log_line}' not found in {log_path}."