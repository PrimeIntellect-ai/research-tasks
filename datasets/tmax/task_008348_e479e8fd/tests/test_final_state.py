# test_final_state.py

import os
import csv
import re
import pytest

def test_violations_csv_exists_and_correct():
    csv_path = '/home/user/violations.csv'
    assert os.path.exists(csv_path), f"Expected output file {csv_path} is missing."
    assert os.path.isfile(csv_path), f"{csv_path} is not a file."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "violations.csv is empty."

    header = rows[0]
    expected_header = ['emp_id', 'resource_id', 'violation_count']
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]
    expected_data = [
        ['2', 'R1', '1'],
        ['3', 'R2', '2'],
        ['4', 'R1', '1']
    ]

    assert data_rows == expected_data, f"CSV data is incorrect. Expected {expected_data}, got {data_rows}."

def test_index_sql_exists_and_correct():
    sql_path = '/home/user/index.sql'
    assert os.path.exists(sql_path), f"Expected SQL file {sql_path} is missing."
    assert os.path.isfile(sql_path), f"{sql_path} is not a file."

    with open(sql_path, 'r') as f:
        sql_content = f.read().strip().lower()

    assert "create index" in sql_content, "SQL file does not contain 'CREATE INDEX'."
    assert "idx_logs_emp_status" in sql_content, "Index name 'idx_logs_emp_status' is missing."
    assert "on logs" in sql_content or "on logs(" in sql_content or "on logs " in sql_content, "Index is not created on the 'logs' table."

    # Check for columns
    assert "emp_id" in sql_content, "Column 'emp_id' is missing from the index definition."
    assert "status" in sql_content, "Column 'status' is missing from the index definition."

    # Check that it's a composite index of emp_id and status
    match = re.search(r'\((.*?)\)', sql_content)
    assert match is not None, "Could not find column list in parentheses."

    columns = [col.strip() for col in match.group(1).split(',')]
    assert "emp_id" in columns and "status" in columns, "The index must include both 'emp_id' and 'status' columns."