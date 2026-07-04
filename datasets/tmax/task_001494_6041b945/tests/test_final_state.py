# test_final_state.py

import os
import csv
import pytest

def test_run_pipeline_script_exists_and_executable():
    """Test that the run_pipeline.sh script exists and is executable."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    assert os.path.isfile(script_path), f"Expected {script_path} to be a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_summary_csv_exists():
    """Test that the summary.csv file exists."""
    csv_path = "/home/user/summary.csv"
    assert os.path.exists(csv_path), f"Missing output file: {csv_path}"
    assert os.path.isfile(csv_path), f"Expected {csv_path} to be a file."

def test_summary_csv_contents():
    """Test that the summary.csv file has the correct content."""
    csv_path = "/home/user/summary.csv"

    expected_header = ["user_id", "total_valid_events", "max_rolling_avg", "unique_masked_ips"]
    expected_rows = {
        "user_a": ["user_a", "4", "30.0", "192.168.1.xxx"],
        "user_b": ["user_b", "2", "10.0", "10.0.0.xxx"],
        "user_c": ["user_c", "1", "50.0", "172.16.254.xxx"]
    }

    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"File {csv_path} is empty."

    header = rows[0]
    assert header == expected_header, f"Expected header {expected_header}, but got {header}"

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected 3 data rows, but got {len(data_rows)}"

    actual_rows_dict = {}
    for row in data_rows:
        assert len(row) == 4, f"Row does not have 4 columns: {row}"
        actual_rows_dict[row[0]] = row

    for user_id, expected_row in expected_rows.items():
        assert user_id in actual_rows_dict, f"Missing data for user: {user_id}"
        assert actual_rows_dict[user_id] == expected_row, f"Incorrect data for {user_id}. Expected {expected_row}, got {actual_rows_dict[user_id]}"