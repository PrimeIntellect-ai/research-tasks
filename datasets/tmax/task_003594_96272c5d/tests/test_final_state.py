# test_final_state.py
import os
import json
import subprocess
import pytest

SCRIPT_PATH = '/home/user/graph_etl.py'
OUTPUT_FILE_2 = '/home/user/output_depth_2.json'
OUTPUT_FILE_3 = '/home/user/output_depth_3.json'

def test_script_exists():
    """Check if the required Python script exists."""
    assert os.path.exists(SCRIPT_PATH), f"Script missing at {SCRIPT_PATH}"
    assert os.path.isfile(SCRIPT_PATH), f"Path {SCRIPT_PATH} is not a file"

def test_output_file_2_exists_and_correct():
    """Check if the output file for depth 2 exists and has the correct JSON content."""
    assert os.path.exists(OUTPUT_FILE_2), f"Output file missing at {OUTPUT_FILE_2}"

    with open(OUTPUT_FILE_2, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_FILE_2} is not valid JSON")

    assert "target_depth" in data, "Key 'target_depth' missing in JSON"
    assert data["target_depth"] == 2, f"Expected target_depth to be 2, got {data['target_depth']}"

    assert "employees" in data, "Key 'employees' missing in JSON"
    expected_employees = ["Tom", "Uma", "Victor", "Wendy"]
    assert data["employees"] == expected_employees, f"Expected employees {expected_employees}, got {data['employees']}"

def test_script_works_for_other_depths():
    """Run the script for depth 3 to verify it uses the command-line argument and processes correctly."""
    assert os.path.exists(SCRIPT_PATH), f"Cannot run test, script missing at {SCRIPT_PATH}"

    result = subprocess.run(['python3', SCRIPT_PATH, '3'], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed when run for depth 3. Stderr: {result.stderr}"

    assert os.path.exists(OUTPUT_FILE_3), f"Output file missing at {OUTPUT_FILE_3} after running script for depth 3"

    with open(OUTPUT_FILE_3, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_FILE_3} is not valid JSON")

    assert data.get("target_depth") == 3, f"Expected target_depth 3, got {data.get('target_depth')}"
    expected_employees = ["Rachel", "Sarah"]
    assert data.get("employees") == expected_employees, f"Expected employees {expected_employees}, got {data.get('employees')}"