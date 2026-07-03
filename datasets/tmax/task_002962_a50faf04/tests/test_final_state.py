# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = '/home/user/generate_report.py'
REPORT_PATH = '/home/user/report.json'

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file"

def test_report_json_exists_and_correct():
    assert os.path.exists(REPORT_PATH), f"Report not found at {REPORT_PATH}"

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON.")

    expected_data = [
        {"region": "North", "revenue": 2100.0},
        {"region": "South", "revenue": 2000.0},
        {"region": "East", "revenue": 900.0},
        {"region": "West", "revenue": 50.0}
    ]

    assert isinstance(data, list), f"Expected a JSON array, got {type(data).__name__}"
    assert data == expected_data, f"Report data for 'Electronics' does not match expected output or is not sorted correctly. Got: {data}"

def test_script_functionality_with_different_category():
    # Run the script with "Furniture" to ensure it's not hardcoded and processes arguments correctly
    result = subprocess.run(
        ['python3', SCRIPT_PATH, 'Furniture'],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed when running with 'Furniture' category. Stderr: {result.stderr}"
    assert os.path.exists(REPORT_PATH), f"Report not found at {REPORT_PATH} after running script."

    with open(REPORT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {REPORT_PATH} does not contain valid JSON after running with 'Furniture'.")

    expected_data = [
        {"region": "North", "revenue": 200.0}
    ]

    assert data == expected_data, f"Report data for 'Furniture' does not match expected output. Got: {data}"