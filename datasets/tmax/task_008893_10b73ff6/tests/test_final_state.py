# test_final_state.py
import os
import csv
import sqlite3

def test_audit_report_exists_and_correct():
    csv_path = "/home/user/audit_report.csv"
    assert os.path.exists(csv_path), f"Expected output file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"{csv_path} is not a regular file."

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = list(csv.reader(f))

    assert len(reader) >= 1, f"{csv_path} is empty."

    # The requirement is that the final output contains exactly:
    # A001,B002,C003,alice_compliance,bob_finance,charlie_admin
    # We will check if any row matches this exactly, or if the first row matches.

    # To be robust against extra newlines or headers, let's look for the specific row.
    expected_row = ["A001", "B002", "C003", "alice_compliance", "bob_finance", "charlie_admin"]

    found = False
    for row in reader:
        # Strip whitespace just in case
        clean_row = [cell.strip() for cell in row]
        if clean_row == expected_row:
            found = True
            break

    assert found, f"Could not find the expected row {expected_row} in {csv_path}. Found: {reader}"

def test_run_audit_script_exists():
    script_path = "/home/user/run_audit.py"
    assert os.path.exists(script_path), f"Expected script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a regular file."