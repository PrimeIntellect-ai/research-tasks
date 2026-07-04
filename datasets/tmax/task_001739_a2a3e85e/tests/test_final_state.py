# test_final_state.py

import os
import csv
import ast

def test_script_exists_and_uses_fcntl():
    """Verify that the script exists and uses fcntl.flock."""
    script_path = '/home/user/process_backups.py'
    assert os.path.isfile(script_path), f"Script not found at {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'fcntl' in content, "The script does not appear to import or use 'fcntl'."
    assert 'flock' in content, "The script does not appear to use 'flock' for concurrency safety."

def test_audit_csv_exists():
    """Verify that the audit CSV file was generated."""
    csv_path = '/home/user/backup_audit.csv'
    assert os.path.isfile(csv_path), f"Audit CSV not found at {csv_path}"

def test_audit_csv_content():
    """Verify the content and sorting of the audit CSV."""
    csv_path = '/home/user/backup_audit.csv'

    expected_rows = [
        ['archive_name', 'status', 'app_name', 'version'],
        ['alpha_backup.tar.gz', 'valid', 'FinanceApp', '1.4.2'],
        ['beta_backup.tar.gz', 'valid', 'HRSystem', '2.0.1'],
        ['delta_missing.tar.gz', 'corrupt', 'N/A', 'N/A'],
        ['gamma_corrupted.tar.gz', 'corrupt', 'N/A', 'N/A']
    ]

    actual_rows = []
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_rows.append(row)

    assert actual_rows == expected_rows, (
        f"CSV content does not match expected output.\n"
        f"Expected: {expected_rows}\n"
        f"Actual: {actual_rows}"
    )