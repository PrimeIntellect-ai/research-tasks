# test_final_state.py
import os
import csv
import pytest

SCRIPT_PATH = '/home/user/generate_plan.py'
CSV_PATH = '/home/user/restore_plan.csv'

def test_script_exists():
    """Test that the Python script was created."""
    assert os.path.isfile(SCRIPT_PATH), f"Script file missing at {SCRIPT_PATH}"

def test_csv_exists_and_correct():
    """Test that the CSV output file exists and contains the correct restore plan."""
    assert os.path.isfile(CSV_PATH), f"CSV output file missing at {CSV_PATH}"

    expected_rows = [
        ['step_number', 'backup_id', 'cumulative_size_mb'],
        ['1', 'bkp_005', '5200'],
        ['2', 'bkp_006', '5250']
    ]

    with open(CSV_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, f"CSV content does not match expected output. Expected: {expected_rows}, Actual: {actual_rows}"