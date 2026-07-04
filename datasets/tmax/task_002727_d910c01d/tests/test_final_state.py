# test_final_state.py

import os
import csv

def test_org_chart_csv_exists_and_correct():
    file_path = '/home/user/org_chart.csv'
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you run the script?"

    expected_header = ['emp_id', 'name', 'dept_name', 'manager_name', 'management_chain']

    expected_rows = [
        ['1', 'Alice', 'Engineering', '', 'Alice'],
        ['2', 'Bob', 'Engineering', 'Alice', 'Alice->Bob'],
        ['3', 'Charlie', 'Sales', 'Alice', 'Alice->Charlie'],
        ['4', 'Dave', 'Engineering', 'Bob', 'Alice->Bob->Dave'],
        ['5', 'Eve', 'Sales', 'Charlie', 'Alice->Charlie->Eve']
    ]

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, f"{file_path} is empty."

        assert header == expected_header, f"Header in {file_path} is incorrect. Expected {expected_header}, got {header}."

        actual_rows = list(reader)

    # Sort both lists of rows to make the test order-insensitive
    expected_rows_sorted = sorted(expected_rows, key=lambda x: int(x[0]))
    actual_rows_sorted = sorted(actual_rows, key=lambda x: int(x[0]) if x and x[0].isdigit() else 0)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}."

    for actual, expected in zip(actual_rows_sorted, expected_rows_sorted):
        assert actual == expected, f"Row mismatch: Expected {expected}, got {actual}."