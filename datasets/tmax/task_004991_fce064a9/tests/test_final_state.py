# test_final_state.py

import os
import csv

def test_compliance_report_contents():
    csv_path = '/home/user/compliance_report.csv'
    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist."

    expected_rows = [
        ['department', 'system_name', 'access_count'],
        ['Finance', 'FIN-01', '2'],
        ['Finance', 'PRD-DB', '1'],
        ['IT', 'FIN-01', '1'],
        ['IT', 'PRD-DB', '2']
    ]

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        # Strip trailing whitespaces if any, and ignore empty lines
        actual_rows = [[cell.strip() for cell in row] for row in reader if row]

    assert len(actual_rows) > 0, "The compliance report CSV is empty."
    assert actual_rows[0] == expected_rows[0], f"CSV headers are incorrect. Expected {expected_rows[0]}, got {actual_rows[0]}"

    assert actual_rows == expected_rows, (
        f"CSV data rows do not match the expected output or are incorrectly sorted.\n"
        f"Expected: {expected_rows}\n"
        f"Actual: {actual_rows}"
    )