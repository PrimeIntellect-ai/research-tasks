# test_final_state.py

import os
import csv
import json
import pytest

def test_unauthorized_edges_csv():
    csv_path = '/home/user/unauthorized_edges.csv'
    assert os.path.isfile(csv_path), f"Expected output file {csv_path} is missing."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{csv_path} is empty."

    # Check header
    assert rows[0] == ['user_id', 'resource_id'], f"Header in {csv_path} is incorrect. Expected ['user_id', 'resource_id']."

    # Check data
    expected_data = [
        ['u1', 'r3'],
        ['u3', 'r2'],
        ['u3', 'r4']
    ]

    actual_data = rows[1:]
    assert actual_data == expected_data, f"Data in {csv_path} is incorrect or not properly sorted. Expected {expected_data}, got {actual_data}."

def test_dept_summary_json():
    json_path = '/home/user/dept_summary.json'
    assert os.path.isfile(json_path), f"Expected output file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} does not contain valid JSON.")

    expected_data = {"Sales": 1, "IT": 2}

    assert data == expected_data, f"Data in {json_path} is incorrect. Expected {expected_data}, got {data}."

def test_script_modified():
    script_path = '/home/user/generate_report.py'
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "BROKEN QUERY WITH IMPLICIT CROSS JOIN" not in content or "p.resource_id != a.resource_id" not in content or "unauthorized_edges.csv" in content, "It seems the script was not fully implemented or the broken query was not fixed."