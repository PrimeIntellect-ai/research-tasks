# test_final_state.py

import os
import json
import subprocess

SCRIPT_PATH = '/home/user/analyze.py'
OUTPUT_PATH = '/home/user/output.json'
DB_PATH = '/home/user/network.db'

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Python script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file."

def test_script_content_constraints():
    with open(SCRIPT_PATH, 'r') as f:
        content = f.read()

    upper_content = content.upper()

    assert '?' in content or ':' in content, "Script must use parameterized queries ('?' or named parameters)."
    assert 'WITH ' in upper_content, "Script must use SQLite CTEs (WITH clause)."
    assert 'OVER' in upper_content, "Script must use Window Functions (OVER clause)."
    assert 'RANK()' in upper_content or 'DENSE_RANK()' in upper_content, "Script must use RANK() or DENSE_RANK()."

    # Ensure no loops are used in Python for processing
    assert 'for ' not in content and 'while ' not in content, "Script must not use Python loops for processing data."

def test_execution_and_output_north():
    # Remove output if exists to ensure we test the new run
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    # Run the script with North 3 1
    result = subprocess.run(['python3', SCRIPT_PATH, 'North', '3', '1'], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

    expected = [
        {"id": "E4", "type": "Corp", "region": "South", "total_received": 200.0, "regional_rank": 1},
        {"id": "E5", "type": "Bank", "region": "East", "total_received": 300.0, "regional_rank": 1},
        {"id": "E3", "type": "Retail", "region": "South", "total_received": 50.0, "regional_rank": 2}
    ]

    assert data == expected, f"Output JSON does not match expected results.\nExpected: {expected}\nGot: {data}"

def test_execution_and_output_east():
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    # East -> E5, E6
    # 1 hop targets: E6
    # 2 hop targets: none
    # Reached: E6
    # E6 total_received: 150
    # Rank: East Rank 1

    result = subprocess.run(['python3', SCRIPT_PATH, 'East', '10', '0'], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    assert os.path.exists(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, 'r') as f:
        data = json.load(f)

    expected = [
        {"id": "E6", "type": "Retail", "region": "East", "total_received": 150.0, "regional_rank": 1}
    ]

    assert data == expected, f"Output JSON does not match expected results for region East.\nExpected: {expected}\nGot: {data}"