# test_final_state.py

import os
import csv

def test_backup_report_exists():
    assert os.path.isfile('/home/user/backup_report.csv'), "/home/user/backup_report.csv does not exist. The script failed to generate the report."

def test_backup_report_content():
    expected_rows = [
        ['project_name', 'file_name', 'file_type', 'header_info'],
        ['alpha', 'app.log', 'text', '[LOG] 2023-10-01 System Initialized'],
        ['alpha', 'data.dat', 'binary', 'DEADBEEF'],
        ['beta', 'cache.dat', 'binary', 'CAFEBABE'],
        ['beta', 'error.log', 'text', '[LOG] 2023-10-02 Warning Encountered']
    ]

    with open('/home/user/backup_report.csv', 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert len(actual_rows) > 0, "The CSV file is empty."

    # Check header
    assert actual_rows[0] == expected_rows[0], f"CSV header mismatch. Expected {expected_rows[0]}, got {actual_rows[0]}"

    # Check data rows
    assert len(actual_rows) == len(expected_rows), f"CSV row count mismatch. Expected {len(expected_rows)} rows, got {len(actual_rows)}."

    for i in range(1, len(expected_rows)):
        assert actual_rows[i] == expected_rows[i], f"CSV data mismatch at row {i + 1}. Expected {expected_rows[i]}, got {actual_rows[i]}"