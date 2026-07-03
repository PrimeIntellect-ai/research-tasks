# test_final_state.py

import os
import subprocess
import csv

def run_script(emp_id):
    script_path = "/home/user/audit.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    result = subprocess.run(["bash", script_path, emp_id], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed for {emp_id} with error: {result.stderr}"

def test_audit_e01():
    run_script("E01")
    output_file = "/home/user/flagged_E01.csv"
    assert os.path.exists(output_file), f"Output file {output_file} was not created."

    with open(output_file, 'r') as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, f"{output_file} is empty."
    assert reader[0] == ["user_id", "timestamp", "rolling_bytes"], f"Incorrect header in {output_file}."

    # Expected data rows for E01
    expected_rows = [
        ["E05", "2023-10-01T10:10:00Z", "6000"],
        ["E04", "2023-10-01T10:12:00Z", "6000"],
        ["E02", "2023-10-01T11:00:00Z", "6000"]
    ]

    actual_rows = reader[1:]
    assert actual_rows == expected_rows, f"Data rows in {output_file} do not match expected output.\nExpected: {expected_rows}\nActual: {actual_rows}"

def test_audit_e03():
    run_script("E03")
    output_file = "/home/user/flagged_E03.csv"
    assert os.path.exists(output_file), f"Output file {output_file} was not created."

    with open(output_file, 'r') as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, f"{output_file} is empty."
    assert reader[0] == ["user_id", "timestamp", "rolling_bytes"], f"Incorrect header in {output_file}."

    # Expected data rows for E03
    expected_rows = [
        ["E05", "2023-10-01T10:10:00Z", "6000"]
    ]

    actual_rows = reader[1:]
    assert actual_rows == expected_rows, f"Data rows in {output_file} do not match expected output.\nExpected: {expected_rows}\nActual: {actual_rows}"

def test_db_exists():
    db_path = "/home/user/audit.db"
    assert os.path.exists(db_path), f"Database {db_path} was not created."