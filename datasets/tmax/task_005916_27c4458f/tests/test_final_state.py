# test_final_state.py

import os
import csv
import pytest

def test_csv_report_exists():
    csv_path = '/home/user/task_report.csv'
    assert os.path.isfile(csv_path), f"The report file {csv_path} does not exist."

def test_csv_report_content():
    csv_path = '/home/user/task_report.csv'
    assert os.path.isfile(csv_path), f"The report file {csv_path} does not exist."

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The CSV file is empty."

    header = rows[0]
    expected_header = ['employee_id', 'employee_name', 'total_tasks']
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]

    # Expected data derived from the truth
    expected_data = [
        ['5', 'Eve', '2'],
        ['1', 'Alice', '1'],
        ['2', 'Bob', '1'],
        ['3', 'Charlie', '1'],
        ['4', 'Dave', '1'],
        ['6', 'Frank', '0']
    ]

    assert len(data_rows) == len(expected_data), f"Expected {len(expected_data)} data rows, but got {len(data_rows)}."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_data)):
        assert actual == expected, f"Row {i+1} is incorrect. Expected {expected}, got {actual}."

def test_no_external_employees():
    csv_path = '/home/user/task_report.csv'
    if not os.path.isfile(csv_path):
        pytest.skip("CSV file missing.")

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            employee_id = int(row['employee_id'])
            assert employee_id not in [7, 8], f"Employee {employee_id} should not be in the report as they are not in the CEO's hierarchy."