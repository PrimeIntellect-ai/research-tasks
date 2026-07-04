# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = '/home/user/etl_graph.py'
DB_PATH = '/home/user/company_data.db'
OUTPUT_PATH = '/home/user/report.json'

def test_script_exists():
    """Verify that the student's script exists."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_script_execution():
    """Run the script with the required arguments and verify it completes successfully."""
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    result = subprocess.run([
        'python3', SCRIPT_PATH,
        '--db', DB_PATH,
        '--start-date', '2023-01-01',
        '--end-date', '2023-03-31',
        '--output', OUTPUT_PATH
    ], capture_output=True, text=True)

    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert os.path.isfile(OUTPUT_PATH), f"Output JSON file was not created at {OUTPUT_PATH}."

def test_json_output_content():
    """Verify the content of the generated JSON file matches the expected results."""
    assert os.path.isfile(OUTPUT_PATH), f"Output JSON file missing at {OUTPUT_PATH}"

    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

    expected = [
        {
            "user_id": 2,
            "name": "Bob",
            "in_degree": 3
        },
        {
            "user_id": 1,
            "name": "Alice",
            "in_degree": 2
        },
        {
            "user_id": 5,
            "name": "Eve",
            "in_degree": 2
        },
        {
            "user_id": 3,
            "name": "Charlie",
            "in_degree": 1
        }
    ]

    assert data == expected, f"JSON output content does not match expected.\nExpected: {expected}\nActual: {data}"

def test_json_formatting():
    """Verify that the JSON is formatted with exactly 2 spaces of indentation."""
    assert os.path.isfile(OUTPUT_PATH), f"Output JSON file missing at {OUTPUT_PATH}"

    with open(OUTPUT_PATH, 'r') as f:
        content = f.read()

    data = json.loads(content)
    expected_content = json.dumps(data, indent=2)

    assert content.strip() == expected_content.strip(), "JSON output is not formatted with an indentation of 2 spaces."