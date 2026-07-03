# test_final_state.py
import csv
import os

def test_zeus_audit_csv():
    csv_path = "/home/user/zeus_audit.csv"
    assert os.path.exists(csv_path), f"File {csv_path} does not exist. The report was not generated."

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    expected_rows = [
        ['employee_id', 'employee_name'],
        ['2', 'Bob'],
        ['3', 'Charlie'],
        ['5', 'Eve'],
        ['6', 'Frank'],
        ['7', 'Grace']
    ]

    assert rows == expected_rows, f"CSV content does not match expected output. Expected {expected_rows}, but got {rows}."