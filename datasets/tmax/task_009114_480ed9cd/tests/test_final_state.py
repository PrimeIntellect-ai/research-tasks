# test_final_state.py
import os
import subprocess
import csv

def test_extract_script_exists_and_runs():
    script_path = '/home/user/audit_extract.py'
    csv_path = '/home/user/flagged_employees.csv'

    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    # Remove CSV if it exists to ensure the script actually creates it
    if os.path.exists(csv_path):
        os.remove(csv_path)

    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to run. Stderr: {result.stderr}"

    assert os.path.exists(csv_path), f"CSV file {csv_path} was not created by the script."

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty."
    assert rows[0] == ['emp_id', 'emp_name', 'access_count'], f"CSV header is incorrect. Got: {rows[0]}"

    expected_data = [
        ['3', 'Charlie', '4'],
        ['1', 'Alice', '3'],
        ['5', 'Eve', '3']
    ]

    assert rows[1:] == expected_data, f"CSV data does not match expected output. Got {rows[1:]}"