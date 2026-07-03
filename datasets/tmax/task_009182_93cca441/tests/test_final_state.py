# test_final_state.py

import os
import csv
import re
import pytest

def test_audit_results_csv():
    csv_path = '/home/user/audit_results.csv'
    assert os.path.exists(csv_path), f"File {csv_path} is missing."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    expected_rows = [
        ['EmployeeName', 'DepartmentName', 'AccessTime', 'Resource'],
        ['Alice', 'Finance', '2023-10-01 09:00:00', 'ServerA'],
        ['Bob', 'Payroll', '2023-10-01 09:15:00', 'ServerB'],
        ['Charlie', 'Accounts Payable', '2023-10-01 09:30:00', 'ServerC'],
        ['Alice', 'Finance', '2023-10-01 10:00:00', 'ServerA']
    ]

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_rows = list(reader)

    assert actual_rows == expected_rows, (
        f"CSV content does not match expected output.\n"
        f"Expected: {expected_rows}\n"
        f"Actual: {actual_rows}"
    )

def test_optimize_sql():
    sql_path = '/home/user/optimize.sql'
    assert os.path.exists(sql_path), f"File {sql_path} is missing."
    assert os.path.isfile(sql_path), f"{sql_path} is not a file."

    with open(sql_path, 'r') as f:
        content = f.read().strip()

    # Normalize whitespace and lowercase for comparison
    normalized_content = re.sub(r'\s+', ' ', content).lower()

    # Check for the required components
    assert 'create index' in normalized_content, "Missing 'CREATE INDEX' in SQL file."
    assert 'idx_access_logs_emp_id' in normalized_content, "Missing correct index name 'idx_access_logs_emp_id'."
    assert 'on access_logs' in normalized_content, "Missing 'ON access_logs' in SQL file."
    assert '(emp_id)' in normalized_content.replace(' ', ''), "Missing '(emp_id)' in SQL file."