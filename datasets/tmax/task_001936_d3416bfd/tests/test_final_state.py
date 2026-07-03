# test_final_state.py

import os
import csv
import pytest

SCRIPT_PATH = "/home/user/process_logs.sh"
OUTPUT_PATH = "/home/user/sampled_errors.csv"

def test_script_exists_and_executable():
    """Verify that the process_logs.sh script exists and is executable."""
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable"

def test_output_file_exists():
    """Verify that the sampled_errors.csv file was generated."""
    assert os.path.exists(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH}"
    assert os.path.isfile(OUTPUT_PATH), f"{OUTPUT_PATH} is not a file"

def test_output_file_content():
    """Verify the content of sampled_errors.csv matches the expected cleaned and sampled data."""
    expected_rows = [
        ["timestamp", "log_level", "user_id", "message"],
        ["2023-10-01T10:05:00Z", "ERROR", "USR2", "Connection timeout\nat module.network (network.c:120)\nRetrying..."],
        ["2023-10-01T10:20:00Z", "ERROR", "USR4", "Database lock exception"],
        ["2023-10-01T10:10:00Z", "CRITICAL", "USR3", "Kernel panic - not syncing"],
        ["2023-10-01T10:25:00Z", "CRITICAL", "USR5", "Out of memory\nOOM killer invoked"]
    ]

    with open(OUTPUT_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) == 5, f"Expected 5 rows (including header), but got {len(actual_rows)}"

    assert actual_rows[0] == expected_rows[0], "CSV header does not match expected."

    for i in range(1, 5):
        assert actual_rows[i] == expected_rows[i], f"Row {i} does not match expected data. Expected {expected_rows[i]}, got {actual_rows[i]}"

def test_user_ids_uppercase():
    """Ensure all user_ids in the output are uppercase."""
    with open(OUTPUT_PATH, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            assert row['user_id'] == row['user_id'].upper(), f"user_id {row['user_id']} is not uppercase"

def test_log_levels_order():
    """Ensure the output contains 2 ERROR logs followed by 2 CRITICAL logs."""
    with open(OUTPUT_PATH, 'r', newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 4, "Should have exactly 4 data rows."
    assert rows[0]['log_level'] == 'ERROR'
    assert rows[1]['log_level'] == 'ERROR'
    assert rows[2]['log_level'] == 'CRITICAL'
    assert rows[3]['log_level'] == 'CRITICAL'