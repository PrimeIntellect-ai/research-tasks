# test_final_state.py

import os
import csv
import pytest

def test_normalized_metrics_csv_exists():
    """Check that the output CSV file exists."""
    file_path = "/home/user/data/normalized_metrics.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

def test_normalized_metrics_csv_content():
    """Check the content of the output CSV file."""
    file_path = "/home/user/data/normalized_metrics.csv"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    expected_rows = [
        ["normalized_id", "timestamp", "measurement", "rolling_sma"],
        ["sensor_A", "1", "10.00", "10.00"],
        ["sensor_A", "2", "20.00", "15.00"],
        ["sensor_A", "3", "30.00", "20.00"],
        ["sensor_A", "4", "40.00", "30.00"],
        ["sensor_Å", "10", "5.00", "5.00"],
        ["sensor_Å", "11", "15.00", "10.00"],
        ["sensor_Å", "12", "10.00", "10.00"],
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
        assert actual == expected, f"Row {i + 1} mismatch. Expected {expected}, got {actual}."